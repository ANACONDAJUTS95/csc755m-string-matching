"""Run the benchmark on one machine.

For every (input instance, algorithm) job, in an order shuffled with ORDER_SEED:
  1. timing pass  (clean version, gc off, repeat-and-divide)
  2. count pass   (counted version; its matches must equal the timing pass)
  3. memory pass  (tracemalloc around preprocessing)
and append one row to results/<machine>/raw_runs.csv, flushed immediately.

The run is resumable: if raw_runs.csv already exists, finished jobs are
skipped. Stop it any time with Ctrl+C and run the same command again.

Usage:
    python run_benchmark.py --machine primary --pilot   # 3 runs per condition
    python run_benchmark.py --machine primary           # full benchmark (30 runs)
    python run_benchmark.py --machine replication
    python run_benchmark.py --machine primary --report-only   # rebuild run_report.md
"""

import argparse
import csv
import json
import os
import random
import sys
import time

import numpy as np

import config
from src import ALGORITHM_MODULES
from src.inputs_io import load_inputs, read_raw_runs, results_dir, verify_inputs_hash
from src.measure import (
    configure_process,
    count_algorithm,
    environment_info,
    measure_memory,
    time_algorithm,
    utc_now,
)
from src.report import fmt_num, md_escape, md_table, range_label
from src.summaries import FACTOR_VIEWS, METRICS, per_condition_table, positive_control_table, wide_table


class MatchMismatchError(RuntimeError):
    """Counted and clean versions disagree: always a bug, never noise."""


# ---------------------------------------------------------------------------
# Jobs
# ---------------------------------------------------------------------------
def build_jobs(inputs, pilot):
    """All (order_index, input_id, algorithm) jobs in the shuffled order.

    The full list is shuffled first and the pilot keeps only runs 1..PILOT_RUNS,
    so the pilot order is a sub-sequence of the full order.
    """
    jobs = [(rec["input_id"], algo) for rec in inputs for algo in config.ALGORITHMS]
    random.Random(config.ORDER_SEED).shuffle(jobs)
    run_of = {rec["input_id"]: rec["run_id"] for rec in inputs}
    out = []
    for order_index, (input_id, algo) in enumerate(jobs):
        if pilot and run_of[input_id] > config.PILOT_RUNS:
            continue
        out.append((order_index, input_id, algo))
    return out


def blank(value):
    return "" if value is None else value


def run_job(rec, algo, machine, order_index):
    """Measure one (input, algorithm) job and return its CSV row."""
    module = ALGORITHM_MODULES[algo]
    text, queries = rec["text"], rec["queries"]
    repeats = config.REPEATS[rec["text_length_range"]]

    prep_time, search_time, matches = time_algorithm(module, text, queries, repeats)
    counted = count_algorithm(module, text, queries)
    if counted["matches"] != matches:
        raise MatchMismatchError(
            f"input_id={rec['input_id']} algorithm={algo}: counted version found "
            f"{len(counted['matches'])} matches, clean version found {len(matches)}. "
            "The two versions must have identical logic. Stopping."
        )
    memory, memory_raw, memory_peak = measure_memory(module, queries)

    return {
        "experiment": rec["experiment"],
        "algorithm": algo,
        "text_type": blank(rec["text_type"]),
        "alphabet_size": blank(rec["alphabet_size"]),
        "text_length_range": rec["text_length_range"],
        "text_length": rec["text_length"],
        "query_length_range": rec["query_length_range"],
        "query_lengths": "|".join(str(m) for m in rec["query_lengths"]),
        "query_style": blank(rec["query_style"]),
        "num_queries": rec["num_queries"],
        "run_id": rec["run_id"],
        "input_id": rec["input_id"],
        "machine": machine,
        "repeats": repeats,
        "prep_time": repr(prep_time),
        "search_time": repr(search_time),
        "total_time": repr(prep_time + search_time),
        "prep_comparisons": counted["prep_comparisons"],
        "search_comparisons": counted["search_comparisons"],
        "search_failure_steps": blank(counted["search_failure_steps"]),
        "memory_bytes": memory,
        "memory_retained_raw_bytes": memory_raw,
        "memory_peak_bytes": memory_peak,
        "num_matches": len(matches),
        "order_index": order_index,
    }


