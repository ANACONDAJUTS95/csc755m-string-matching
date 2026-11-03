"""Timing, comparison counting, memory measurement, CPU pinning, environment info.

The benchmark runs three *separate* passes on the identical input for every
(input, algorithm) job, because each kind of measurement disturbs the others:

1. Timing pass  - clean versions, gc disabled, tracemalloc OFF, repeat-and-divide.
2. Count pass   - counted versions, run once; matches must equal the timing pass.
3. Memory pass  - tracemalloc ON, build the preprocessing structures once.

Nothing in this module prints anything while a timer is running.
"""

import gc
import importlib.metadata
import platform
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

import psutil

import config

PACKAGES = ("numpy", "scipy", "pandas", "matplotlib", "psutil", "pytest")


# ---------------------------------------------------------------------------
# 1. Timing pass
# ---------------------------------------------------------------------------
def time_algorithm(module, text, queries, repeats):
    """Return (prep_time, search_time, matches) in seconds per call.

    Why repeat-and-divide: a single search on a 50-character text takes a few
    microseconds, close to the timer's resolution. Running it R times inside one
    timed interval and dividing by R gives a stable per-call average.
    Why gc.disable(): a garbage-collection pause landing inside one run would
    add noise unrelated to the algorithm. Our structures contain no reference
    cycles, so reference counting still frees everything.
    """
    if tracemalloc.is_tracing():
        raise RuntimeError("tracemalloc must be stopped during the timing pass")

    preprocess = module.preprocess
    search = module.search
    loop = range(repeats)
    perf_counter = time.perf_counter

    gc.collect()  # start every measurement from a clean heap
    gc.disable()
    try:
        # One untimed warm-up call: fills CPU caches and Python's internal caches.
        state = preprocess(queries)
        matches = search(text, state)

        start = perf_counter()
        for _ in loop:
            state = preprocess(queries)
        middle = perf_counter()
        for _ in loop:
            matches = search(text, state)
        end = perf_counter()
    finally:
        gc.enable()

    return (middle - start) / repeats, (end - middle) / repeats, matches


# ---------------------------------------------------------------------------
# 2. Count pass
# ---------------------------------------------------------------------------
def count_algorithm(module, text, queries):
    """Run the counted versions once. Returns a dict of matches and counters."""
    state, prep_comparisons = module.preprocess_counted(queries)
    matches, search_comparisons, failure_steps = module.search_counted(text, state)
    return {
        "matches": matches,
        "prep_comparisons": prep_comparisons,
        "search_comparisons": search_comparisons,
        "search_failure_steps": failure_steps,
    }


# ---------------------------------------------------------------------------
# 3. Memory pass
# ---------------------------------------------------------------------------
def _traced_build(build):
    """Run build() under tracemalloc; return (current - baseline, peak - baseline).

    `current` is read while the built structures are still alive, so it is the
    size they retain. `peak` also includes temporary objects created and freed
    during the build.
    """
    gc.collect()
    tracemalloc.start()
    try:
        baseline_current, _ = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        state = build()
        current, peak = tracemalloc.get_traced_memory()  # read while `state` is alive
    finally:
        tracemalloc.stop()
    return current - baseline_current, peak - baseline_current, state


def character_object_bytes(module, state):
    """Bytes of the per-character string objects the structure keeps alive.

    CPython shares one cached object for every character with ord <= 255, so those
    cost nothing. A character above 255 (e.g. Alice's curly quotes) is a separate
    string object. Only Aho-Corasick stores characters (as trie dict keys); each such
    key is counted once (de-duplicated by id) with sys.getsizeof.
    """
    if not hasattr(module, "trie_keys"):
        return 0
    unique = {id(key): key for key in module.trie_keys(state) if ord(key) > 255}
    return sum(sys.getsizeof(key) for key in unique.values())


def measure_memory(module, queries):
    """Return (memory_bytes, memory_retained_raw_bytes, memory_peak_bytes).

    memory_retained_raw_bytes = current - baseline after the build, structures alive.
    memory_bytes              = raw minus the per-character string objects of
                                Aho-Corasick's trie keys with ord > 255, i.e. the
                                structure only (nodes, dicts, failure links, output
                                lists). For KMP it equals the raw value.
                                Used by every memory test.
    memory_peak_bytes         = peak - baseline (includes short-lived temporaries).

    The harness itself leaves two int objects alive (the values returned by the first
    get_traced_memory() call). That fixed overhead is measured with an empty build
    right before and subtracted, so an empty structure measures 0.
    Naive builds nothing, so it records (0, 0, 0).
    """
    if not module.HAS_PREPROCESSING:
        return 0, 0, 0
    overhead_current, overhead_peak, _ = _traced_build(lambda: None)
    retained, peak, state = _traced_build(lambda: module.preprocess(queries))
    raw = retained - overhead_current
    structure = raw - character_object_bytes(module, state)
    del state
    return structure, raw, peak - overhead_peak


