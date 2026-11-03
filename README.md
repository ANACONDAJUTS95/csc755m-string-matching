# String-matching benchmark: Naive vs. KMP vs. Aho-Corasick

CSC755M MCO1, Milestone 3. This project measures **time**, **character comparisons** and **memory** for three
exact string-matching algorithms. It uses fixed seeds and pre-generated inputs, so the run can be repeated
on a second machine and checked against the first.

- Primary machine: Windows 11
- Replication machine: Linux CachyOS (Dell Inspiron 7501, i5-10300H)

Everything is plain Python 3.12. The algorithms use only the standard library.

---

## 1. One-time setup

You need **Python 3.12**. With [uv](https://docs.astral.sh/uv/) installed you can use the uv commands. If you
don't have uv, use the plain-venv commands. Run everything from the project folder.

### Windows (PowerShell)

```powershell
# with uv
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt

# or with plain venv
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Linux / CachyOS (works in bash, zsh and fish)

```bash
# with uv
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt

# or with plain venv
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The commands below call the venv's Python directly, so you never need to "activate" anything:

| | Python command |
|---|---|
| Windows | `.venv\Scripts\python.exe` |
| Linux | `.venv/bin/python` |

In the rest of this file, **`PY`** stands for whichever of these applies to your machine.

---

## 2. Step-by-step

These steps are **already done** on the primary machine. They are listed so you know what each file is for.

| Step | Command | What it does |
|---|---|---|
| 1 | `PY prepare_alice.py` | Downloads Alice (Gutenberg #11), cleans it, writes `data/alice_info.md` (Σ, hashes, date) |
| 2 | `PY -m pytest` | Runs the correctness tests (45 tests) |
| 3 | `PY generate_inputs.py` | Builds the 1,710 shared input instances into `inputs/inputs.jsonl` and writes `inputs/manifest.md`. It refuses to overwrite unless you pass `--force`. **Never regenerate after the benchmark has started.** |
| 4 | `PY run_benchmark.py --machine primary --pilot` | 3-run pilot, written to `results/primary/pilot/` |
| 5 | `PY analyze.py --pilot` | Statistics on the pilot data (proves the pipeline works) |

### The full benchmark (you run this, outside VS Code)

**Primary machine (Windows):**

```powershell
.venv\Scripts\python.exe run_benchmark.py --machine primary
.venv\Scripts\python.exe analyze.py
```

**Replication machine (CachyOS):** first get the project there, *including* `data/` and `inputs/`, for
example via your GitHub repository. Then:

```bash
.venv/bin/python -m pytest
.venv/bin/python run_benchmark.py --machine replication
```

**Back on the primary machine,** once `results/replication/` is copied over:

```powershell
.venv\Scripts\python.exe replicate.py
```

`run_benchmark.py` first checks the SHA-256 of `inputs/inputs.jsonl` against `inputs/manifest.md` and stops if
the two differ. The `.gitattributes` file stops Git from changing line endings in that file, which would
change its hash.

### Resuming

The benchmark writes one CSV row per job and flushes it immediately. If it stops (Ctrl+C, crash, reboot),
run **the same command again**: finished jobs are skipped, and a half-written last row is dropped and
redone. Each session is logged in `sessions.jsonl` and listed in `run_report.md`.

To rebuild only the report from an existing CSV, run `PY run_benchmark.py --machine primary --report-only`.

### For a fair measurement

- Plug the laptop in and use the same power mode on every run (Windows: *Best performance*).
- Close other programs. **Pause OneDrive syncing** during the run: this folder is inside OneDrive, and syncing
  the CSV while it is being written adds background CPU and disk activity.
- The script pins itself to logical core 2 (`PIN_CORE` in `config.py`) and raises its priority
  (Windows: `HIGH_PRIORITY_CLASS`; Linux: `nice -5`). On Linux, raising priority needs root. Without it the
  script logs a warning in `run_report.md` and continues at normal priority. To allow it without running as
  root, add `yourusername - nice -5` to `/etc/security/limits.conf` and log in again.

---

## 3. Experimental design (implemented exactly as in the paper)

All constants are in `config.py`.

| Experiment | Conditions | Factors | Text | Queries |
|---|---|---|---|---|
| Core grid (H0-1 to H0-6) | 108 | 3 algorithms × 2 text types × 3 text lengths × 3 query lengths × 2 query counts | random from Alice Σ, or narrative slice | 1 or 5 random substrings of the text |
| Query pattern (H0-7 to H0-9) | 18 | 2 styles × 3 algorithms × 3 text lengths | narrative | 1 query, length 5–10, letters a–z/A–Z; *distinct* or *repeating* (unit of 1–3 letters) |
| Alphabet size (H0-10 to H0-12) | 36 | 4 alphabets (2, 4, 26, full Σ) × 3 algorithms × 3 text lengths | random from the alphabet | 1 random substring, length 5–10 |
| Positive control | 9 | 3 algorithms × 3 text lengths | `a` × n | `a` × (m−1) + `b` (n, m drawn once, reused for all runs) |

- Text lengths are drawn from 10–100, 100–1000 and 1000–10000, and query lengths from 1–5, 5–10 and 10–20.
  All lengths are uniform integers, inclusive at both ends.
- 30 runs per condition: 171 × 30 = **5,130 rows per machine**.
- **Pairing:** run *i* of a condition uses the same input for all three algorithms (1,710 input instances).
- Seeds: `GENERATION_SEED = 755` (inputs) and `ORDER_SEED = 2026` (the job order is shuffled). Each seed gets
  its own `random.Random` instance.

### Comparison-counting definitions

- **Naive:** `prep = 0`. During the search, every check of `text[i + j] == pattern[j]` counts 1.
- **KMP:** `prep` is every character comparison made while building the LPS table. `search` is every `text[i] == pattern[j]` check, including the re-checks after a fallback via the LPS table.
- **Aho-Corasick:** the trie uses `dict` children, a failure link, and an output list per node, with failure links built breadth-first.
  - `prep` counts 1 for every child lookup while inserting keywords, plus every child lookup or failure-link step while building the failure links.
  - `search` counts 1 for every **attempted goto transition**, meaning every check of whether the current node has a child for the current character, including the failed attempts that lead to following a failure link.
  - Following the failure link itself is counted separately as `search_failure_steps`; record it in its own column.

A useful consequence of these definitions is that Aho-Corasick's `search_comparisons = n + search_failure_steps`
always holds. The tests check this.

The "comparisons" dependent variable in the statistics is `prep_comparisons + search_comparisons`.

### How each job is measured (`src/measure.py`)

Each (input, algorithm) job gets three separate passes on the identical input:

1. **Timing pass** (clean version, no counters). `tracemalloc` is off and `gc` is disabled. The pass makes one
   untimed warm-up call, then times `R` preprocessing calls and `R` search calls with `time.perf_counter()` and
   divides by `R`. R is 10,000 / 1,000 / 100 for the text-length levels 10–100 / 100–1000 / 1000–10000
   (the same R is used for preprocessing).
2. **Count pass** (counted version, run once). Its matches must equal the timing pass's matches, otherwise the
   run stops with an error.
3. **Memory pass.** `tracemalloc` takes a baseline, resets the peak, and builds the preprocessing structures
   (KMP: all LPS tables; Aho-Corasick: one automaton). It records three columns, defined exactly below.

**Why memory is measured this way.** Python stores every character with a code point of 255 or less as one
shared object, but each character above 255 (such as Alice's curly quotes) becomes a separate small string
object, both briefly while it is compared and permanently when Aho-Corasick uses it as a trie key. Random
text uses all 74 Alice characters evenly, while narrative text rarely uses curly quotes, so a measure that
counts these objects could show a false memory difference between text types or alphabets. `memory_bytes`
therefore measures only the structure each algorithm builds (KMP's LPS tables; the trie's nodes, dicts,
failure links and output lists), and the raw retained size and the peak are kept as descriptive columns.

Exact definitions (also in `config.MEMORY_DEFINITIONS` and `paper_values.md`):

- **Naive:** builds nothing, so all three columns are 0.
- **KMP:** `memory_bytes` = `memory_retained_raw_bytes` = tracemalloc current − baseline after all LPS tables
  are built, with the tables still alive.
- **Aho-Corasick:** `memory_retained_raw_bytes` = current − baseline after the automaton is built, with it still
  alive. `memory_bytes` = that value minus `sys.getsizeof` of every trie key string with code point > 255
  (each object counted once, de-duplicated by `id()`).
- **All:** `memory_peak_bytes` = peak − baseline during the build. The measuring code's own fixed overhead
  (measured with an empty build) is subtracted from every column.

With several queries, Naive and KMP process each query in turn, so their times and comparisons are sums over
the queries. Aho-Corasick builds one automaton and scans the text once.

---

## 4. Outputs

| File | Contents |
|---|---|
| `data/alice_info.md` | Download date, character counts, SHA-256 of raw and clean text, full Σ with counts |
| `inputs/manifest.md` | Input hash, seeds, counts, length sanity tables, redraws, duplicate queries |
| `results/<machine>/raw_runs.csv` | One row per job (5,130), including `memory_bytes`, `memory_retained_raw_bytes` and `memory_peak_bytes`. Blank = not applicable |
| `results/<machine>/run_report.md` | Environment (incl. the pinned core's type), validation checks, memory check, timing-resolution check, summary tables |
| `results/<machine>/environment.json`, `sessions.jsonl` | Machine details and run sessions (used by the reports) |
| `results/primary/stats_report.md` | H0-1 … H0-12: decisions summary, one section per hypothesis, descriptive results, figures |
| `results/primary/figures/*.png` | Figures 5.2a–5.5c (a = time, b = comparisons, c = memory) |
| `results/primary/paper_values.md` | Checklist of every number to paste into the paper |
| `results/replication_report.md` | Primary vs. replication: hashes, identical counts, Table 5.8 winners, time ratios |
| `traces/*.md` | Step-by-step algorithm traces |

### Traces (for the qualitative section)

```bash
PY trace.py --algorithm naive --text "hello world" --queries "wor"
PY trace.py --algorithm kmp --text "ABABCABABA" --queries "ABABA"
PY trace.py --algorithm aho_corasick --text "ushers" --queries he --queries she --queries his --queries hers
```

Each trace checks itself against the benchmark's counted version and refuses to write if they disagree.
Use `--name myfile` to choose the output name.

---

## 5. Statistics (`analyze.py`)

- α = 0.05. Each test is run per algorithm and per text-length level.
- Shapiro-Wilk is run on each group. With two groups the test is Welch's t-test if every group is normal,
  otherwise Mann-Whitney U (two-sided). With four groups it is one-way ANOVA if every group is normal,
  otherwise Kruskal-Wallis.
- Effect sizes: Cohen's d (Welch; small 0.2 / medium 0.5 / large 0.8, Cohen, 1988), Cliff's δ (Mann-Whitney;
  0.11 / 0.28 / 0.43), η² (ANOVA; 0.01 / 0.06 / 0.14, Cohen, 1988), and ε² = H/(N − 1) (Kruskal-Wallis;
  0.01 / 0.06 / 0.14).
- Memory tests (H0-3, H0-6, H0-9, H0-12) use `memory_bytes` (structure only).
- There are 81 tests in total, with Holm's correction applied across all 81 as one family.
- Memory hypotheses (H0-3, H0-9, H0-12) are tested only for KMP and Aho-Corasick. H0-4 to H0-6 are tested only
  for Aho-Corasick.

---

## 6. Implementation choices to be aware of

These follow the design but fill in details it did not spell out:

1. **Redraw rule with 5 queries.** If *any* of the 5 drawn query lengths is longer than the drawn text length,
   the text length **and all 5** query lengths are drawn again. With the current seed this happens 8 times,
   all in the 10–100 text / 10–20 query cell.
2. **Sorting matches** (to return a sorted list) happens inside `search()` for all three algorithms, so it
   is included in search time equally for each.
3. **Naive preprocessing time** is measured too. Naive's `preprocess()` is a no-op, so its prep time
   (about 0.05 µs) is pure function-call overhead.
4. **Memory of non-Latin-1 queries.** `run_report.md` checks that `memory_bytes` is identical for queries
   with the same lengths and character structure, whether or not they contain non-Latin-1 characters, for both
   KMP and Aho-Corasick. It also reports, per text type and alphabet size, how large the removed CPython
   character-object effect is (`memory_retained_raw_bytes − memory_bytes`).
5. **Effect-size labels for d and η²** follow Cohen (1988): d 0.2 / 0.5 / 0.8 and η² 0.01 / 0.06 / 0.14.
6. **"Not applicable" tests** (every value identical) stay in the Holm family of 81. They are ranked last,
   as if p = 1, and are never counted as rejections.
7. In the CSV, `text_type` is blank for the positive control and `alphabet_size` is filled only in the
   alphabet experiment, following the "blank when it does not apply" rule.

---

## 7. Project layout

```
config.py            every constant (seeds, ranges, R, alphabets, pinned core)
prepare_alice.py     download + clean Alice
generate_inputs.py   build inputs once, hash them
run_benchmark.py     run one machine (resumable)
analyze.py           statistics on the primary results
replicate.py         primary vs. replication
trace.py             Markdown step-by-step traces
src/naive.py  src/kmp.py  src/aho_corasick.py   the algorithms (clean + counted versions)
src/measure.py       timing, counting, memory, CPU pinning, environment info
src/report.py        Markdown helpers;  src/summaries.py  shared summary tables
src/inputs_io.py     hashing and file loading
tests/test_algorithms.py
```