# ---------------------------------------------------------------------------
# Resuming
# ---------------------------------------------------------------------------
def _row_is_complete(row):
    if len(row) != len(config.CSV_COLUMNS):
        return False
    rec = dict(zip(config.CSV_COLUMNS, row))
    try:
        float(rec["total_time"])
        int(rec["order_index"])
        int(rec["input_id"])
    except ValueError:
        return False
    return True


def load_done(csv_path, machine):
    """Set of (input_id, algorithm) already in the CSV. Drops a half-written last row."""
    if not csv_path.exists():
        return set()
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        csv_path.unlink()
        return set()
    header, body = rows[0], rows[1:]
    if header != config.CSV_COLUMNS:
        sys.exit(f"{csv_path} has an unexpected header; refusing to append to it.")
    good = [r for r in body if _row_is_complete(r)]
    if len(good) != len(body):
        print(f"WARNING: dropping {len(body) - len(good)} incomplete row(s) from {csv_path.name} "
              "(probably interrupted mid-write); those jobs will be re-run.")
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(good)
    machine_idx = config.CSV_COLUMNS.index("machine")
    if any(r[machine_idx] != machine for r in good):
        sys.exit(f"{csv_path} contains rows from another machine label; refusing to mix them.")
    i_idx = config.CSV_COLUMNS.index("input_id")
    a_idx = config.CSV_COLUMNS.index("algorithm")
    return {(int(r[i_idx]), r[a_idx]) for r in good}


def fmt_duration(seconds):
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:d}h {m:02d}m {s:02d}s" if h else f"{m:d}m {s:02d}s"


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def run(machine, pilot):
    out_dir = results_dir(machine, pilot)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "raw_runs.csv"

    ok, actual, expected = verify_inputs_hash()
    if not ok:
        sys.exit(f"inputs/inputs.jsonl hash {actual} does not match the manifest ({expected}). Stopping.")
    print(f"Input hash verified: {actual}")

    inputs = load_inputs()
    by_id = {rec["input_id"]: rec for rec in inputs}
    jobs = build_jobs(inputs, pilot)
    done = load_done(csv_path, machine)
    todo = [j for j in jobs if (j[1], j[2]) not in done]
    print(f"{len(jobs):,} jobs in total, {len(done):,} already done, {len(todo):,} to run "
          f"({'pilot' if pilot else 'full'} run, machine = {machine})")

    status = configure_process(config.PIN_CORE)
    for w in status["warnings"]:
        print(f"WARNING: {w}")
    print(f"Pinned core: {status['pin_message']}; priority: {status['priority_message']}")

    env = environment_info()
    core = env["core_type"]
    print(f"Core type: {core['summary'].replace('**', '')}")
    if core["pinned_class_is_fastest"] is False:
        print(f"WARNING: logical core {config.PIN_CORE} is NOT on the fastest core type of this CPU. "
              "Consider changing PIN_CORE in config.py before the full run.")
    (out_dir / "environment.json").write_text(json.dumps(env, indent=2) + "\n", encoding="utf-8", newline="\n")

    session = {
        "start_utc": utc_now().isoformat(timespec="seconds"),
        "jobs_before": len(done),
        "jobs_planned": len(todo),
        "input_hash": actual,
        "process": status,
        "python_version": env["python_version"],
    }
    t_start = time.perf_counter()
    finished = 0
    interrupted = False
    new_file = not csv_path.exists()
    try:
        with csv_path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=config.CSV_COLUMNS)
            if new_file:
                writer.writeheader()
            for order_index, input_id, algo in todo:
                row = run_job(by_id[input_id], algo, machine, order_index)
                writer.writerow(row)
                f.flush()
                os.fsync(f.fileno())
                finished += 1
                if finished % config.PROGRESS_EVERY == 0 or finished == len(todo):
                    elapsed = time.perf_counter() - t_start
                    eta = elapsed / finished * (len(todo) - finished)
                    print(f"  {len(done) + finished:>5,}/{len(jobs):,} jobs | "
                          f"elapsed {fmt_duration(elapsed)} | ETA {fmt_duration(eta)}", flush=True)
    except KeyboardInterrupt:
        interrupted = True
        print("\nInterrupted. Progress is saved; run the same command again to resume.")

    session.update({
        "end_utc": utc_now().isoformat(timespec="seconds"),
        "duration_s": time.perf_counter() - t_start,
        "jobs_run": finished,
        "interrupted": interrupted,
    })
    with (out_dir / "sessions.jsonl").open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(session) + "\n")

    print(f"Session finished: {finished:,} jobs in {fmt_duration(session['duration_s'])}")
    print("Building run_report.md (re-checks every input's matches; this takes a moment) ...")
    write_run_report(machine, pilot)
    print(f"Wrote {(out_dir / 'run_report.md').relative_to(config.ROOT)}")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def expected_rows(pilot):
    runs = config.PILOT_RUNS if pilot else config.NUM_RUNS
    return number_of_conditions() * runs


