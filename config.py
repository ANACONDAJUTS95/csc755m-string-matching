"""Every experimental constant lives here, in one place.

Why one file? So that the paper, the code and the reports can never disagree:
every script imports its numbers from here instead of hard-coding them.
Changing anything in this file changes the experiment, so treat it as frozen
once the full benchmark has started.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Folders and files (pathlib keeps this identical on Windows and Linux)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
INPUTS_DIR = ROOT / "inputs"
RESULTS_DIR = ROOT / "results"
TRACES_DIR = ROOT / "traces"

ALICE_URL = "https://www.gutenberg.org/cache/epub/11/pg11.txt"
ALICE_RAW = DATA_DIR / "alice_raw.txt"
ALICE_CLEAN = DATA_DIR / "alice_clean.txt"
ALICE_INFO_MD = DATA_DIR / "alice_info.md"
ALICE_META_JSON = DATA_DIR / "alice_meta.json"  # machine-readable copy of alice_info.md
GUTENBERG_START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK"
GUTENBERG_END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK"

INPUTS_FILE = INPUTS_DIR / "inputs.jsonl"
MANIFEST_FILE = INPUTS_DIR / "manifest.md"

MACHINES = ("primary", "replication")

# ---------------------------------------------------------------------------
# Seeds (each use creates its own random.Random(seed); the global `random`
# module is never used, so nothing else can disturb the sequence)
# ---------------------------------------------------------------------------
GENERATION_SEED = 755  # input generation
ORDER_SEED = 2026  # shuffling the (input, algorithm) job order

# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------
ALGORITHMS = ("naive", "kmp", "aho_corasick")
ALGORITHM_LABELS = {"naive": "Naive", "kmp": "KMP", "aho_corasick": "Aho-Corasick"}

# ---------------------------------------------------------------------------
# Experimental design
# ---------------------------------------------------------------------------
NUM_RUNS = 30  # runs per condition in the full benchmark
PILOT_RUNS = 3  # runs per condition in the --pilot benchmark

# Lengths are drawn uniformly as integers, inclusive at both ends.
TEXT_LENGTH_RANGES = {
    "10-100": (10, 100),
    "100-1000": (100, 1000),
    "1000-10000": (1000, 10000),
}
QUERY_LENGTH_RANGES = {
    "1-5": (1, 5),
    "5-10": (5, 10),
    "10-20": (10, 20),
}

# 1. Core grid
TEXT_TYPES = ("random", "narrative")
NUM_QUERIES_LEVELS = (1, 5)

# 2-4. The other experiments all use a single query of length 5-10.
FIXED_QUERY_RANGE = "5-10"

# 2. Query-pattern experiment
QUERY_STYLES = ("distinct", "repeating")
REPEAT_UNIT_LENGTH = (1, 3)  # length of the repeated unit, inclusive

# 3. Alphabet-size experiment. None means "the full Alice character set".
ALPHABETS = {
    "2": "ab",
    "4": "abcd",
    "26": "abcdefghijklmnopqrstuvwxyz",
    "full": None,
}

# 4. Positive control: text "a" * n, query "a" * (m - 1) + "b"
CONTROL_TEXT_CHAR = "a"
CONTROL_LAST_QUERY_CHAR = "b"

EXPERIMENTS = ("core", "query_pattern", "alphabet", "positive_control")

# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------
# Repeat-and-divide: each timed operation runs R times inside one timer and the
# elapsed time is divided by R. Shorter texts need more repeats so the timed
# interval stays well above the clock resolution. Same R for prep and search.
REPEATS = {
    "10-100": 10000,
    "100-1000": 1000,
    "1000-10000": 100,
}

PIN_CORE = 2  # avoid core 0, which services most interrupts
LINUX_NICE = -5  # needs root / CAP_SYS_NICE; a warning is logged otherwise

PROGRESS_EVERY = 100  # print a progress line every N jobs

# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
ALPHA = 0.05
EXPECTED_TESTS = 81

# ---------------------------------------------------------------------------
# Raw results CSV columns (order matters: this is the file header)
# ---------------------------------------------------------------------------
CSV_COLUMNS = [
    "experiment",
    "algorithm",
    "text_type",
    "alphabet_size",
    "text_length_range",
    "text_length",
    "query_length_range",
    "query_lengths",
    "query_style",
    "num_queries",
    "run_id",
    "input_id",
    "machine",
    "repeats",
    "prep_time",
    "search_time",
    "total_time",
    "prep_comparisons",
    "search_comparisons",
    "search_failure_steps",
    "memory_bytes",  # structure only (tested): raw minus AC's non-Latin-1 key objects
    "memory_retained_raw_bytes",  # current - baseline after the build (descriptive only)
    "memory_peak_bytes",  # peak during preprocessing, incl. temporaries (descriptive only)
    "num_matches",
    "order_index",
]

# ---------------------------------------------------------------------------
# Memory definitions (used by README.md, paper_values.md and stats_report.md)
# ---------------------------------------------------------------------------
MEMORY_DEFINITIONS = """\
All three values come from `tracemalloc` around the preprocessing build, after subtracting the measuring code's own fixed overhead (measured with an empty build).

- **Naive:** builds nothing, so `memory_bytes = memory_retained_raw_bytes = memory_peak_bytes = 0`.
- **KMP:** `memory_bytes` = `memory_retained_raw_bytes` = tracemalloc current − baseline after all LPS tables are built, with the tables still alive (the lists holding the LPS values).
- **Aho-Corasick:** `memory_retained_raw_bytes` = tracemalloc current − baseline after the automaton is built, with it still alive. `memory_bytes` = that value minus the size (`sys.getsizeof`, each object counted once by `id()`) of every trie key string with code point > 255, i.e. the trie structure only: nodes, child dicts, failure links and output lists.
- **All algorithms:** `memory_peak_bytes` = tracemalloc peak − baseline during the build (also counts short-lived temporaries). Descriptive only.
- The memory hypotheses (H0-3, H0-6, H0-9, H0-12) are tested on `memory_bytes`."""


# ---------------------------------------------------------------------------
# Comparison-counting definitions, word for word as they appear in the paper.
# Reproduced in README.md and results/primary/paper_values.md.
# ---------------------------------------------------------------------------
COMPARISON_DEFINITIONS = """\
- **Naive:** `prep = 0`. During the search, every check of `text[i + j] == pattern[j]` counts 1.
- **KMP:** `prep` is every character comparison made while building the LPS table. `search` is every `text[i] == pattern[j]` check, including the re-checks after a fallback via the LPS table.
- **Aho-Corasick:** the trie uses `dict` children, a failure link, and an output list per node, with failure links built breadth-first.
  - `prep` counts 1 for every child lookup while inserting keywords, plus every child lookup or failure-link step while building the failure links.
  - `search` counts 1 for every **attempted goto transition**, meaning every check of whether the current node has a child for the current character, including the failed attempts that lead to following a failure link.
  - Following the failure link itself is counted separately as `search_failure_steps`; record it in its own column."""
