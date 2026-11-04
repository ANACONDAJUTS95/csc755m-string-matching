# Paper values checklist

Generated 2026-11-04 04:38:54 UTC by `analyze.py`. Tick each item off as you paste it.

> Time and comparisons are divided by text length n before testing because exact lengths vary up to tenfold within each level and are drawn independently for each condition. This normalization was adopted after inspecting the first, unnormalized analysis, which is reported in the appendix.

## Seeds

- [ ] `GENERATION_SEED` = **755** (input generation)
- [ ] `ORDER_SEED` = **2026** (run-order shuffle)

## Repeat counts R (repeat-and-divide)

| Text length | R |
| --- | ---: |
| 10–100 | 10,000 |
| 100–1000 | 1,000 |
| 1000–10000 | 100 |

## Text source

- [ ] \|Σ\| = **74**
- [ ] Alice download date: **2026-11-03 04:01:40 UTC**
- [ ] Clean text length: **143,127** characters (raw: 167,712)
- [ ] alice_clean.txt SHA-256: `1d59d565fe460faead044bd47eb19214388b495f1dbb90e3491bad8f6e695974`
- [ ] alice_raw.txt SHA-256: `01b38ea4c710a84bc18d0bd41271a5a1a92b94e97b2812f4dece97d4a694725e`

## Inputs

- [ ] inputs.jsonl SHA-256: `578618582b5aff0ab3cbf18e11be7bbb8bea207c1f1a9b41bf0129ba0ba67cb6`
- [ ] Input instances: **1,710** (each shared by the 3 algorithms)

## Machine specifications

|  | Primary machine | Replication machine |
| --- | --- | --- |
| **Role** | Primary | Replication |
| **Model** | TODO | Dell Inspiron 7501 |
| **CPU** | AMD Ryzen AI 9 HX 370 w/ Radeon 890M | (not yet run) |
| **Cores** | 12 physical / 24 logical | (not yet run) |
| **RAM** | 32 GB (31.1 GiB usable) | (not yet run) |
| **OS** | Windows 11 (Core, build 10.0.26300) | (not yet run) |
| **Python version** | CPython 3.12.13 | (not yet run) |
| **Pinned core** | Logical core 2: Zen 5 core | (not yet run) |

## Software and machine details (primary)

| Item | Value |
| --- | --- |
| OS | Windows 11 (Core, build 10.0.26300) |
| CPU | AMD Ryzen AI 9 HX 370 w/ Radeon 890M |
| Cores (physical / logical) | 12 / 24 |
| RAM | 31.1 GiB |
| Python | CPython 3.12.13 (main Mar 10 2026 18:15:39) |
| Packages | numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, matplotlib 3.11.2, psutil 7.2.2, pytest 9.2.0 |
| Timer resolution | 100 ns |
| Pinned core | core 2 (OK) |
| Priority raised | yes (HIGH_PRIORITY_CLASS) |
| Total benchmark duration | 5.9 min |

## Software and machine (replication)

| Item | Value |
| --- | --- |
| (not available) |  |

## Row counts

- [ ] Primary rows: **5,130** (expected 5,130)
- [ ] Replication rows: (not yet run)

| Algorithm | Primary rows |
| --- | ---: |
| Naive | 1,710 |
| KMP | 1,710 |
| Aho-Corasick | 1,710 |

| Experiment | Primary rows |
| --- | ---: |
| core | 3,240 |
| query_pattern | 540 |
| alphabet | 1,080 |
| positive_control | 270 |

## Statistics

- [ ] Tests: **81** (Holm family size 81, α = 0.05)
- [ ] Dependent variables: time = total time ÷ text length (ns per text character); comparisons = (prep + search comparisons) ÷ text length (comparisons per text character); memory = `memory_bytes` (bytes)
- [ ] Rejected after Holm: **36**; not applicable: **0**
- [ ] Appendix (unnormalized time and comparisons, separate Holm family of 81): rejected **20**; not applicable: **0**
- [ ] Effect-size labels: Cohen's d small 0.2 / medium 0.5 / large 0.8 (Cohen, 1988); η² small 0.01 / medium 0.06 / large 0.14 (Cohen, 1988); Cliff's δ negligible < 0.11 / small < 0.28 / medium < 0.43 / large otherwise; ε² = H/(N − 1) small 0.01 / medium 0.06 / large 0.14

## Memory definitions

All three values come from `tracemalloc` around the preprocessing build, after subtracting the measuring code's own fixed overhead (measured with an empty build).

- **Naive:** builds nothing, so `memory_bytes = memory_retained_raw_bytes = memory_peak_bytes = 0`.
- **KMP:** `memory_bytes` = `memory_retained_raw_bytes` = tracemalloc current − baseline after all LPS tables are built, with the tables still alive (the lists holding the LPS values).
- **Aho-Corasick:** `memory_retained_raw_bytes` = tracemalloc current − baseline after the automaton is built, with it still alive. `memory_bytes` = that value minus the size (`sys.getsizeof`, each object counted once by `id()`) of every trie key string with code point > 255, i.e. the trie structure only: nodes, child dicts, failure links and output lists.
- **All algorithms:** `memory_peak_bytes` = tracemalloc peak − baseline during the build (also counts short-lived temporaries). Descriptive only.
- The memory hypotheses (H0-3, H0-6, H0-9, H0-12) are tested on `memory_bytes`.

## Comparison-counting definitions

- **Naive:** `prep = 0`. During the search, every check of `text[i + j] == pattern[j]` counts 1.
- **KMP:** `prep` is every character comparison made while building the LPS table. `search` is every `text[i] == pattern[j]` check, including the re-checks after a fallback via the LPS table.
- **Aho-Corasick:** the trie uses `dict` children, a failure link, and an output list per node, with failure links built breadth-first.
  - `prep` counts 1 for every child lookup while inserting keywords, plus every child lookup or failure-link step while building the failure links.
  - `search` counts 1 for every **attempted goto transition**, meaning every check of whether the current node has a child for the current character, including the failed attempts that lead to following a failure link.
  - Following the failure link itself is counted separately as `search_failure_steps`; record it in its own column.