def number_of_conditions():
    """171 in the paper's design: 3 algorithms x (108 + 18 + 36 + 9) / 3."""
    n_text = len(config.TEXT_LENGTH_RANGES)
    per_algorithm = (
        len(config.TEXT_TYPES) * n_text * len(config.QUERY_LENGTH_RANGES) * len(config.NUM_QUERIES_LEVELS)
        + len(config.QUERY_STYLES) * n_text
        + len(config.ALPHABETS) * n_text
        + n_text
    )
    return len(config.ALGORITHMS) * per_algorithm


def required_columns(row):
    """Columns that must be non-blank for this row (blank is allowed only where N/A)."""
    req = [
        "experiment", "algorithm", "text_length_range", "text_length", "query_length_range",
        "query_lengths", "num_queries", "run_id", "input_id", "machine", "repeats", "prep_time",
        "search_time", "total_time", "prep_comparisons", "search_comparisons", "memory_bytes",
        "memory_retained_raw_bytes", "memory_peak_bytes", "num_matches", "order_index",
    ]
    if row["experiment"] in ("core", "query_pattern", "alphabet"):
        req.append("text_type")
    if row["experiment"] == "alphabet":
        req.append("alphabet_size")
    if row["experiment"] == "query_pattern":
        req.append("query_style")
    if row["algorithm"] == "aho_corasick":
        req.append("search_failure_steps")
    return req


# Pools for structure-preserving relabelling. Printable ASCII is inside Latin-1 (CPython
# caches these 1-character strings); Cyrillic is outside it (fresh objects every time).
LATIN1_POOL = [chr(c) for c in range(33, 127)]
NON_LATIN1_POOL = [chr(0x0410 + i) for i in range(96)]


def relabel(queries, pool):
    """Rename characters consistently (first-appearance order) using `pool`.

    The result has the same lengths and the same character structure (which
    positions hold equal characters, within and across queries) as the input,
    so LPS tables and trie shapes are unchanged; only the characters differ.
    """
    mapping = {}
    for q in queries:
        for c in q:
            if c not in mapping:
                mapping[c] = pool[len(mapping)]
    return ["".join(mapping[c] for c in q) for q in queries]


MEMORY_MEASURES = [  # (index in measure_memory's result, CSV column)
    (0, "memory_bytes"),
    (1, "memory_retained_raw_bytes"),
    (2, "memory_peak_bytes"),
]