# ---------------------------------------------------------------------------
# Core type of the pinned logical processor (hybrid CPUs such as Zen 5 + Zen 5c)
# ---------------------------------------------------------------------------
def _windows_cpu_sets():
    """{logical processor: (core index, last-level-cache index, efficiency class)} via the Win32 API."""
    import ctypes
    import ctypes.wintypes as wt
    import struct

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    needed = wt.ULONG(0)
    kernel32.GetSystemCpuSetInformation(None, 0, ctypes.byref(needed), None, 0)
    buf = ctypes.create_string_buffer(needed.value)
    if not kernel32.GetSystemCpuSetInformation(buf, needed, ctypes.byref(needed), None, 0):
        raise OSError(ctypes.get_last_error(), "GetSystemCpuSetInformation failed")
    out, offset = {}, 0
    while offset < needed.value:
        size, _type = struct.unpack_from("<II", buf.raw, offset)
        # SYSTEM_CPU_SET_INFORMATION.CpuSet: Id, Group, LogicalProcessorIndex, CoreIndex,
        # LastLevelCacheIndex, NumaNodeIndex, EfficiencyClass
        _id, _group, lp, core, llc, _numa, eff = struct.unpack_from("<IHBBBBB", buf.raw, offset + 8)
        out[lp] = (core, llc, eff)
        offset += size
    return out


def _linux_l3_sizes():
    """{logical cpu: L3 size in KiB} from sysfs. Hybrid Zen 5 / Zen 5c parts have two L3 sizes."""
    out = {}
    for cpu_dir in Path("/sys/devices/system/cpu").glob("cpu[0-9]*"):
        size_file = cpu_dir / "cache" / "index3" / "size"
        if size_file.exists():
            text = size_file.read_text().strip().upper()  # e.g. "16384K" or "16M"
            digits = "".join(c for c in text if c.isdigit())
            unit = {"M": 1024, "G": 1024 * 1024}.get(text.rstrip("B")[-1:], 1)
            out[int(cpu_dir.name[3:])] = int(digits) * unit
    return out


def core_type_info(pinned_core, cpu_model):
    """Classify the pinned logical processor's core type.

    Returns a dict with: reliable (bool), method, summary, classes (list of rows),
    pinned_class_is_fastest (bool or None) and psutil per-core max frequencies.
    Windows: EfficiencyClass from GetSystemCpuSetInformation (higher = faster core).
    Linux:   L3 cluster size from sysfs (the faster cluster has the larger L3).
    """
    info = {"reliable": False, "method": "", "summary": "", "classes": [],
            "pinned_class_is_fastest": None, "psutil_max_mhz": []}
    try:
        info["psutil_max_mhz"] = [round(f.max) for f in psutil.cpu_freq(percpu=True) or []]
    except (OSError, NotImplementedError, AttributeError, psutil.Error):
        pass

    groups = {}  # class value -> list of logical processors (higher value = faster cores)
    try:
        if sys.platform == "win32":
            for lp, (_core, _llc, eff) in _windows_cpu_sets().items():
                groups.setdefault(eff, []).append(lp)
            info["method"] = "Windows GetSystemCpuSetInformation EfficiencyClass (higher = faster core type)"
        elif sys.platform.startswith("linux"):
            for cpu, l3 in _linux_l3_sizes().items():
                groups.setdefault(l3, []).append(cpu)
            info["method"] = "Linux sysfs L3 cache size per logical CPU (larger L3 = faster core type)"
    except (OSError, ValueError, AttributeError) as exc:
        info["method"] = f"detection failed: {exc!r}"
        groups = {}

    if not groups or pinned_core not in {lp for lps in groups.values() for lp in lps}:
        freqs = info["psutil_max_mhz"]
        info["summary"] = ("Core type could NOT be detected reliably. psutil per-core max frequency (MHz): "
                           + (", ".join(f"core {i}: {f}" for i, f in enumerate(freqs)) or "not available"))
        return info

    info["reliable"] = True
    ordered = sorted(groups, reverse=True)  # fastest class first
    hybrid_zen5 = len(ordered) == 2 and "ryzen ai" in cpu_model.lower()
    names = {}
    for rank, cls in enumerate(ordered):
        if len(ordered) == 1:
            names[cls] = "single core type (homogeneous CPU)"
        elif hybrid_zen5:
            names[cls] = "Zen 5" if rank == 0 else "Zen 5c"
        else:
            names[cls] = "fastest core type" if rank == 0 else f"slower core type #{rank}"
        lps = sorted(groups[cls])
        info["classes"].append({"class": cls, "name": names[cls], "logical_processors": lps})
    pinned_cls = next(cls for cls, lps in groups.items() if pinned_core in lps)
    info["pinned_class_is_fastest"] = pinned_cls == ordered[0]
    info["summary"] = f"Logical core {pinned_core} is a **{names[pinned_cls]}** core."
    return info