def memory_invariance(df, inputs):
    """For KMP and Aho-Corasick: is each memory measure the same for the original queries,
    an all-Latin-1 relabelling and an all-non-Latin-1 relabelling?"""
    input_ids = sorted(set(int(i) for i in df["input_id"]))
    csv_mem = {(int(i), a): (int(m), int(raw), int(pk)) for i, a, m, raw, pk in zip(
        df["input_id"], df["algorithm"], df["memory_bytes"], df["memory_retained_raw_bytes"],
        df["memory_peak_bytes"])}
    result = {}
    for algo in ("kmp", "aho_corasick"):
        module = ALGORITHM_MODULES[algo]
        r = {"checked": 0, "with_non_latin1": 0, "csv_reproduced": 0, "examples": [],
             "identical": {col: 0 for _, col in MEMORY_MEASURES},
             "max_diff": {col: 0 for _, col in MEMORY_MEASURES}}
        for input_id in input_ids:
            queries = inputs[input_id]["queries"]
            versions = {
                "original": queries,
                "Latin-1": relabel(queries, LATIN1_POOL),
                "non-Latin-1": relabel(queries, NON_LATIN1_POOL),
            }
            mem = {name: measure_memory(module, qs) for name, qs in versions.items()}
            r["checked"] += 1
            r["with_non_latin1"] += any(ord(c) > 0xFF for q in queries for c in q)
            r["csv_reproduced"] += csv_mem.get((input_id, algo)) == tuple(mem["original"])
            for idx, col in MEMORY_MEASURES:
                values = [m[idx] for m in mem.values()]
                r["identical"][col] += len(set(values)) == 1
                r["max_diff"][col] = max(r["max_diff"][col], max(values) - min(values))
                if col == "memory_bytes" and len(set(values)) > 1 and len(r["examples"]) < 3:
                    r["examples"].append((input_id, {k: v[0] for k, v in mem.items()}))
        result[algo] = r
    return result


def memory_invariance_section(inv):
    rows = []
    for algo, r in inv.items():
        n = r["checked"]
        ok = r["identical"]["memory_bytes"] == n
        rows.append([
            config.ALGORITHM_LABELS[algo], f"{n:,}", f"{r['with_non_latin1']:,}",
            f"{'✅' if ok else '❌'} {r['identical']['memory_bytes']:,} / {n:,} "
            f"(max diff {r['max_diff']['memory_bytes']:,} B)",
            f"{r['identical']['memory_retained_raw_bytes']:,} / {n:,} "
            f"(max diff {r['max_diff']['memory_retained_raw_bytes']:,} B)",
            f"{r['identical']['memory_peak_bytes']:,} / {n:,} (max diff {r['max_diff']['memory_peak_bytes']:,} B)",
            f"{r['csv_reproduced']:,} / {n:,}",
        ])
    md = (
        "Every input's queries are measured three times: as generated, renamed to printable ASCII "
        "(inside Latin-1), and renamed to Cyrillic (outside Latin-1). The renaming keeps the lengths and "
        "the character structure (which positions hold equal characters, within and across queries), so "
        "the LPS tables and the trie have exactly the same shape. `memory_bytes` (the tested measure) must "
        "be identical for all three versions; the two descriptive columns are shown for comparison.\n\n"
        + md_table(["Algorithm", "Inputs checked", "Inputs with non-Latin-1 chars",
                    "memory_bytes identical (tested)", "memory_retained_raw_bytes identical",
                    "memory_peak_bytes identical", "CSV values reproduced (all 3 columns)"],
                   rows, ["l", "r", "r", "r", "r", "r", "r"])
    )
    for algo, r in inv.items():
        for input_id, values in r["examples"]:
            md += (f"\n- ❌ {config.ALGORITHM_LABELS[algo]}, input {input_id}: memory_bytes "
                   + ", ".join(f"{k} = {v:,} B" for k, v in values.items()))
    md += ("\n\n*Why the raw retained size differs for Aho-Corasick:* the trie's `dict` keys are the "
           "character objects themselves. CPython shares one cached object per character with code point "
           "≤ 255, but every character above 255 (e.g. Alice's curly quotes) is a separate 60-byte string "
           "object kept alive by the trie. `memory_bytes` subtracts those objects (`sys.getsizeof`, each "
           "object once), leaving the trie's structure only.\n")
    return md + "\n"


def cpython_effect_section(df):
    """Mean (memory_retained_raw_bytes - memory_bytes) per text type and alphabet size."""
    groups = [
        ("Core grid, random text", dict(experiment="core", text_type="random")),
        ("Core grid, narrative text", dict(experiment="core", text_type="narrative")),
        ("Query pattern (narrative text)", dict(experiment="query_pattern")),
        *[(f"Alphabet size {size}", dict(experiment="alphabet", alphabet_size=size)) for size in config.ALPHABETS],
        ("Positive control", dict(experiment="positive_control")),
    ]
    rows = []
    for label, filters in groups:
        sub = df
        for col, val in filters.items():
            sub = sub[sub[col] == val]
        kmp = sub[sub["algorithm"] == "kmp"]
        ac = sub[sub["algorithm"] == "aho_corasick"]
        if ac.empty:
            continue
        diff = ac["memory_retained_raw_bytes"] - ac["memory_bytes"]
        kdiff = kmp["memory_retained_raw_bytes"] - kmp["memory_bytes"]
        rows.append([
            label, len(ac), fmt_num(kdiff.mean(), 1), fmt_num(ac["memory_retained_raw_bytes"].mean(), 1),
            fmt_num(ac["memory_bytes"].mean(), 1), fmt_num(diff.mean(), 1), fmt_num(diff.max(), 0),
            f"{(diff > 0).mean() * 100:.1f} %",
            fmt_num(100 * diff.sum() / ac["memory_retained_raw_bytes"].sum(), 2) + " %",
        ])
    return (
        "Size of the CPython character-object effect that `memory_bytes` removes: "
        "`memory_retained_raw_bytes − memory_bytes`. It is 0 for KMP by construction.\n\n"
        + md_table(["Group", "AC runs", "KMP mean diff (B)", "AC mean raw (B)", "AC mean memory_bytes (B)",
                    "AC mean diff (B)", "AC max diff (B)", "AC runs affected", "AC diff as % of raw"],
                   rows, ["l", "r", "r", "r", "r", "r", "r", "r", "r"])
    )