# ---------------------------------------------------------------------------
# CPU pinning and priority
# ---------------------------------------------------------------------------
def configure_process(core=config.PIN_CORE):
    """Pin to one core and raise priority. Never fails: problems become warnings."""
    proc = psutil.Process()
    status = {
        "pinned_core": core,
        "pin_ok": False,
        "pin_message": "",
        "priority_ok": False,
        "priority_message": "",
        "warnings": [],
    }

    try:
        proc.cpu_affinity([core])
        status["pin_ok"] = proc.cpu_affinity() == [core]
        status["pin_message"] = f"cpu_affinity set to {proc.cpu_affinity()}"
    except (AttributeError, ValueError, OSError, psutil.Error) as exc:
        status["pin_message"] = f"could not pin to core {core}: {exc!r}"
        status["warnings"].append(status["pin_message"])

    try:
        if sys.platform == "win32":
            proc.nice(psutil.HIGH_PRIORITY_CLASS)
            status["priority_ok"] = proc.nice() == psutil.HIGH_PRIORITY_CLASS
            status["priority_message"] = "HIGH_PRIORITY_CLASS"
        else:
            proc.nice(config.LINUX_NICE)
            status["priority_ok"] = proc.nice() == config.LINUX_NICE
            status["priority_message"] = f"nice {proc.nice()}"
    except (AttributeError, ValueError, OSError, psutil.Error) as exc:
        status["priority_message"] = (
            f"could not raise priority ({exc.__class__.__name__}); "
            "running at normal priority. On Linux this needs root or CAP_SYS_NICE."
        )
        status["warnings"].append(status["priority_message"])

    return status


# ---------------------------------------------------------------------------
# Environment information
# ---------------------------------------------------------------------------
def _cpu_model():
    """Human-readable CPU name (platform.processor() is vague on Windows)."""
    if sys.platform == "win32":
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            )
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except OSError:
            pass
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    return platform.processor() or "unknown"


def _os_pretty_name():
    if sys.platform == "win32":
        release, version, *_ = platform.win32_ver()
        build = int(version.split(".")[-1]) if version.count(".") >= 2 else 0
        # Windows 11 still reports release "10"; builds >= 22000 are Windows 11.
        name = "Windows 11" if build >= 22000 else f"Windows {release}"
        return f"{name} ({platform.win32_edition() or 'edition unknown'}, build {version})"
    os_release = Path("/etc/os-release")
    if os_release.exists():
        for line in os_release.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("PRETTY_NAME="):
                return f"{line.split('=', 1)[1].strip(chr(34))} (kernel {platform.release()})"
    return platform.platform()


def installed_ram():
    """(installed RAM in GB, source). Usable RAM (psutil) is lower because of reserved memory.

    Windows reports the installed amount directly. Elsewhere it is estimated by
    rounding usable memory up to the next multiple of 4 GiB (e.g. 15.4 GiB -> 16 GB).
    """
    if sys.platform == "win32":
        try:
            import ctypes

            kib = ctypes.c_ulonglong(0)
            if ctypes.windll.kernel32.GetPhysicallyInstalledSystemMemory(ctypes.byref(kib)):
                return round(kib.value / 1024**2), "GetPhysicallyInstalledSystemMemory"
        except (OSError, AttributeError):
            pass
    usable_gib = psutil.virtual_memory().total / 2**30
    return int(-(-usable_gib // 4) * 4), "estimated: usable RAM rounded up to a multiple of 4 GiB"


def package_versions():
    versions = {}
    for name in PACKAGES:
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "not installed"
    return versions


def environment_info():
    """Everything a reader needs to know about the machine and software."""
    freq = None
    try:
        f = psutil.cpu_freq()
        freq = {"current_mhz": f.current, "max_mhz": f.max} if f else None
    except (OSError, NotImplementedError, psutil.Error):
        pass
    clock = time.get_clock_info("perf_counter")
    cpu_model = _cpu_model()
    return {
        "os": _os_pretty_name(),
        "platform": platform.platform(),
        "machine_arch": platform.machine(),
        "cpu_model": cpu_model,
        "core_type": core_type_info(config.PIN_CORE, cpu_model),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "cpu_freq": freq,
        "ram_bytes": psutil.virtual_memory().total,
        "ram_installed_gb": installed_ram()[0],
        "ram_installed_source": installed_ram()[1],
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_build": " ".join(platform.python_build()),
        "python_compiler": platform.python_compiler(),
        "packages": package_versions(),
        "perf_counter": {
            "implementation": clock.implementation,
            "resolution_s": clock.resolution,
            "monotonic": clock.monotonic,
        },
    }


def utc_now():
    return datetime.now(timezone.utc)