def validation_section(df, pilot, machine):
    """Return (markdown, all_passed)."""
    checks = []

    # 1. Row count
    exp_n = expected_rows(pilot)
    checks.append(("Row count", len(df) == exp_n, f"{len(df):,} rows (expected {exp_n:,})"))

    # 2. Each (input, algorithm) exactly once
    dupes = int(df.duplicated(subset=["input_id", "algorithm"]).sum())
    checks.append(("Each (input_id, algorithm) appears once", dupes == 0, f"{dupes} duplicate(s)"))

    # 3. Missing values
    missing = 0
    examples = []
    for row in df.to_dict("records"):
        for col in required_columns(row):
            v = row[col]
            if v is None or (isinstance(v, float) and np.isnan(v)) or v == "":
                missing += 1
                if len(examples) < 3:
                    examples.append(f"input {row['input_id']}/{row['algorithm']}: {col}")
    checks.append(("No missing required values", missing == 0,
                   f"{missing} missing" + (f" (e.g. {'; '.join(examples)})" if examples else "")))

    # 4. Naive memory
    naive = df[df["algorithm"] == "naive"]
    mem_cols = ["memory_bytes", "memory_retained_raw_bytes", "memory_peak_bytes"]
    nonzero = int((naive[mem_cols] != 0).any(axis=1).sum())
    checks.append(("Naive memory is all 0", nonzero == 0,
                   f"{nonzero} row(s) with any non-zero memory column out of {len(naive):,}"))

    # 5. KMP memory follows the LPS sizes
    kmp = df[df["algorithm"] == "kmp"]
    total_q = kmp["query_lengths"].map(lambda s: sum(int(x) for x in str(s).split("|")))
    if len(kmp) > 2 and total_q.std() > 0 and kmp["memory_bytes"].std() > 0:
        r = float(np.corrcoef(total_q, kmp["memory_bytes"])[0, 1])
        slope = float(np.polyfit(total_q, kmp["memory_bytes"], 1)[0])
        checks.append(("KMP memory follows LPS sizes", r >= 0.95,
                       f"Pearson r = {r:.4f} between memory_bytes and total query length "
                       f"(slope ≈ {slope:.2f} bytes per query character: one 8-byte list slot per LPS "
                       "entry, plus a fixed header per table)"))
    else:
        checks.append(("KMP memory follows LPS sizes", False, "not enough KMP rows to compute"))

    # 6. Matches identical across algorithms (re-computed with the clean versions)
    inputs = {rec["input_id"]: rec for rec in load_inputs()}
    csv_counts = {(int(i), a): int(nm) for i, a, nm in zip(df["input_id"], df["algorithm"], df["num_matches"])}
    bad_inputs = []
    for input_id in sorted(set(int(i) for i in df["input_id"])):
        rec = inputs[input_id]
        results = {a: ALGORITHM_MODULES[a].find_all(rec["text"], rec["queries"]) for a in config.ALGORITHMS}
        first = results[config.ALGORITHMS[0]]
        same = all(results[a] == first for a in config.ALGORITHMS)
        counts_ok = all(csv_counts.get((input_id, a), len(first)) == len(first) for a in config.ALGORITHMS)
        if not (same and counts_ok):
            bad_inputs.append(input_id)
    n_inputs = df["input_id"].nunique()
    checks.append(("Matches identical across the 3 algorithms", not bad_inputs,
                   f"{n_inputs:,} inputs re-checked (full match lists compared, and num_matches in the CSV); "
                   f"{len(bad_inputs)} mismatch(es)" + (f": input_ids {bad_inputs[:10]}" if bad_inputs else "")))

    # 7. Memory does not depend on which characters a query uses (see memory_invariance_section)
    inv = memory_invariance(df, inputs)
    inv_ok = all(r["identical"]["memory_bytes"] == r["checked"] for r in inv.values())
    checks.append(("memory_bytes independent of non-Latin-1 characters", inv_ok,
                   "; ".join(f"{config.ALGORITHM_LABELS[a]}: {r['identical']['memory_bytes']:,}/{r['checked']:,} inputs identical"
                             for a, r in inv.items()) + " (details in the memory check below)"))

    # 8. Input hash
    ok, actual, expected = verify_inputs_hash()
    checks.append(("Input hash matches the manifest", ok, f"`{actual}`"))

    # 9. Machine label
    machines = sorted(set(df["machine"]))
    checks.append(("Machine label", machines == [machine], ", ".join(machines)))

    rows = [[name, "✅ PASS" if passed else "❌ FAIL", details] for name, passed, details in checks]
    md = md_table(["Check", "Result", "Details"], rows)
    return md, all(p for _, p, _ in checks), inv


def timing_resolution_section(df, env):
    """Flag timings whose whole timed interval (time × R) is close to the clock resolution."""
    resolution = env.get("perf_counter", {}).get("resolution_s", 1e-7) if env else 1e-7
    threshold = 1000 * resolution  # quantisation error below 0.1 %
    rows = []
    flagged = []
    for algo in config.ALGORITHMS:
        for tr in config.TEXT_LENGTH_RANGES:
            sub = df[(df["algorithm"] == algo) & (df["text_length_range"] == tr)]
            if sub.empty:
                continue
            r = int(sub["repeats"].iloc[0])
            for phase in ("prep_time", "search_time"):
                tmin = float(sub[phase].min())
                tmed = float(sub[phase].median())
                interval = tmin * r
                zeros = int((sub[phase] <= 0).sum())
                suspicious = interval < threshold or zeros > 0
                if suspicious:
                    flagged.append((algo, tr, phase))
                rows.append([
                    config.ALGORITHM_LABELS[algo], range_label(tr), phase.replace("_time", ""), r,
                    fmt_num(tmin * 1e6, 4), fmt_num(tmed * 1e6, 4), fmt_num(interval * 1e6, 2),
                    zeros, "⚠️ yes" if suspicious else "no",
                ])
    md = (
        f"`perf_counter` resolution on this machine: {resolution * 1e9:.0f} ns. A timing is flagged when "
        f"the whole timed interval (min per-call time × R) is below 1,000 × resolution "
        f"(= {threshold * 1e6:.0f} µs), i.e. when clock quantisation could exceed 0.1 %, or when a value is 0.\n\n"
        + md_table(["Algorithm", "Text length", "Phase", "R", "Min per call (µs)", "Median per call (µs)",
                    "Min timed interval (µs)", "Zeros", "Flagged?"],
                   rows, ["l", "l", "l", "r", "r", "r", "r", "r", "c"])
    )
    return md, flagged


def environment_section(env, sessions):
    if not env:
        return "*environment.json not found.*\n"
    last = sessions[-1]["process"] if sessions else {}
    pkgs = ", ".join(f"{k} {v}" for k, v in env["packages"].items())
    freq = env.get("cpu_freq") or {}
    rows = [
        ["Operating system", md_escape(env["os"])],
        ["Platform string", md_escape(env["platform"])],
        ["CPU model", md_escape(env["cpu_model"])],
        ["Cores (physical / logical)", f"{env['physical_cores']} / {env['logical_cores']}"],
        ["CPU frequency as reported by psutil (current / max, MHz)",
         f"{fmt_num(freq.get('current_mhz'), 0)} / {fmt_num(freq.get('max_mhz'), 0)}"],
        ["RAM", f"{env['ram_bytes'] / 2**30:.1f} GiB"],
        ["Python", f"{env['python_implementation']} {env['python_version']}"],
        ["Python build", md_escape(f"{env['python_build']}; {env['python_compiler']}")],
        ["Packages", pkgs],
        ["Timer", f"time.perf_counter ({env['perf_counter']['implementation']}, "
                  f"resolution {env['perf_counter']['resolution_s'] * 1e9:.0f} ns)"],
        ["Pinned core", f"{last.get('pinned_core')} — {'OK' if last.get('pin_ok') else 'FAILED'} "
                        f"({md_escape(last.get('pin_message', ''))})"],
        ["Priority raised", f"{'yes' if last.get('priority_ok') else 'NO'} "
                            f"({md_escape(last.get('priority_message', ''))})"],
    ]
    md = md_table(["Item", "Value"], rows)
    md += "\n" + core_type_section(env)

    if sessions:
        srows = []
        total = 0.0
        for i, s in enumerate(sessions, 1):
            total += s.get("duration_s", 0)
            srows.append([i, s["start_utc"], s.get("end_utc", "—"), fmt_duration(s.get("duration_s", 0)),
                          f"{s.get('jobs_run', 0):,}", "yes" if s.get("interrupted") else "no",
                          "yes" if s["process"].get("priority_ok") else "no"])
        md += "\n**Run sessions** (a resumed run has several):\n\n" + md_table(
            ["Session", "Start (UTC)", "End (UTC)", "Duration", "Jobs run", "Interrupted?", "Priority raised?"],
            srows, ["r", "l", "l", "r", "r", "c", "c"])
        md += f"\nTotal measured duration: **{fmt_duration(total)}**\n"

    warnings = [w for s in sessions for w in s["process"].get("warnings", [])]
    if warnings:
        md += "\n**Warnings:**\n\n" + "\n".join(f"- ⚠️ {md_escape(w)}" for w in dict.fromkeys(warnings)) + "\n"
    return md


def core_type_section(env):
    """Which core type the pinned logical processor belongs to (hybrid CPUs)."""
    info = env.get("core_type")
    if not info:
        return "*Core type: not recorded.*\n"
    md = f"**Pinned core type.** {info['summary']}"
    if info["reliable"]:
        md += f" Detected with: {md_escape(info['method'])}.\n\n"
        md += md_table(["Core type", "Class value", "Logical processors"],
                       [[c["name"], c["class"], ", ".join(str(lp) for lp in c["logical_processors"])]
                        for c in info["classes"]], ["l", "r", "l"])
        if info["pinned_class_is_fastest"] is False:
            md += ("\n⚠️ **The pinned core is not on the fastest core type.** Timings will be slower and "
                   "not comparable with a fast-core run; change `PIN_CORE` in `config.py`.\n")
    else:
        md += "\n"
    freqs = info.get("psutil_max_mhz") or []
    if freqs:
        distinct = sorted(set(freqs))
        md += (f"\npsutil per-core max frequency (MHz): {', '.join(map(str, distinct))}"
               + (" for every core. On Windows psutil only reports the nominal base clock, so this "
                  "cannot tell core types apart." if len(distinct) == 1 else ".") + "\n")
    return md


def write_run_report(machine, pilot):
    out_dir = results_dir(machine, pilot)
    csv_path = out_dir / "raw_runs.csv"
    df = read_raw_runs(csv_path)
    env_path = out_dir / "environment.json"
    env = json.loads(env_path.read_text(encoding="utf-8")) if env_path.exists() else None
    sessions = []
    sessions_path = out_dir / "sessions.jsonl"
    if sessions_path.exists():
        sessions = [json.loads(line) for line in sessions_path.read_text(encoding="utf-8").splitlines() if line]

    validation_md, all_ok, inv = validation_section(df, pilot, machine)
    timing_md, flagged = timing_resolution_section(df, env)

    title = f"# Run report: {machine} machine" + (" (PILOT, 3 runs per condition)" if pilot else "")
    parts = [
        title,
        "",
        f"Generated {utc_now():%Y-%m-%d %H:%M:%S} UTC by `run_benchmark.py`. "
        f"Raw data: `raw_runs.csv` ({len(df):,} rows).",
        "",
        "## Environment",
        "",
        environment_section(env, sessions),
        "## Validation checks",
        "",
        f"Overall: **{'all checks passed ✅' if all_ok else 'some checks FAILED ❌'}**",
        "",
        validation_md,
        "### Memory check: independence from non-Latin-1 characters",
        "",
        memory_invariance_section(inv),
        "### Memory: size of the CPython character-object effect",
        "",
        cpython_effect_section(df),
        "",
        "### Timing resolution check",
        "",
        timing_md,
        "",
    ]
    if flagged:
        parts += [
            f"**{len(flagged)} timing group(s) flagged.** Naive's preprocessing is a no-op, so its prep "
            "time is only function-call overhead and is expected to be near zero; any other flagged group "
            "may need a larger R in `config.REPEATS` (decide before the full run).",
            "",
        ]

    parts += ["## Summary tables", ""]
    for view in FACTOR_VIEWS:
        parts += [f"### {view['title']}", "", f"*{view['pooling'].capitalize()}.*", ""]
        for metric in METRICS:
            parts += [wide_table(df, view, metric), ""]

    parts += [
        "### Positive control",
        "",
        "Text `a`×n, query `a`×(m−1) + `b`: the worst case for Naive. One (n, m) per text-length level, "
        "reused for every run.",
        "",
        positive_control_table(df),
        "",
        "## Appendix: every condition",
        "",
        "All factor levels, not pooled. Units as above: times in µs per call, comparisons as counts, "
        "memory in bytes.",
        "",
        per_condition_table(df),
    ]
    (out_dir / "run_report.md").write_text("\n".join(parts), encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--machine", required=True, choices=config.MACHINES)
    parser.add_argument("--pilot", action="store_true",
                        help=f"{config.PILOT_RUNS} runs per condition, written to results/<machine>/pilot/")
    parser.add_argument("--report-only", action="store_true", help="only rebuild run_report.md from the CSV")
    args = parser.parse_args()

    if args.report_only:
        write_run_report(args.machine, args.pilot)
        print(f"Wrote {(results_dir(args.machine, args.pilot) / 'run_report.md').relative_to(config.ROOT)}")
        return 0
    run(args.machine, args.pilot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
