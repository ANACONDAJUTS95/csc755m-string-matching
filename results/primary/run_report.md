# Run report: primary machine

Generated 2026-11-04 04:04:29 UTC by `run_benchmark.py`. Raw data: `raw_runs.csv` (5,130 rows).

## Environment

| Item | Value |
| --- | --- |
| Operating system | Windows 11 (Core, build 10.0.26300) |
| Platform string | Windows-11-10.0.26300-SP0 |
| CPU model | AMD Ryzen AI 9 HX 370 w/ Radeon 890M |
| Cores (physical / logical) | 12 / 24 |
| CPU frequency as reported by psutil (current / max, MHz) | 2,000 / 2,000 |
| RAM | 31.1 GiB |
| Python | CPython 3.12.13 |
| Python build | main Mar 10 2026 18:15:39; MSC v.1944 64 bit (AMD64) |
| Packages | numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, matplotlib 3.11.2, psutil 7.2.2, pytest 9.2.0 |
| Timer | time.perf_counter (QueryPerformanceCounter(), resolution 100 ns) |
| Pinned core | 2 — OK (cpu_affinity set to [2]) |
| Priority raised | yes (HIGH_PRIORITY_CLASS) |

**Pinned core type.** Logical core 2 is a **Zen 5** core. Detected with: Windows GetSystemCpuSetInformation EfficiencyClass (higher = faster core type).

| Core type | Class value | Logical processors |
| --- | ---: | --- |
| Zen 5 | 1 | 0, 1, 2, 3, 4, 5, 6, 7 |
| Zen 5c | 0 | 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 |

psutil per-core max frequency (MHz): 2000 for every core. On Windows psutil only reports the nominal base clock, so this cannot tell core types apart.

**Run sessions** (a resumed run has several):

| Session | Start (UTC) | End (UTC) | Duration | Jobs run | Interrupted? | Priority raised? |
| ---: | --- | --- | ---: | ---: | :---: | :---: |
| 1 | 2026-11-04T03:55:27+00:00 | 2026-11-04T04:01:24+00:00 | 5m 57s | 5,130 | no | yes |

Total measured duration: **5m 57s**

## Validation checks

Overall: **all checks passed ✅**

| Check | Result | Details |
| --- | --- | --- |
| Row count | ✅ PASS | 5,130 rows (expected 5,130) |
| Each (input_id, algorithm) appears once | ✅ PASS | 0 duplicate(s) |
| No missing required values | ✅ PASS | 0 missing |
| Naive memory is all 0 | ✅ PASS | 0 row(s) with any non-zero memory column out of 1,710 |
| KMP memory follows LPS sizes | ✅ PASS | Pearson r = 0.9564 between memory_bytes and total query length (slope ≈ 12.03 bytes per query character: one 8-byte list slot per LPS entry, plus a fixed header per table) |
| Matches identical across the 3 algorithms | ✅ PASS | 1,710 inputs re-checked (full match lists compared, and num_matches in the CSV); 0 mismatch(es) |
| memory_bytes independent of non-Latin-1 characters | ✅ PASS | KMP: 1,710/1,710 inputs identical; Aho-Corasick: 1,710/1,710 inputs identical (details in the memory check below) |
| Input hash matches the manifest | ✅ PASS | `578618582b5aff0ab3cbf18e11be7bbb8bea207c1f1a9b41bf0129ba0ba67cb6` |
| Machine label | ✅ PASS | primary |

### Memory check: independence from non-Latin-1 characters

Every input's queries are measured three times: as generated, renamed to printable ASCII (inside Latin-1), and renamed to Cyrillic (outside Latin-1). The renaming keeps the lengths and the character structure (which positions hold equal characters, within and across queries), so the LPS tables and the trie have exactly the same shape. `memory_bytes` (the tested measure) must be identical for all three versions; the two descriptive columns are shown for comparison.

| Algorithm | Inputs checked | Inputs with non-Latin-1 chars | memory_bytes identical (tested) | memory_retained_raw_bytes identical | memory_peak_bytes identical | CSV values reproduced (all 3 columns) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| KMP | 1,710 | 538 | ✅ 1,710 / 1,710 (max diff 0 B) | 1,710 / 1,710 (max diff 0 B) | 46 / 1,710 (max diff 88 B) | 1,710 / 1,710 |
| Aho-Corasick | 1,710 | 538 | ✅ 1,710 / 1,710 (max diff 0 B) | 0 / 1,710 (max diff 5,460 B) | 0 / 1,710 (max diff 5,460 B) | 1,710 / 1,710 |


*Why the raw retained size differs for Aho-Corasick:* the trie's `dict` keys are the character objects themselves. CPython shares one cached object per character with code point ≤ 255, but every character above 255 (e.g. Alice's curly quotes) is a separate 60-byte string object kept alive by the trie. `memory_bytes` subtracts those objects (`sys.getsizeof`, each object once), leaving the trie's structure only.


### Memory: size of the CPython character-object effect

Size of the CPython character-object effect that `memory_bytes` removes: `memory_retained_raw_bytes − memory_bytes`. It is 0 for KMP by construction.

| Group | AC runs | KMP mean diff (B) | AC mean raw (B) | AC mean memory_bytes (B) | AC mean diff (B) | AC max diff (B) | AC runs affected | AC diff as % of raw |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Core grid, random text | 540 | 0.0 | 7,257.8 | 7,154.1 | 103.8 | 960 | 61.9 % | 1.43 % |
| Core grid, narrative text | 540 | 0.0 | 7,042.5 | 7,009.9 | 32.7 | 360 | 31.3 % | 0.46 % |
| Query pattern (narrative text) | 180 | 0.0 | 2,666.9 | 2,666.9 | 0.0 | 0 | 0.0 % | 0.00 % |
| Alphabet size 2 | 90 | 0.0 | 2,595.7 | 2,595.7 | 0.0 | 0 | 0.0 % | 0.00 % |
| Alphabet size 4 | 90 | 0.0 | 2,665.1 | 2,665.1 | 0.0 | 0 | 0.0 % | 0.00 % |
| Alphabet size 26 | 90 | 0.0 | 2,773.9 | 2,773.9 | 0.0 | 0 | 0.0 % | 0.00 % |
| Alphabet size full | 90 | 0.0 | 2,592.4 | 2,563.7 | 28.7 | 180 | 38.9 % | 1.11 % |
| Positive control | 90 | 0.0 | 2,528.0 | 2,528.0 | 0.0 | 0 | 0.0 % | 0.00 % |


### Timing resolution check

`perf_counter` resolution on this machine: 100 ns. A timing is flagged when the whole timed interval (min per-call time × R) is below 1,000 × resolution (= 100 µs), i.e. when clock quantisation could exceed 0.1 %, or when a value is 0.

| Algorithm | Text length | Phase | R | Min per call (µs) | Median per call (µs) | Min timed interval (µs) | Zeros | Flagged? |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| Naive | 10–100 | prep | 10000 | 0.0214 | 0.0223 | 214.20 | 0 | no |
| Naive | 10–100 | search | 10000 | 0.2763 | 3.5026 | 2,762.70 | 0 | no |
| Naive | 100–1000 | prep | 1000 | 0.0209 | 0.0219 | 20.90 | 0 | ⚠️ yes |
| Naive | 100–1000 | search | 1000 | 4.0687 | 37.1707 | 4,068.70 | 0 | no |
| Naive | 1000–10000 | prep | 100 | 0.0190 | 0.0260 | 1.90 | 0 | ⚠️ yes |
| Naive | 1000–10000 | search | 100 | 45.1180 | 436.0655 | 4,511.80 | 0 | no |
| KMP | 10–100 | prep | 10000 | 0.1338 | 0.5449 | 1,338.20 | 0 | no |
| KMP | 10–100 | search | 10000 | 0.4548 | 3.1270 | 4,548.00 | 0 | no |
| KMP | 100–1000 | prep | 1000 | 0.1347 | 0.5409 | 134.70 | 0 | no |
| KMP | 100–1000 | search | 1000 | 3.5277 | 30.6423 | 3,527.70 | 0 | no |
| KMP | 1000–10000 | prep | 100 | 0.1400 | 0.5160 | 14.00 | 0 | ⚠️ yes |
| KMP | 1000–10000 | search | 100 | 34.6670 | 317.2475 | 3,466.70 | 0 | no |
| Aho-Corasick | 10–100 | prep | 10000 | 0.5599 | 2.3387 | 5,599.10 | 0 | no |
| Aho-Corasick | 10–100 | search | 10000 | 0.5867 | 3.2949 | 5,866.50 | 0 | no |
| Aho-Corasick | 100–1000 | prep | 1000 | 0.5464 | 2.2477 | 546.40 | 0 | no |
| Aho-Corasick | 100–1000 | search | 1000 | 5.1098 | 32.4150 | 5,109.80 | 0 | no |
| Aho-Corasick | 1000–10000 | prep | 100 | 0.5980 | 2.3435 | 59.80 | 0 | ⚠️ yes |
| Aho-Corasick | 1000–10000 | search | 100 | 53.9870 | 324.0760 | 5,398.70 | 0 | no |


**4 timing group(s) flagged.** Naive's preprocessing is a no-op, so its prep time is only function-call overhead and is expected to be near zero; any other flagged group may need a larger R in `config.REPEATS` (decide before the full run).

## Summary tables

### Core grid: random vs. narrative text

*Pooled over the 3 query lengths and both query counts.*

**Total time (prep + search)** (µs per call)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 7.43 ± 6.30<br>Mdn 4.11, IQR 10.16 | 7.51 ± 6.36<br>Mdn 4.10, IQR 10.42 |
| Naive | 100–1000 | 79.53 ± 71.19<br>Mdn 40.41, IQR 108.14 | 78.55 ± 73.69<br>Mdn 42.36, IQR 106.95 |
| Naive | 1000–10000 | 876.06 ± 744.85<br>Mdn 481.50, IQR 1,141.89 | 852.16 ± 755.76<br>Mdn 491.66, IQR 988.31 |
| KMP | 10–100 | 7.84 ± 6.42<br>Mdn 4.20, IQR 10.59 | 7.96 ± 6.30<br>Mdn 4.62, IQR 11.31 |
| KMP | 100–1000 | 66.98 ± 58.83<br>Mdn 34.47, IQR 92.85 | 66.66 ± 60.91<br>Mdn 37.02, IQR 88.87 |
| KMP | 1000–10000 | 694.06 ± 589.10<br>Mdn 378.59, IQR 917.98 | 684.71 ± 605.22<br>Mdn 409.06, IQR 812.96 |
| Aho-Corasick | 10–100 | 8.86 ± 5.76<br>Mdn 6.70, IQR 7.11 | 8.79 ± 5.24<br>Mdn 6.84, IQR 7.59 |
| Aho-Corasick | 100–1000 | 38.97 ± 18.05<br>Mdn 39.49, IQR 27.82 | 38.41 ± 19.12<br>Mdn 36.07, IQR 28.94 |
| Aho-Corasick | 1000–10000 | 358.82 ± 161.60<br>Mdn 360.03, IQR 251.89 | 349.46 ± 175.50<br>Mdn 360.81, IQR 292.85 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 |
| Naive | 100–1000 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.003<br>Mdn 0.022, IQR 0.001 |
| Naive | 1000–10000 | 0.025 ± 0.007<br>Mdn 0.026, IQR 0.005 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.005 |
| KMP | 10–100 | 1.249 ± 1.094<br>Mdn 0.851, IQR 1.358 | 1.258 ± 1.106<br>Mdn 0.815, IQR 1.431 |
| KMP | 100–1000 | 1.259 ± 1.115<br>Mdn 0.855, IQR 1.450 | 1.252 ± 1.105<br>Mdn 0.810, IQR 1.349 |
| KMP | 1000–10000 | 1.259 ± 1.101<br>Mdn 0.819, IQR 1.455 | 1.259 ± 1.108<br>Mdn 0.811, IQR 1.384 |
| Aho-Corasick | 10–100 | 5.604 ± 5.150<br>Mdn 3.540, IQR 6.127 | 5.433 ± 4.909<br>Mdn 3.302, IQR 6.202 |
| Aho-Corasick | 100–1000 | 5.946 ± 5.672<br>Mdn 3.442, IQR 6.792 | 5.760 ± 5.448<br>Mdn 3.443, IQR 5.864 |
| Aho-Corasick | 1000–10000 | 6.004 ± 5.608<br>Mdn 3.661, IQR 6.722 | 5.966 ± 5.680<br>Mdn 3.464, IQR 6.305 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Search time** (µs per call)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 7.41 ± 6.30<br>Mdn 4.09, IQR 10.16 | 7.48 ± 6.36<br>Mdn 4.08, IQR 10.41 |
| Naive | 100–1000 | 79.51 ± 71.19<br>Mdn 40.38, IQR 108.14 | 78.52 ± 73.69<br>Mdn 42.33, IQR 106.95 |
| Naive | 1000–10000 | 876.03 ± 744.85<br>Mdn 481.48, IQR 1,141.89 | 852.14 ± 755.76<br>Mdn 491.64, IQR 988.31 |
| KMP | 10–100 | 6.59 ± 5.59<br>Mdn 3.58, IQR 9.19 | 6.70 ± 5.63<br>Mdn 3.79, IQR 9.38 |
| KMP | 100–1000 | 65.72 ± 58.14<br>Mdn 33.52, IQR 90.01 | 65.41 ± 60.30<br>Mdn 35.61, IQR 87.58 |
| KMP | 1000–10000 | 692.80 ± 588.43<br>Mdn 378.06, IQR 917.78 | 683.45 ± 604.57<br>Mdn 408.76, IQR 811.27 |
| Aho-Corasick | 10–100 | 3.26 ± 1.41<br>Mdn 3.11, IQR 2.15 | 3.36 ± 1.51<br>Mdn 3.35, IQR 2.50 |
| Aho-Corasick | 100–1000 | 33.02 ± 16.02<br>Mdn 33.33, IQR 27.45 | 32.65 ± 17.48<br>Mdn 30.94, IQR 27.87 |
| Aho-Corasick | 1000–10000 | 352.81 ± 160.43<br>Mdn 355.67, IQR 250.61 | 343.50 ± 174.65<br>Mdn 354.46, IQR 288.53 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Comparisons (prep + search)** (count)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 174.4 ± 151.5<br>Mdn 97.0, IQR 236.2 | 181.2 ± 157.6<br>Mdn 98.5, IQR 254.5 |
| Naive | 100–1000 | 1,738.5 ± 1,513.0<br>Mdn 880.5, IQR 2,370.5 | 1,761.8 ± 1,595.6<br>Mdn 998.0, IQR 2,404.2 |
| Naive | 1000–10000 | 17,846.4 ± 15,071.2<br>Mdn 9,832.0, IQR 23,779.8 | 17,714.5 ± 15,610.6<br>Mdn 10,207.0, IQR 21,071.8 |
| KMP | 10–100 | 197.0 ± 167.4<br>Mdn 104.5, IQR 270.8 | 203.3 ± 168.5<br>Mdn 116.5, IQR 292.5 |
| KMP | 100–1000 | 1,761.5 ± 1,526.5<br>Mdn 905.0, IQR 2,412.8 | 1,766.0 ± 1,591.6<br>Mdn 997.5, IQR 2,384.5 |
| KMP | 1000–10000 | 17,866.1 ± 15,081.4<br>Mdn 9,842.0, IQR 23,767.0 | 17,545.3 ± 15,448.2<br>Mdn 10,057.5, IQR 20,992.8 |
| Aho-Corasick | 10–100 | 108.6 ± 61.5<br>Mdn 89.0, IQR 74.0 | 117.5 ± 62.7<br>Mdn 103.0, IQR 84.5 |
| Aho-Corasick | 100–1000 | 638.0 ± 279.7<br>Mdn 651.0, IQR 478.8 | 684.9 ± 340.2<br>Mdn 651.0, IQR 531.0 |
| Aho-Corasick | 1000–10000 | 6,133.9 ± 2,689.2<br>Mdn 6,248.0, IQR 4,652.8 | 6,548.6 ± 3,287.6<br>Mdn 6,621.5, IQR 5,887.0 |

*Units: count. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Memory, structure only (memory_bytes, tested)** (bytes)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 531 ± 300<br>Mdn 444, IQR 488 | 532 ± 301<br>Mdn 448, IQR 492 |
| KMP | 100–1000 | 536 ± 309<br>Mdn 444, IQR 506 | 530 ± 302<br>Mdn 436, IQR 474 |
| KMP | 1000–10000 | 533 ± 304<br>Mdn 448, IQR 504 | 533 ± 307<br>Mdn 440, IQR 488 |
| Aho-Corasick | 10–100 | 6,916 ± 6,153<br>Mdn 4,284, IQR 7,026 | 6,784 ± 5,980<br>Mdn 4,036, IQR 7,312 |
| Aho-Corasick | 100–1000 | 7,309 ± 6,694<br>Mdn 4,192, IQR 7,864 | 7,078 ± 6,430<br>Mdn 4,272, IQR 6,724 |
| Aho-Corasick | 1000–10000 | 7,237 ± 6,547<br>Mdn 4,192, IQR 7,888 | 7,168 ± 6,604<br>Mdn 4,272, IQR 7,096 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Memory, raw retained size (descriptive only)** (bytes)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 531 ± 300<br>Mdn 444, IQR 488 | 532 ± 301<br>Mdn 448, IQR 492 |
| KMP | 100–1000 | 536 ± 309<br>Mdn 444, IQR 506 | 530 ± 302<br>Mdn 436, IQR 474 |
| KMP | 1000–10000 | 533 ± 304<br>Mdn 448, IQR 504 | 533 ± 307<br>Mdn 440, IQR 488 |
| Aho-Corasick | 10–100 | 7,029 ± 6,271<br>Mdn 4,404, IQR 7,239 | 6,810 ± 6,006<br>Mdn 4,036, IQR 7,312 |
| Aho-Corasick | 100–1000 | 7,408 ± 6,790<br>Mdn 4,282, IQR 7,909 | 7,112 ± 6,460<br>Mdn 4,322, IQR 6,724 |
| Aho-Corasick | 1000–10000 | 7,337 ± 6,648<br>Mdn 4,282, IQR 7,903 | 7,206 ± 6,643<br>Mdn 4,272, IQR 7,171 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Peak memory during preprocessing (descriptive only)** (bytes)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 593 ± 303<br>Mdn 520, IQR 497 | 583 ± 302<br>Mdn 510, IQR 496 |
| KMP | 100–1000 | 597 ± 313<br>Mdn 506, IQR 508 | 583 ± 304<br>Mdn 516, IQR 480 |
| KMP | 1000–10000 | 593 ± 307<br>Mdn 510, IQR 505 | 586 ± 309<br>Mdn 490, IQR 488 |
| Aho-Corasick | 10–100 | 7,853 ± 6,415<br>Mdn 5,164, IQR 7,239 | 7,629 ± 6,136<br>Mdn 4,796, IQR 7,312 |
| Aho-Corasick | 100–1000 | 8,247 ± 6,954<br>Mdn 5,042, IQR 7,909 | 7,948 ± 6,621<br>Mdn 5,082, IQR 6,724 |
| Aho-Corasick | 1000–10000 | 8,170 ± 6,801<br>Mdn 5,042, IQR 7,903 | 8,042 ± 6,804<br>Mdn 5,032, IQR 7,171 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


### Core grid: 1 vs. 5 queries

*Pooled over both text types and the 3 query lengths.*

**Total time (prep + search)** (µs per call)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 2.45 ± 1.03<br>Mdn 2.50, IQR 1.62 | 12.49 ± 5.33<br>Mdn 12.92, IQR 9.11 |
| Naive | 100–1000 | 25.09 ± 13.25<br>Mdn 24.71, IQR 23.45 | 132.99 ± 66.85<br>Mdn 131.47, IQR 118.73 |
| Naive | 1000–10000 | 288.99 ± 144.32<br>Mdn 309.79, IQR 255.76 | 1,439.23 ± 663.48<br>Mdn 1,405.72, IQR 1,181.54 |
| KMP | 10–100 | 2.64 ± 0.95<br>Mdn 2.68, IQR 1.34 | 13.16 ± 4.93<br>Mdn 13.81, IQR 8.54 |
| KMP | 100–1000 | 21.29 ± 10.64<br>Mdn 21.17, IQR 18.70 | 112.35 ± 53.74<br>Mdn 111.87, IQR 96.10 |
| KMP | 1000–10000 | 230.37 ± 114.90<br>Mdn 244.06, IQR 203.56 | 1,148.41 ± 525.76<br>Mdn 1,121.23, IQR 946.40 |
| Aho-Corasick | 10–100 | 5.07 ± 1.70<br>Mdn 5.03, IQR 2.40 | 12.59 ± 5.40<br>Mdn 12.21, IQR 8.04 |
| Aho-Corasick | 100–1000 | 30.75 ± 14.35<br>Mdn 30.47, IQR 25.31 | 46.63 ± 18.94<br>Mdn 47.50, IQR 32.38 |
| Aho-Corasick | 1000–10000 | 315.64 ± 154.09<br>Mdn 338.63, IQR 293.18 | 392.64 ± 173.88<br>Mdn 380.06, IQR 307.87 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 |
| Naive | 100–1000 | 0.022 ± 0.003<br>Mdn 0.022, IQR 0.001 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 |
| Naive | 1000–10000 | 0.026 ± 0.007<br>Mdn 0.026, IQR 0.005 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.005 |
| KMP | 10–100 | 0.458 ± 0.228<br>Mdn 0.427, IQR 0.364 | 2.050 ± 1.046<br>Mdn 1.846, IQR 2.107 |
| KMP | 100–1000 | 0.452 ± 0.224<br>Mdn 0.438, IQR 0.341 | 2.059 ± 1.057<br>Mdn 1.826, IQR 2.162 |
| KMP | 1000–10000 | 0.451 ± 0.220<br>Mdn 0.433, IQR 0.312 | 2.067 ± 1.039<br>Mdn 1.849, IQR 2.041 |
| Aho-Corasick | 10–100 | 2.134 ± 1.127<br>Mdn 1.954, IQR 1.728 | 8.903 ± 5.131<br>Mdn 8.110, IQR 9.973 |
| Aho-Corasick | 100–1000 | 2.088 ± 1.071<br>Mdn 1.998, IQR 1.553 | 9.618 ± 5.676<br>Mdn 8.176, IQR 11.523 |
| Aho-Corasick | 1000–10000 | 2.140 ± 1.091<br>Mdn 2.011, IQR 1.526 | 9.831 ± 5.725<br>Mdn 8.535, IQR 11.324 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Search time** (µs per call)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 2.43 ± 1.03<br>Mdn 2.48, IQR 1.62 | 12.47 ± 5.33<br>Mdn 12.90, IQR 9.11 |
| Naive | 100–1000 | 25.06 ± 13.25<br>Mdn 24.69, IQR 23.45 | 132.97 ± 66.85<br>Mdn 131.45, IQR 118.73 |
| Naive | 1000–10000 | 288.96 ± 144.32<br>Mdn 309.77, IQR 255.76 | 1,439.21 ± 663.48<br>Mdn 1,405.70, IQR 1,181.54 |
| KMP | 10–100 | 2.18 ± 0.91<br>Mdn 2.21, IQR 1.43 | 11.12 ± 4.70<br>Mdn 11.61, IQR 8.34 |
| KMP | 100–1000 | 20.83 ± 10.63<br>Mdn 20.64, IQR 18.73 | 110.29 ± 53.65<br>Mdn 109.48, IQR 95.82 |
| KMP | 1000–10000 | 229.92 ± 114.90<br>Mdn 243.37, IQR 203.79 | 1,146.34 ± 525.67<br>Mdn 1,118.94, IQR 943.53 |
| Aho-Corasick | 10–100 | 2.93 ± 1.26<br>Mdn 2.94, IQR 1.93 | 3.69 ± 1.54<br>Mdn 3.62, IQR 2.52 |
| Aho-Corasick | 100–1000 | 28.67 ± 14.29<br>Mdn 28.78, IQR 25.33 | 37.01 ± 17.97<br>Mdn 36.78, IQR 32.04 |
| Aho-Corasick | 1000–10000 | 313.50 ± 154.08<br>Mdn 335.97, IQR 292.98 | 382.81 ± 173.58<br>Mdn 373.84, IQR 302.96 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Comparisons (prep + search)** (count)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 57.0 ± 26.1<br>Mdn 57.0, IQR 39.2 | 298.6 ± 133.3<br>Mdn 310.5, IQR 230.2 |
| Naive | 100–1000 | 558.8 ± 273.3<br>Mdn 549.5, IQR 473.2 | 2,941.5 ± 1,380.7<br>Mdn 2,937.0, IQR 2,418.0 |
| Naive | 1000–10000 | 5,970.5 ± 2,950.1<br>Mdn 6,313.0, IQR 5,203.0 | 29,590.4 ± 13,476.9<br>Mdn 28,891.0, IQR 24,146.2 |
| KMP | 10–100 | 64.7 ± 26.8<br>Mdn 68.0, IQR 38.0 | 335.6 ± 137.1<br>Mdn 349.0, IQR 242.0 |
| KMP | 100–1000 | 563.5 ± 271.8<br>Mdn 552.0, IQR 470.8 | 2,964.0 ± 1,375.7<br>Mdn 2,971.0, IQR 2,430.2 |
| KMP | 1000–10000 | 5,944.3 ± 2,928.0<br>Mdn 6,292.0, IQR 5,192.8 | 29,467.2 ± 13,392.7<br>Mdn 28,801.5, IQR 23,777.8 |
| Aho-Corasick | 10–100 | 74.7 ± 28.9<br>Mdn 75.0, IQR 43.0 | 151.4 ± 62.9<br>Mdn 148.5, IQR 100.8 |
| Aho-Corasick | 100–1000 | 575.4 ± 272.4<br>Mdn 572.5, IQR 470.8 | 747.5 ± 325.6<br>Mdn 764.0, IQR 548.8 |
| Aho-Corasick | 1000–10000 | 5,971.2 ± 2,935.5<br>Mdn 6,335.0, IQR 5,225.2 | 6,711.4 ± 3,038.8<br>Mdn 6,632.5, IQR 5,152.2 |

*Units: count. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Memory, structure only (memory_bytes, tested)** (bytes)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 269 ± 44<br>Mdn 264, IQR 72 | 794 ± 201<br>Mdn 752, IQR 410 |
| KMP | 100–1000 | 267 ± 42<br>Mdn 264, IQR 64 | 799 ± 207<br>Mdn 744, IQR 434 |
| KMP | 1000–10000 | 267 ± 43<br>Mdn 260, IQR 64 | 799 ± 205<br>Mdn 752, IQR 404 |
| Aho-Corasick | 10–100 | 2,923 ± 1,469<br>Mdn 2,832, IQR 2,352 | 10,777 ± 6,361<br>Mdn 9,808, IQR 12,358 |
| Aho-Corasick | 100–1000 | 2,867 ± 1,398<br>Mdn 2,832, IQR 2,112 | 11,520 ± 6,826<br>Mdn 9,808, IQR 14,030 |
| Aho-Corasick | 1000–10000 | 2,849 ± 1,420<br>Mdn 2,616, IQR 2,112 | 11,556 ± 6,808<br>Mdn 10,048, IQR 13,608 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Memory, raw retained size (descriptive only)** (bytes)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 269 ± 44<br>Mdn 264, IQR 72 | 794 ± 201<br>Mdn 752, IQR 410 |
| KMP | 100–1000 | 267 ± 42<br>Mdn 264, IQR 64 | 799 ± 207<br>Mdn 744, IQR 434 |
| KMP | 1000–10000 | 267 ± 43<br>Mdn 260, IQR 64 | 799 ± 205<br>Mdn 752, IQR 404 |
| Aho-Corasick | 10–100 | 2,949 ± 1,486<br>Mdn 2,832, IQR 2,352 | 10,890 ± 6,443<br>Mdn 9,842, IQR 12,444 |
| Aho-Corasick | 100–1000 | 2,889 ± 1,414<br>Mdn 2,832, IQR 2,112 | 11,631 ± 6,888<br>Mdn 9,928, IQR 14,103 |
| Aho-Corasick | 1000–10000 | 2,868 ± 1,434<br>Mdn 2,676, IQR 2,112 | 11,674 ± 6,876<br>Mdn 10,168, IQR 13,803 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Peak memory during preprocessing (descriptive only)** (bytes)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 326 ± 50<br>Mdn 316, IQR 73 | 851 ± 206<br>Mdn 812, IQR 414 |
| KMP | 100–1000 | 324 ± 51<br>Mdn 312, IQR 77 | 856 ± 212<br>Mdn 810, IQR 440 |
| KMP | 1000–10000 | 323 ± 49<br>Mdn 312, IQR 68 | 856 ± 210<br>Mdn 808, IQR 423 |
| Aho-Corasick | 10–100 | 3,709 ± 1,486<br>Mdn 3,592, IQR 2,352 | 11,773 ± 6,628<br>Mdn 10,602, IQR 12,444 |
| Aho-Corasick | 100–1000 | 3,649 ± 1,414<br>Mdn 3,592, IQR 2,112 | 12,547 ± 7,102<br>Mdn 10,688, IQR 14,631 |
| Aho-Corasick | 1000–10000 | 3,628 ± 1,434<br>Mdn 3,436, IQR 2,112 | 12,584 ± 7,084<br>Mdn 10,928, IQR 14,331 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


### Query-pattern experiment: distinct vs. repeating

*Narrative text, one query of length 5–10.*

**Total time (prep + search)** (µs per call)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 1.99 ± 1.03<br>Mdn 1.97, IQR 1.65 | 2.13 ± 1.05<br>Mdn 2.11, IQR 1.63 |
| Naive | 100–1000 | 22.01 ± 11.81<br>Mdn 19.74, IQR 14.31 | 22.77 ± 11.81<br>Mdn 22.37, IQR 21.36 |
| Naive | 1000–10000 | 233.89 ± 136.13<br>Mdn 271.75, IQR 223.96 | 292.09 ± 114.42<br>Mdn 312.72, IQR 157.87 |
| KMP | 10–100 | 2.30 ± 0.88<br>Mdn 2.25, IQR 1.62 | 2.43 ± 0.91<br>Mdn 2.28, IQR 1.21 |
| KMP | 100–1000 | 18.35 ± 9.17<br>Mdn 16.31, IQR 11.40 | 19.22 ± 9.38<br>Mdn 18.93, IQR 16.29 |
| KMP | 1000–10000 | 183.86 ± 106.35<br>Mdn 214.15, IQR 175.42 | 228.93 ± 89.22<br>Mdn 244.04, IQR 130.40 |
| Aho-Corasick | 10–100 | 4.53 ± 1.24<br>Mdn 4.66, IQR 2.15 | 4.76 ± 1.28<br>Mdn 4.79, IQR 2.21 |
| Aho-Corasick | 100–1000 | 27.48 ± 12.94<br>Mdn 24.80, IQR 14.01 | 28.28 ± 12.83<br>Mdn 27.96, IQR 22.69 |
| Aho-Corasick | 1000–10000 | 261.37 ± 151.24<br>Mdn 296.53, IQR 246.84 | 321.77 ± 124.52<br>Mdn 340.54, IQR 171.46 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 |
| Naive | 100–1000 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 |
| Naive | 1000–10000 | 0.026 ± 0.003<br>Mdn 0.026, IQR 0.007 | 0.026 ± 0.003<br>Mdn 0.027, IQR 0.003 |
| KMP | 10–100 | 0.408 ± 0.060<br>Mdn 0.422, IQR 0.076 | 0.415 ± 0.054<br>Mdn 0.430, IQR 0.085 |
| KMP | 100–1000 | 0.401 ± 0.080<br>Mdn 0.406, IQR 0.094 | 0.416 ± 0.056<br>Mdn 0.430, IQR 0.084 |
| KMP | 1000–10000 | 0.409 ± 0.068<br>Mdn 0.426, IQR 0.110 | 0.385 ± 0.061<br>Mdn 0.367, IQR 0.113 |
| Aho-Corasick | 10–100 | 1.929 ± 0.317<br>Mdn 1.981, IQR 0.427 | 1.967 ± 0.318<br>Mdn 2.040, IQR 0.529 |
| Aho-Corasick | 100–1000 | 1.831 ± 0.308<br>Mdn 1.834, IQR 0.469 | 1.925 ± 0.311<br>Mdn 1.942, IQR 0.537 |
| Aho-Corasick | 1000–10000 | 1.983 ± 0.409<br>Mdn 2.059, IQR 0.719 | 1.803 ± 0.335<br>Mdn 1.689, IQR 0.656 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Search time** (µs per call)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 1.97 ± 1.03<br>Mdn 1.95, IQR 1.65 | 2.10 ± 1.05<br>Mdn 2.09, IQR 1.63 |
| Naive | 100–1000 | 21.98 ± 11.81<br>Mdn 19.72, IQR 14.31 | 22.75 ± 11.81<br>Mdn 22.34, IQR 21.36 |
| Naive | 1000–10000 | 233.87 ± 136.13<br>Mdn 271.73, IQR 223.96 | 292.07 ± 114.42<br>Mdn 312.70, IQR 157.87 |
| KMP | 10–100 | 1.89 ± 0.89<br>Mdn 1.84, IQR 1.56 | 2.01 ± 0.91<br>Mdn 1.88, IQR 1.27 |
| KMP | 100–1000 | 17.95 ± 9.16<br>Mdn 15.98, IQR 11.43 | 18.80 ± 9.38<br>Mdn 18.48, IQR 16.27 |
| KMP | 1000–10000 | 183.45 ± 106.34<br>Mdn 213.77, IQR 175.37 | 228.54 ± 89.21<br>Mdn 243.65, IQR 130.50 |
| Aho-Corasick | 10–100 | 2.60 ± 1.23<br>Mdn 2.63, IQR 2.13 | 2.79 ± 1.26<br>Mdn 2.68, IQR 1.87 |
| Aho-Corasick | 100–1000 | 25.65 ± 12.92<br>Mdn 23.25, IQR 14.22 | 26.36 ± 12.87<br>Mdn 25.85, IQR 22.85 |
| Aho-Corasick | 1000–10000 | 259.39 ± 151.19<br>Mdn 294.64, IQR 246.58 | 319.97 ± 124.45<br>Mdn 339.02, IQR 171.96 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Comparisons (prep + search)** (count)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 46.2 ± 26.6<br>Mdn 45.0, IQR 42.5 | 49.5 ± 27.2<br>Mdn 48.0, IQR 40.2 |
| Naive | 100–1000 | 504.7 ± 248.8<br>Mdn 462.0, IQR 312.2 | 520.7 ± 253.2<br>Mdn 513.0, IQR 439.0 |
| Naive | 1000–10000 | 4,951.7 ± 2,845.3<br>Mdn 5,745.0, IQR 4,720.0 | 6,151.2 ± 2,393.6<br>Mdn 6,598.5, IQR 3,332.5 |
| KMP | 10–100 | 59.7 ± 26.4<br>Mdn 59.0, IQR 46.8 | 63.9 ± 27.1<br>Mdn 60.0, IQR 35.5 |
| KMP | 100–1000 | 517.3 ± 248.9<br>Mdn 472.0, IQR 310.8 | 534.6 ± 252.5<br>Mdn 528.5, IQR 438.5 |
| KMP | 1000–10000 | 4,965.0 ± 2,845.8<br>Mdn 5,756.0, IQR 4,722.0 | 6,160.2 ± 2,392.4<br>Mdn 6,591.5, IQR 3,315.0 |
| Aho-Corasick | 10–100 | 67.5 ± 26.4<br>Mdn 68.0, IQR 47.0 | 72.0 ± 27.2<br>Mdn 70.0, IQR 37.2 |
| Aho-Corasick | 100–1000 | 524.7 ± 249.1<br>Mdn 478.0, IQR 310.0 | 542.7 ± 252.4<br>Mdn 537.5, IQR 436.8 |
| Aho-Corasick | 1000–10000 | 4,972.7 ± 2,846.1<br>Mdn 5,762.5, IQR 4,723.0 | 6,167.3 ± 2,392.8<br>Mdn 6,596.5, IQR 3,312.2 |

*Units: count. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Memory, structure only (memory_bytes, tested)** (bytes)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 262 ± 13<br>Mdn 264, IQR 16 | 265 ± 13<br>Mdn 268, IQR 22 |
| KMP | 100–1000 | 259 ± 12<br>Mdn 260, IQR 20 | 264 ± 13<br>Mdn 264, IQR 22 |
| KMP | 1000–10000 | 262 ± 15<br>Mdn 264, IQR 24 | 257 ± 15<br>Mdn 252, IQR 30 |
| Aho-Corasick | 10–100 | 2,691 ± 468<br>Mdn 2,832, IQR 672 | 2,808 ± 471<br>Mdn 2,952, IQR 852 |
| Aho-Corasick | 100–1000 | 2,576 ± 450<br>Mdn 2,616, IQR 792 | 2,763 ± 464<br>Mdn 2,832, IQR 852 |
| Aho-Corasick | 1000–10000 | 2,670 ± 554<br>Mdn 2,832, IQR 912 | 2,493 ± 526<br>Mdn 2,280, IQR 1,092 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Memory, raw retained size (descriptive only)** (bytes)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 262 ± 13<br>Mdn 264, IQR 16 | 265 ± 13<br>Mdn 268, IQR 22 |
| KMP | 100–1000 | 259 ± 12<br>Mdn 260, IQR 20 | 264 ± 13<br>Mdn 264, IQR 22 |
| KMP | 1000–10000 | 262 ± 15<br>Mdn 264, IQR 24 | 257 ± 15<br>Mdn 252, IQR 30 |
| Aho-Corasick | 10–100 | 2,691 ± 468<br>Mdn 2,832, IQR 672 | 2,808 ± 471<br>Mdn 2,952, IQR 852 |
| Aho-Corasick | 100–1000 | 2,576 ± 450<br>Mdn 2,616, IQR 792 | 2,763 ± 464<br>Mdn 2,832, IQR 852 |
| Aho-Corasick | 1000–10000 | 2,670 ± 554<br>Mdn 2,832, IQR 912 | 2,493 ± 526<br>Mdn 2,280, IQR 1,092 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Peak memory during preprocessing (descriptive only)** (bytes)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 310 ± 13<br>Mdn 312, IQR 16 | 313 ± 13<br>Mdn 316, IQR 22 |
| KMP | 100–1000 | 307 ± 12<br>Mdn 308, IQR 20 | 312 ± 13<br>Mdn 312, IQR 22 |
| KMP | 1000–10000 | 310 ± 15<br>Mdn 312, IQR 24 | 305 ± 15<br>Mdn 300, IQR 30 |
| Aho-Corasick | 10–100 | 3,451 ± 468<br>Mdn 3,592, IQR 672 | 3,568 ± 471<br>Mdn 3,712, IQR 852 |
| Aho-Corasick | 100–1000 | 3,336 ± 450<br>Mdn 3,376, IQR 792 | 3,523 ± 464<br>Mdn 3,592, IQR 852 |
| Aho-Corasick | 1000–10000 | 3,430 ± 554<br>Mdn 3,592, IQR 912 | 3,253 ± 526<br>Mdn 3,040, IQR 1,092 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


### Alphabet-size experiment

*Random text, one query of length 5–10.*

**Total time (prep + search)** (µs per call)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 4.05 ± 1.88<br>Mdn 3.96, IQR 3.12 | 3.14 ± 1.30<br>Mdn 3.39, IQR 1.64 | 2.83 ± 1.01<br>Mdn 2.94, IQR 1.37 | 2.16 ± 0.95<br>Mdn 2.27, IQR 1.25 |
| Naive | 100–1000 | 54.17 ± 25.81<br>Mdn 58.52, IQR 49.58 | 28.71 ± 15.64<br>Mdn 27.93, IQR 20.08 | 21.92 ± 12.08<br>Mdn 20.14, IQR 22.61 | 26.05 ± 13.48<br>Mdn 26.23, IQR 26.32 |
| Naive | 1000–10000 | 567.93 ± 257.50<br>Mdn 646.73, IQR 448.92 | 379.16 ± 171.86<br>Mdn 387.54, IQR 330.73 | 283.38 ± 128.40<br>Mdn 267.45, IQR 230.71 | 249.38 ± 116.01<br>Mdn 232.93, IQR 142.69 |
| KMP | 10–100 | 3.58 ± 1.34<br>Mdn 3.65, IQR 2.10 | 3.28 ± 1.17<br>Mdn 3.45, IQR 1.32 | 2.93 ± 0.89<br>Mdn 3.04, IQR 1.26 | 2.31 ± 0.83<br>Mdn 2.35, IQR 1.08 |
| KMP | 100–1000 | 37.45 ± 16.64<br>Mdn 39.34, IQR 30.38 | 24.32 ± 12.42<br>Mdn 23.69, IQR 15.77 | 18.76 ± 9.73<br>Mdn 17.44, IQR 17.47 | 21.90 ± 10.77<br>Mdn 21.91, IQR 20.19 |
| KMP | 1000–10000 | 368.00 ± 163.67<br>Mdn 422.49, IQR 281.10 | 299.12 ± 134.91<br>Mdn 301.28, IQR 254.88 | 226.90 ± 101.77<br>Mdn 215.02, IQR 183.46 | 196.17 ± 89.58<br>Mdn 182.47, IQR 116.42 |
| Aho-Corasick | 10–100 | 5.35 ± 1.56<br>Mdn 5.22, IQR 2.26 | 5.29 ± 1.38<br>Mdn 5.25, IQR 1.70 | 5.45 ± 1.29<br>Mdn 5.69, IQR 1.68 | 4.41 ± 1.20<br>Mdn 4.28, IQR 1.73 |
| Aho-Corasick | 100–1000 | 43.03 ± 18.46<br>Mdn 46.25, IQR 34.51 | 30.70 ± 14.96<br>Mdn 30.25, IQR 18.63 | 27.02 ± 13.08<br>Mdn 25.04, IQR 22.51 | 31.87 ± 14.91<br>Mdn 32.57, IQR 27.24 |
| Aho-Corasick | 1000–10000 | 407.51 ± 180.62<br>Mdn 460.93, IQR 315.28 | 358.56 ± 161.25<br>Mdn 365.32, IQR 305.77 | 309.03 ± 136.88<br>Mdn 293.29, IQR 242.77 | 273.37 ± 122.83<br>Mdn 248.07, IQR 160.68 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 0.023 ± 0.002<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 |
| Naive | 100–1000 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.001 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 |
| Naive | 1000–10000 | 0.024 ± 0.003<br>Mdn 0.025, IQR 0.005 | 0.026 ± 0.003<br>Mdn 0.027, IQR 0.003 | 0.025 ± 0.003<br>Mdn 0.025, IQR 0.006 | 0.026 ± 0.002<br>Mdn 0.026, IQR 0.001 |
| KMP | 10–100 | 0.486 ± 0.128<br>Mdn 0.479, IQR 0.244 | 0.456 ± 0.086<br>Mdn 0.465, IQR 0.124 | 0.446 ± 0.067<br>Mdn 0.462, IQR 0.095 | 0.401 ± 0.084<br>Mdn 0.394, IQR 0.138 |
| KMP | 100–1000 | 0.469 ± 0.125<br>Mdn 0.494, IQR 0.226 | 0.478 ± 0.090<br>Mdn 0.482, IQR 0.110 | 0.425 ± 0.075<br>Mdn 0.444, IQR 0.093 | 0.405 ± 0.073<br>Mdn 0.421, IQR 0.120 |
| KMP | 1000–10000 | 0.538 ± 0.101<br>Mdn 0.552, IQR 0.120 | 0.494 ± 0.110<br>Mdn 0.525, IQR 0.168 | 0.427 ± 0.064<br>Mdn 0.442, IQR 0.085 | 0.423 ± 0.077<br>Mdn 0.400, IQR 0.126 |
| Aho-Corasick | 10–100 | 1.883 ± 0.429<br>Mdn 1.790, IQR 0.869 | 1.910 ± 0.361<br>Mdn 1.831, IQR 0.619 | 2.066 ± 0.311<br>Mdn 2.096, IQR 0.604 | 1.833 ± 0.407<br>Mdn 1.768, IQR 0.729 |
| Aho-Corasick | 100–1000 | 1.832 ± 0.393<br>Mdn 1.813, IQR 0.750 | 1.935 ± 0.339<br>Mdn 1.865, IQR 0.478 | 1.971 ± 0.370<br>Mdn 2.083, IQR 0.600 | 1.859 ± 0.360<br>Mdn 1.924, IQR 0.671 |
| Aho-Corasick | 1000–10000 | 2.103 ± 0.348<br>Mdn 2.164, IQR 0.429 | 2.129 ± 0.419<br>Mdn 2.210, IQR 0.681 | 2.025 ± 0.346<br>Mdn 2.113, IQR 0.580 | 2.010 ± 0.372<br>Mdn 1.922, IQR 0.608 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Search time** (µs per call)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 4.03 ± 1.88<br>Mdn 3.94, IQR 3.12 | 3.11 ± 1.30<br>Mdn 3.36, IQR 1.64 | 2.81 ± 1.01<br>Mdn 2.92, IQR 1.37 | 2.14 ± 0.95<br>Mdn 2.24, IQR 1.25 |
| Naive | 100–1000 | 54.15 ± 25.81<br>Mdn 58.50, IQR 49.58 | 28.69 ± 15.64<br>Mdn 27.91, IQR 20.08 | 21.90 ± 12.08<br>Mdn 20.12, IQR 22.61 | 26.02 ± 13.48<br>Mdn 26.21, IQR 26.32 |
| Naive | 1000–10000 | 567.90 ± 257.50<br>Mdn 646.70, IQR 448.92 | 379.13 ± 171.86<br>Mdn 387.52, IQR 330.73 | 283.36 ± 128.40<br>Mdn 267.43, IQR 230.72 | 249.35 ± 116.01<br>Mdn 232.90, IQR 142.69 |
| KMP | 10–100 | 3.09 ± 1.35<br>Mdn 3.19, IQR 2.13 | 2.83 ± 1.16<br>Mdn 3.05, IQR 1.33 | 2.48 ± 0.88<br>Mdn 2.61, IQR 1.31 | 1.90 ± 0.82<br>Mdn 1.97, IQR 1.10 |
| KMP | 100–1000 | 36.98 ± 16.62<br>Mdn 38.76, IQR 30.17 | 23.85 ± 12.42<br>Mdn 23.23, IQR 15.70 | 18.33 ± 9.72<br>Mdn 17.01, IQR 17.54 | 21.49 ± 10.77<br>Mdn 21.49, IQR 20.37 |
| KMP | 1000–10000 | 367.46 ± 163.68<br>Mdn 421.83, IQR 281.12 | 298.62 ± 134.93<br>Mdn 300.85, IQR 255.04 | 226.47 ± 101.79<br>Mdn 214.58, IQR 183.55 | 195.75 ± 89.58<br>Mdn 182.08, IQR 116.38 |
| Aho-Corasick | 10–100 | 3.46 ± 1.52<br>Mdn 3.43, IQR 2.50 | 3.38 ± 1.38<br>Mdn 3.69, IQR 1.68 | 3.38 ± 1.24<br>Mdn 3.51, IQR 1.69 | 2.57 ± 1.14<br>Mdn 2.68, IQR 1.44 |
| Aho-Corasick | 100–1000 | 41.20 ± 18.37<br>Mdn 44.08, IQR 33.72 | 28.77 ± 14.95<br>Mdn 27.82, IQR 18.31 | 25.05 ± 13.01<br>Mdn 23.07, IQR 22.66 | 30.01 ± 14.90<br>Mdn 30.67, IQR 28.19 |
| Aho-Corasick | 1000–10000 | 405.41 ± 180.61<br>Mdn 458.44, IQR 315.70 | 356.43 ± 161.31<br>Mdn 363.41, IQR 306.07 | 307.00 ± 137.02<br>Mdn 291.22, IQR 243.29 | 271.36 ± 122.82<br>Mdn 246.36, IQR 160.49 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Comparisons (prep + search)** (count)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 98.2 ± 48.3<br>Mdn 95.5, IQR 77.5 | 75.9 ± 33.9<br>Mdn 82.0, IQR 43.2 | 68.9 ± 26.5<br>Mdn 73.0, IQR 37.2 | 48.6 ± 23.2<br>Mdn 51.5, IQR 31.0 |
| Naive | 100–1000 | 1,230.5 ± 550.8<br>Mdn 1,340.5, IQR 1,055.0 | 664.5 ± 337.3<br>Mdn 652.5, IQR 417.0 | 511.8 ± 260.9<br>Mdn 477.5, IQR 472.0 | 574.4 ± 278.5<br>Mdn 584.0, IQR 531.8 |
| Naive | 1000–10000 | 12,077.2 ± 5,416.3<br>Mdn 13,683.5, IQR 9,281.2 | 8,058.1 ± 3,626.2<br>Mdn 8,163.5, IQR 6,950.8 | 6,032.2 ± 2,694.8<br>Mdn 5,733.5, IQR 4,845.8 | 5,046.0 ± 2,259.7<br>Mdn 4,594.0, IQR 2,951.8 |
| KMP | 10–100 | 82.8 ± 33.6<br>Mdn 82.5, IQR 49.5 | 79.0 ± 31.3<br>Mdn 85.0, IQR 37.8 | 76.4 ± 26.6<br>Mdn 80.5, IQR 36.5 | 54.8 ± 23.2<br>Mdn 60.0, IQR 30.8 |
| KMP | 100–1000 | 885.3 ± 382.7<br>Mdn 947.0, IQR 698.5 | 626.5 ± 314.7<br>Mdn 610.0, IQR 397.5 | 518.2 ± 260.4<br>Mdn 484.5, IQR 464.8 | 580.7 ± 278.4<br>Mdn 590.5, IQR 527.0 |
| KMP | 1000–10000 | 8,547.4 ± 3,808.4<br>Mdn 9,899.5, IQR 6,503.2 | 7,515.0 ± 3,375.5<br>Mdn 7,628.5, IQR 6,508.0 | 6,029.5 ± 2,689.3<br>Mdn 5,730.5, IQR 4,834.0 | 5,052.0 ± 2,259.4<br>Mdn 4,600.0, IQR 2,953.8 |
| Aho-Corasick | 10–100 | 93.7 ± 34.1<br>Mdn 92.0, IQR 47.2 | 88.7 ± 31.5<br>Mdn 93.0, IQR 38.2 | 86.1 ± 26.9<br>Mdn 90.0, IQR 36.8 | 63.0 ± 23.4<br>Mdn 66.0, IQR 34.2 |
| Aho-Corasick | 100–1000 | 903.0 ± 384.7<br>Mdn 961.5, IQR 711.0 | 636.6 ± 314.8<br>Mdn 622.5, IQR 399.2 | 527.4 ± 260.8<br>Mdn 494.0, IQR 461.0 | 588.9 ± 278.5<br>Mdn 599.0, IQR 522.2 |
| Aho-Corasick | 1000–10000 | 8,604.4 ± 3,821.0<br>Mdn 9,967.0, IQR 6,583.5 | 7,526.9 ± 3,375.8<br>Mdn 7,638.5, IQR 6,507.5 | 6,038.5 ± 2,688.6<br>Mdn 5,740.0, IQR 4,830.8 | 5,060.7 ± 2,259.4<br>Mdn 4,608.0, IQR 2,954.8 |

*Units: count. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Memory, structure only (memory_bytes, tested)** (bytes)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 258 ± 16<br>Mdn 256, IQR 30 | 260 ± 14<br>Mdn 256, IQR 24 | 267 ± 12<br>Mdn 268, IQR 24 | 257 ± 15<br>Mdn 256, IQR 30 |
| KMP | 100–1000 | 256 ± 14<br>Mdn 256, IQR 30 | 261 ± 12<br>Mdn 256, IQR 16 | 263 ± 15<br>Mdn 268, IQR 22 | 258 ± 14<br>Mdn 260, IQR 30 |
| KMP | 1000–10000 | 263 ± 13<br>Mdn 264, IQR 14 | 264 ± 14<br>Mdn 268, IQR 24 | 262 ± 13<br>Mdn 264, IQR 24 | 261 ± 14<br>Mdn 256, IQR 24 |
| Aho-Corasick | 10–100 | 2,541 ± 560<br>Mdn 2,400, IQR 1,092 | 2,602 ± 509<br>Mdn 2,400, IQR 912 | 2,864 ± 442<br>Mdn 2,952, IQR 912 | 2,496 ± 531<br>Mdn 2,400, IQR 1,092 |
| Aho-Corasick | 100–1000 | 2,490 ± 522<br>Mdn 2,400, IQR 1,092 | 2,626 ± 452<br>Mdn 2,400, IQR 672 | 2,746 ± 523<br>Mdn 2,952, IQR 852 | 2,568 ± 506<br>Mdn 2,616, IQR 1,092 |
| Aho-Corasick | 1000–10000 | 2,757 ± 467<br>Mdn 2,832, IQR 564 | 2,768 ± 503<br>Mdn 2,952, IQR 912 | 2,712 ± 486<br>Mdn 2,832, IQR 912 | 2,627 ± 499<br>Mdn 2,400, IQR 912 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Memory, raw retained size (descriptive only)** (bytes)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 258 ± 16<br>Mdn 256, IQR 30 | 260 ± 14<br>Mdn 256, IQR 24 | 267 ± 12<br>Mdn 268, IQR 24 | 257 ± 15<br>Mdn 256, IQR 30 |
| KMP | 100–1000 | 256 ± 14<br>Mdn 256, IQR 30 | 261 ± 12<br>Mdn 256, IQR 16 | 263 ± 15<br>Mdn 268, IQR 22 | 258 ± 14<br>Mdn 260, IQR 30 |
| KMP | 1000–10000 | 263 ± 13<br>Mdn 264, IQR 14 | 264 ± 14<br>Mdn 268, IQR 24 | 262 ± 13<br>Mdn 264, IQR 24 | 261 ± 14<br>Mdn 256, IQR 24 |
| Aho-Corasick | 10–100 | 2,541 ± 560<br>Mdn 2,400, IQR 1,092 | 2,602 ± 509<br>Mdn 2,400, IQR 912 | 2,864 ± 442<br>Mdn 2,952, IQR 912 | 2,526 ± 549<br>Mdn 2,400, IQR 1,047 |
| Aho-Corasick | 100–1000 | 2,490 ± 522<br>Mdn 2,400, IQR 1,092 | 2,626 ± 452<br>Mdn 2,400, IQR 672 | 2,746 ± 523<br>Mdn 2,952, IQR 852 | 2,596 ± 507<br>Mdn 2,706, IQR 1,047 |
| Aho-Corasick | 1000–10000 | 2,757 ± 467<br>Mdn 2,832, IQR 564 | 2,768 ± 503<br>Mdn 2,952, IQR 912 | 2,712 ± 486<br>Mdn 2,832, IQR 912 | 2,655 ± 513<br>Mdn 2,460, IQR 897 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Peak memory during preprocessing (descriptive only)** (bytes)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 100–1000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| Naive | 1000–10000 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| KMP | 10–100 | 306 ± 16<br>Mdn 304, IQR 30 | 308 ± 14<br>Mdn 304, IQR 24 | 315 ± 12<br>Mdn 316, IQR 24 | 317 ± 24<br>Mdn 316, IQR 34 |
| KMP | 100–1000 | 304 ± 14<br>Mdn 304, IQR 30 | 309 ± 12<br>Mdn 304, IQR 16 | 311 ± 15<br>Mdn 316, IQR 22 | 317 ± 19<br>Mdn 316, IQR 24 |
| KMP | 1000–10000 | 311 ± 13<br>Mdn 312, IQR 14 | 312 ± 14<br>Mdn 316, IQR 24 | 310 ± 13<br>Mdn 312, IQR 24 | 321 ± 26<br>Mdn 318, IQR 27 |
| Aho-Corasick | 10–100 | 3,301 ± 560<br>Mdn 3,160, IQR 1,092 | 3,362 ± 509<br>Mdn 3,160, IQR 912 | 3,624 ± 442<br>Mdn 3,712, IQR 912 | 3,286 ± 549<br>Mdn 3,160, IQR 1,047 |
| Aho-Corasick | 100–1000 | 3,250 ± 522<br>Mdn 3,160, IQR 1,092 | 3,386 ± 452<br>Mdn 3,160, IQR 672 | 3,506 ± 523<br>Mdn 3,712, IQR 852 | 3,356 ± 507<br>Mdn 3,466, IQR 1,047 |
| Aho-Corasick | 1000–10000 | 3,517 ± 467<br>Mdn 3,592, IQR 564 | 3,528 ± 503<br>Mdn 3,712, IQR 912 | 3,472 ± 486<br>Mdn 3,592, IQR 912 | 3,415 ± 513<br>Mdn 3,220, IQR 897 |

*Units: bytes. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


### Positive control

Text `a`×n, query `a`×(m−1) + `b`: the worst case for Naive. One (n, m) per text-length level, reused for every run.

| Text length | n | m | Expected Naive (n−m+1)·m | Naive comparisons | Naive comparisons / char | Naive median time (µs) | KMP comparisons | KMP comparisons / char | KMP median time (µs) | Aho-Corasick comparisons | Aho-Corasick comparisons / char | Aho-Corasick median time (µs) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10–100 | 77 | 8 | 560 | 560 | 7.27 | 17.62 | 160 | 2.08 | 6.17 | 174 | 2.26 | 7.33 |
| 100–1000 | 741 | 8 | 5,872 | 5,872 | 7.92 | 209.14 | 1,488 | 2.01 | 56.38 | 1,502 | 2.03 | 54.82 |
| 1000–10000 | 3,302 | 5 | 16,490 | 16,490 | 4.99 | 648.51 | 6,607 | 2.00 | 253.12 | 6,615 | 2.00 | 238.75 |

*Comparisons = prep + search (identical in every run, so the median equals every value). Comparisons / char = comparisons ÷ n. Time = median total time in µs per call over the runs.*


## Appendix: every condition

All factor levels, not pooled. Units as above: times in µs per call, comparisons as counts, memory in bytes.

| Condition | Algorithm | N | Total time (prep + search) (µs per call) | Preprocessing time (µs per call) | Search time (µs per call) | Comparisons (prep + search) (count) | Memory, structure only (memory_bytes, tested) (bytes) | Memory, raw retained size (descriptive only) (bytes) | Peak memory during preprocessing (descriptive only) (bytes) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| core, random, q 1–5, k=1, n 10–100 | Naive | 30 | 2.42 ± 1.09<br>Mdn 2.45, IQR 1.67 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 2.39 ± 1.09<br>Mdn 2.43, IQR 1.67 | 54.0 ± 27.2<br>Mdn 55.0, IQR 41.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=1, n 10–100 | KMP | 30 | 2.30 ± 0.97<br>Mdn 2.34, IQR 1.57 | 0.214 ± 0.064<br>Mdn 0.216, IQR 0.118 | 2.08 ± 0.96<br>Mdn 2.07, IQR 1.49 | 55.8 ± 27.4<br>Mdn 57.0, IQR 43.8 | 222 ± 12<br>Mdn 224, IQR 22 | 222 ± 12<br>Mdn 224, IQR 22 | 275 ± 18<br>Mdn 272, IQR 28 |
| core, random, q 1–5, k=1, n 10–100 | Aho-Corasick | 30 | 3.82 ± 1.43<br>Mdn 3.92, IQR 2.37 | 0.943 ± 0.296<br>Mdn 0.970, IQR 0.537 | 2.87 ± 1.37<br>Mdn 2.91, IQR 2.07 | 59.6 ± 28.0<br>Mdn 61.0, IQR 44.5 | 1,384 ± 349<br>Mdn 1,440, IQR 660 | 1,398 ± 352<br>Mdn 1,440, IQR 615 | 2,158 ± 352<br>Mdn 2,200, IQR 615 |
| core, random, q 1–5, k=5, n 10–100 | Naive | 30 | 11.11 ± 5.05<br>Mdn 9.72, IQR 5.86 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 11.09 ± 5.05<br>Mdn 9.70, IQR 5.86 | 255.7 ± 124.1<br>Mdn 226.0, IQR 150.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=5, n 10–100 | KMP | 30 | 10.45 ± 4.38<br>Mdn 9.19, IQR 5.41 | 0.922 ± 0.121<br>Mdn 0.899, IQR 0.136 | 9.53 ± 4.39<br>Mdn 8.22, IQR 5.19 | 265.6 ± 124.0<br>Mdn 238.0, IQR 154.5 | 576 ± 21<br>Mdn 572, IQR 24 | 576 ± 21<br>Mdn 572, IQR 24 | 627 ± 24<br>Mdn 624, IQR 39 |
| core, random, q 1–5, k=5, n 10–100 | Aho-Corasick | 30 | 6.89 ± 1.63<br>Mdn 6.78, IQR 2.52 | 3.512 ± 0.603<br>Mdn 3.484, IQR 0.679 | 3.38 ± 1.52<br>Mdn 3.01, IQR 1.62 | 83.6 ± 27.2<br>Mdn 79.0, IQR 39.5 | 4,100 ± 729<br>Mdn 3,956, IQR 920 | 4,158 ± 738<br>Mdn 4,102, IQR 969 | 4,918 ± 738<br>Mdn 4,862, IQR 969 |
| core, random, q 5–10, k=1, n 10–100 | Naive | 30 | 2.43 ± 0.96<br>Mdn 2.43, IQR 1.34 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 2.40 ± 0.96<br>Mdn 2.41, IQR 1.34 | 55.6 ± 23.6<br>Mdn 55.0, IQR 31.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=1, n 10–100 | KMP | 30 | 2.55 ± 0.83<br>Mdn 2.60, IQR 1.06 | 0.417 ± 0.072<br>Mdn 0.426, IQR 0.120 | 2.14 ± 0.83<br>Mdn 2.14, IQR 1.12 | 62.2 ± 23.5<br>Mdn 62.0, IQR 31.5 | 261 ± 14<br>Mdn 264, IQR 24 | 261 ± 14<br>Mdn 264, IQR 24 | 326 ± 30<br>Mdn 322, IQR 36 |
| core, random, q 5–10, k=1, n 10–100 | Aho-Corasick | 30 | 4.88 ± 1.23<br>Mdn 4.81, IQR 1.54 | 1.954 ± 0.376<br>Mdn 2.043, IQR 0.669 | 2.92 ± 1.19<br>Mdn 2.92, IQR 1.58 | 70.9 ± 23.6<br>Mdn 71.5, IQR 30.0 | 2,654 ± 509<br>Mdn 2,832, IQR 912 | 2,692 ± 523<br>Mdn 2,862, IQR 972 | 3,452 ± 523<br>Mdn 3,622, IQR 972 |
| core, random, q 5–10, k=5, n 10–100 | Naive | 30 | 12.18 ± 5.68<br>Mdn 13.04, IQR 8.58 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 12.16 ± 5.68<br>Mdn 13.02, IQR 8.58 | 286.7 ± 138.5<br>Mdn 303.0, IQR 215.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=5, n 10–100 | KMP | 30 | 12.61 ± 4.97<br>Mdn 13.53, IQR 7.52 | 1.827 ± 0.132<br>Mdn 1.789, IQR 0.181 | 10.78 ± 4.94<br>Mdn 11.71, IQR 7.56 | 319.0 ± 139.1<br>Mdn 334.0, IQR 214.8 | 751 ± 27<br>Mdn 752, IQR 44 | 751 ± 27<br>Mdn 752, IQR 44 | 818 ± 40<br>Mdn 820, IQR 44 |
| core, random, q 5–10, k=5, n 10–100 | Aho-Corasick | 30 | 11.58 ± 2.25<br>Mdn 12.04, IQR 3.22 | 8.004 ± 0.999<br>Mdn 8.202, IQR 0.843 | 3.58 ± 1.58<br>Mdn 3.74, IQR 2.31 | 134.3 ± 33.7<br>Mdn 142.0, IQR 50.5 | 9,650 ± 1,329<br>Mdn 9,808, IQR 888 | 9,790 ± 1,355<br>Mdn 10,040, IQR 1,062 | 10,550 ± 1,355<br>Mdn 10,800, IQR 1,062 |
| core, random, q 10–20, k=1, n 10–100 | Naive | 30 | 2.25 ± 0.99<br>Mdn 2.00, IQR 1.69 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 2.23 ± 0.99<br>Mdn 1.97, IQR 1.69 | 52.8 ± 24.7<br>Mdn 47.0, IQR 39.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=1, n 10–100 | KMP | 30 | 2.81 ± 0.88<br>Mdn 2.56, IQR 1.30 | 0.744 ± 0.124<br>Mdn 0.741, IQR 0.206 | 2.07 ± 0.86<br>Mdn 1.83, IQR 1.41 | 67.6 ± 25.0<br>Mdn 62.5, IQR 37.5 | 325 ± 24<br>Mdn 328, IQR 36 | 325 ± 24<br>Mdn 328, IQR 36 | 392 ± 29<br>Mdn 392, IQR 32 |
| core, random, q 10–20, k=1, n 10–100 | Aho-Corasick | 30 | 6.36 ± 1.39<br>Mdn 6.25, IQR 1.80 | 3.581 ± 0.612<br>Mdn 3.649, IQR 0.900 | 2.78 ± 1.23<br>Mdn 2.48, IQR 2.05 | 84.5 ± 25.8<br>Mdn 82.0, IQR 35.0 | 4,787 ± 791<br>Mdn 4,944, IQR 1,272 | 4,867 ± 806<br>Mdn 4,974, IQR 1,242 | 5,627 ± 806<br>Mdn 5,734, IQR 1,242 |
| core, random, q 10–20, k=5, n 10–100 | Naive | 30 | 14.21 ± 4.42<br>Mdn 14.96, IQR 7.61 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 14.19 ± 4.42<br>Mdn 14.94, IQR 7.61 | 341.5 ± 107.2<br>Mdn 366.5, IQR 181.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=5, n 10–100 | KMP | 30 | 16.32 ± 4.04<br>Mdn 16.91, IQR 6.97 | 3.373 ± 0.355<br>Mdn 3.283, IQR 0.506 | 12.94 ± 3.95<br>Mdn 13.80, IQR 7.01 | 411.6 ± 107.8<br>Mdn 430.5, IQR 189.5 | 1,050 ± 59<br>Mdn 1,060, IQR 90 | 1,050 ± 59<br>Mdn 1,060, IQR 90 | 1,119 ± 61<br>Mdn 1,118, IQR 92 |
| core, random, q 10–20, k=5, n 10–100 | Aho-Corasick | 30 | 19.65 ± 3.16<br>Mdn 20.27, IQR 3.58 | 15.629 ± 2.605<br>Mdn 16.307, IQR 2.698 | 4.02 ± 1.20<br>Mdn 4.27, IQR 2.07 | 218.6 ± 32.8<br>Mdn 220.5, IQR 46.8 | 18,922 ± 3,201<br>Mdn 19,492, IQR 3,118 | 19,268 ± 3,293<br>Mdn 19,976, IQR 3,325 | 20,415 ± 3,491<br>Mdn 21,264, IQR 3,591 |
| core, random, q 1–5, k=1, n 100–1000 | Naive | 30 | 24.21 ± 12.11<br>Mdn 24.71, IQR 19.34 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.001 | 24.18 ± 12.11<br>Mdn 24.69, IQR 19.33 | 532.4 ± 244.0<br>Mdn 562.5, IQR 395.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=1, n 100–1000 | KMP | 30 | 20.21 ± 9.79<br>Mdn 20.89, IQR 15.61 | 0.227 ± 0.062<br>Mdn 0.219, IQR 0.087 | 19.98 ± 9.78<br>Mdn 20.56, IQR 15.55 | 534.4 ± 244.3<br>Mdn 566.0, IQR 397.0 | 225 ± 10<br>Mdn 224, IQR 16 | 225 ± 10<br>Mdn 224, IQR 16 | 277 ± 16<br>Mdn 272, IQR 24 |
| core, random, q 1–5, k=1, n 100–1000 | Aho-Corasick | 30 | 29.07 ± 13.36<br>Mdn 30.54, IQR 21.89 | 1.016 ± 0.268<br>Mdn 1.013, IQR 0.420 | 28.05 ± 13.31<br>Mdn 29.10, IQR 21.62 | 539.9 ± 245.4<br>Mdn 572.5, IQR 398.2 | 1,456 ± 308<br>Mdn 1,440, IQR 480 | 1,470 ± 314<br>Mdn 1,440, IQR 480 | 2,230 ± 314<br>Mdn 2,200, IQR 480 |
| core, random, q 1–5, k=5, n 100–1000 | Naive | 30 | 132.17 ± 63.69<br>Mdn 148.48, IQR 106.24 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 132.15 ± 63.69<br>Mdn 148.46, IQR 106.24 | 2,892.8 ± 1,309.7<br>Mdn 3,189.0, IQR 2,177.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=5, n 100–1000 | KMP | 30 | 109.68 ± 50.98<br>Mdn 122.80, IQR 83.44 | 0.945 ± 0.124<br>Mdn 0.925, IQR 0.136 | 108.73 ± 50.97<br>Mdn 122.03, IQR 83.44 | 2,902.8 ± 1,309.8<br>Mdn 3,195.5, IQR 2,183.0 | 579 ± 21<br>Mdn 576, IQR 24 | 579 ± 21<br>Mdn 576, IQR 24 | 634 ± 32<br>Mdn 624, IQR 31 |
| core, random, q 1–5, k=5, n 100–1000 | Aho-Corasick | 30 | 40.94 ± 17.46<br>Mdn 44.08, IQR 29.70 | 3.690 ± 0.573<br>Mdn 3.587, IQR 0.579 | 37.25 ± 17.39<br>Mdn 41.11, IQR 28.41 | 640.6 ± 277.6<br>Mdn 693.0, IQR 468.0 | 4,342 ± 717<br>Mdn 4,192, IQR 852 | 4,408 ± 719<br>Mdn 4,252, IQR 867 | 5,168 ± 719<br>Mdn 5,012, IQR 867 |
| core, random, q 5–10, k=1, n 100–1000 | Naive | 30 | 28.56 ± 12.85<br>Mdn 32.56, IQR 19.74 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 28.54 ± 12.85<br>Mdn 32.54, IQR 19.74 | 626.2 ± 257.6<br>Mdn 723.5, IQR 402.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=1, n 100–1000 | KMP | 30 | 23.84 ± 10.16<br>Mdn 27.53, IQR 15.48 | 0.414 ± 0.063<br>Mdn 0.428, IQR 0.063 | 23.43 ± 10.15<br>Mdn 27.10, IQR 15.37 | 632.7 ± 258.0<br>Mdn 730.5, IQR 405.0 | 260 ± 13<br>Mdn 260, IQR 16 | 260 ± 13<br>Mdn 260, IQR 16 | 315 ± 18<br>Mdn 314, IQR 23 |
| core, random, q 5–10, k=1, n 100–1000 | Aho-Corasick | 30 | 34.60 ± 13.88<br>Mdn 39.95, IQR 22.64 | 1.894 ± 0.333<br>Mdn 1.896, IQR 0.445 | 32.71 ± 13.80<br>Mdn 38.00, IQR 22.17 | 641.2 ± 258.3<br>Mdn 739.0, IQR 407.8 | 2,616 ± 462<br>Mdn 2,616, IQR 672 | 2,638 ± 472<br>Mdn 2,646, IQR 672 | 3,398 ± 472<br>Mdn 3,406, IQR 672 |
| core, random, q 5–10, k=5, n 100–1000 | Naive | 30 | 126.43 ± 59.09<br>Mdn 127.01, IQR 66.10 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 126.41 ± 59.09<br>Mdn 126.98, IQR 66.10 | 2,767.7 ± 1,212.0<br>Mdn 2,823.0, IQR 1,417.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=5, n 100–1000 | KMP | 30 | 106.94 ± 48.06<br>Mdn 107.28, IQR 55.97 | 1.849 ± 0.134<br>Mdn 1.880, IQR 0.178 | 105.09 ± 48.00<br>Mdn 105.37, IQR 55.92 | 2,800.5 ± 1,213.5<br>Mdn 2,857.0, IQR 1,417.0 | 760 ± 29<br>Mdn 768, IQR 38 | 760 ± 29<br>Mdn 768, IQR 38 | 826 ± 38<br>Mdn 824, IQR 43 |
| core, random, q 5–10, k=5, n 100–1000 | Aho-Corasick | 30 | 43.30 ± 16.07<br>Mdn 44.01, IQR 20.19 | 8.527 ± 0.799<br>Mdn 8.727, IQR 1.002 | 34.78 ± 15.72<br>Mdn 34.96, IQR 19.83 | 658.2 ± 259.3<br>Mdn 676.5, IQR 299.5 | 10,324 ± 1,072<br>Mdn 10,528, IQR 1,428 | 10,472 ± 1,077<br>Mdn 10,648, IQR 1,503 | 11,232 ± 1,077<br>Mdn 11,408, IQR 1,503 |
| core, random, q 10–20, k=1, n 100–1000 | Naive | 30 | 22.89 ± 12.83<br>Mdn 23.63, IQR 19.73 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 22.87 ± 12.83<br>Mdn 23.61, IQR 19.73 | 508.9 ± 267.3<br>Mdn 506.0, IQR 381.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=1, n 100–1000 | KMP | 30 | 19.80 ± 10.32<br>Mdn 20.12, IQR 16.89 | 0.689 ± 0.136<br>Mdn 0.657, IQR 0.212 | 19.11 ± 10.32<br>Mdn 19.53, IQR 16.86 | 522.4 ± 267.4<br>Mdn 517.5, IQR 383.8 | 316 ± 29<br>Mdn 312, IQR 62 | 316 ± 29<br>Mdn 312, IQR 62 | 387 ± 35<br>Mdn 390, IQR 53 |
| core, random, q 10–20, k=1, n 100–1000 | Aho-Corasick | 30 | 30.01 ± 14.56<br>Mdn 28.81, IQR 20.45 | 3.301 ± 0.703<br>Mdn 3.202, IQR 1.423 | 26.71 ± 14.54<br>Mdn 26.33, IQR 21.17 | 538.0 ± 267.5<br>Mdn 529.0, IQR 377.8 | 4,448 ± 940<br>Mdn 4,272, IQR 2,052 | 4,506 ± 947<br>Mdn 4,332, IQR 1,917 | 5,266 ± 947<br>Mdn 5,092, IQR 1,917 |
| core, random, q 10–20, k=5, n 100–1000 | Naive | 30 | 142.95 ± 69.13<br>Mdn 138.12, IQR 107.45 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 142.93 ± 69.13<br>Mdn 138.10, IQR 107.45 | 3,103.3 ± 1,413.4<br>Mdn 3,057.0, IQR 2,245.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=5, n 100–1000 | KMP | 30 | 121.42 ± 55.26<br>Mdn 118.50, IQR 85.07 | 3.431 ± 0.315<br>Mdn 3.417, IQR 0.461 | 117.99 ± 55.22<br>Mdn 114.96, IQR 84.74 | 3,176.3 ± 1,413.8<br>Mdn 3,137.5, IQR 2,239.8 | 1,075 ± 58<br>Mdn 1,080, IQR 80 | 1,075 ± 58<br>Mdn 1,080, IQR 80 | 1,141 ± 61<br>Mdn 1,152, IQR 81 |
| core, random, q 10–20, k=5, n 100–1000 | Aho-Corasick | 30 | 55.89 ± 18.46<br>Mdn 57.08, IQR 28.52 | 17.246 ± 1.826<br>Mdn 17.584, IQR 2.680 | 38.64 ± 18.27<br>Mdn 38.14, IQR 30.39 | 810.1 ± 298.1<br>Mdn 820.5, IQR 464.5 | 20,669 ± 1,979<br>Mdn 21,016, IQR 3,024 | 20,955 ± 2,015<br>Mdn 21,346, IQR 2,739 | 22,190 ± 2,120<br>Mdn 22,634, IQR 2,739 |
| core, random, q 1–5, k=1, n 1000–10000 | Naive | 30 | 277.71 ± 128.86<br>Mdn 274.19, IQR 227.89 | 0.028 ± 0.015<br>Mdn 0.026, IQR 0.004 | 277.69 ± 128.87<br>Mdn 274.16, IQR 227.89 | 5,702.4 ± 2,645.3<br>Mdn 5,561.5, IQR 4,699.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=1, n 1000–10000 | KMP | 30 | 219.72 ± 101.41<br>Mdn 211.42, IQR 176.65 | 0.223 ± 0.057<br>Mdn 0.224, IQR 0.077 | 219.50 ± 101.42<br>Mdn 211.19, IQR 176.58 | 5,703.5 ± 2,644.5<br>Mdn 5,563.5, IQR 4,701.5 | 223 ± 11<br>Mdn 224, IQR 14 | 223 ± 11<br>Mdn 224, IQR 14 | 277 ± 23<br>Mdn 272, IQR 24 |
| core, random, q 1–5, k=1, n 1000–10000 | Aho-Corasick | 30 | 309.29 ± 142.78<br>Mdn 300.76, IQR 246.76 | 1.023 ± 0.277<br>Mdn 1.064, IQR 0.343 | 308.27 ± 142.81<br>Mdn 299.69, IQR 246.33 | 5,723.1 ± 2,647.1<br>Mdn 5,567.5, IQR 4,674.2 | 1,400 ± 322<br>Mdn 1,440, IQR 420 | 1,412 ± 331<br>Mdn 1,440, IQR 435 | 2,172 ± 331<br>Mdn 2,200, IQR 435 |
| core, random, q 1–5, k=5, n 1000–10000 | Naive | 30 | 1,485.16 ± 652.38<br>Mdn 1,418.92, IQR 1,267.65 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.006 | 1,485.14 ± 652.38<br>Mdn 1,418.89, IQR 1,267.65 | 30,185.0 ± 13,189.6<br>Mdn 29,276.5, IQR 26,030.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=5, n 1000–10000 | KMP | 30 | 1,176.45 ± 513.08<br>Mdn 1,129.64, IQR 1,012.33 | 0.949 ± 0.156<br>Mdn 0.905, IQR 0.206 | 1,175.50 ± 513.07<br>Mdn 1,128.54, IQR 1,012.24 | 30,190.5 ± 13,188.2<br>Mdn 29,285.5, IQR 26,028.8 | 578 ± 28<br>Mdn 572, IQR 38 | 578 ± 28<br>Mdn 572, IQR 38 | 632 ± 29<br>Mdn 628, IQR 42 |
| core, random, q 1–5, k=5, n 1000–10000 | Aho-Corasick | 30 | 402.65 ± 176.49<br>Mdn 389.21, IQR 353.09 | 3.733 ± 0.750<br>Mdn 3.624, IQR 1.024 | 398.92 ± 176.45<br>Mdn 384.65, IQR 353.23 | 6,401.6 ± 2,785.1<br>Mdn 6,229.5, IQR 5,551.0 | 4,302 ± 901<br>Mdn 4,072, IQR 1,332 | 4,360 ± 907<br>Mdn 4,132, IQR 1,332 | 5,120 ± 907<br>Mdn 4,892, IQR 1,332 |
| core, random, q 5–10, k=1, n 1000–10000 | Naive | 30 | 286.78 ± 134.19<br>Mdn 289.51, IQR 250.53 | 0.025 ± 0.003<br>Mdn 0.025, IQR 0.005 | 286.75 ± 134.19<br>Mdn 289.48, IQR 250.52 | 5,905.7 ± 2,726.5<br>Mdn 5,946.5, IQR 5,197.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=1, n 1000–10000 | KMP | 30 | 226.23 ± 104.74<br>Mdn 228.36, IQR 201.58 | 0.406 ± 0.074<br>Mdn 0.419, IQR 0.141 | 225.82 ± 104.75<br>Mdn 227.99, IQR 201.55 | 5,911.1 ± 2,726.0<br>Mdn 5,952.0, IQR 5,198.5 | 258 ± 14<br>Mdn 256, IQR 22 | 258 ± 14<br>Mdn 256, IQR 22 | 314 ± 22<br>Mdn 312, IQR 35 |
| core, random, q 5–10, k=1, n 1000–10000 | Aho-Corasick | 30 | 319.27 ± 146.74<br>Mdn 322.94, IQR 284.52 | 1.905 ± 0.366<br>Mdn 1.881, IQR 0.614 | 317.37 ± 146.79<br>Mdn 321.14, IQR 284.22 | 5,919.4 ± 2,725.8<br>Mdn 5,959.5, IQR 5,199.5 | 2,531 ± 500<br>Mdn 2,400, IQR 852 | 2,549 ± 510<br>Mdn 2,430, IQR 867 | 3,309 ± 510<br>Mdn 3,190, IQR 867 |
| core, random, q 5–10, k=5, n 1000–10000 | Naive | 30 | 1,404.52 ± 636.95<br>Mdn 1,408.75, IQR 1,104.22 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.006 | 1,404.49 ± 636.95<br>Mdn 1,408.72, IQR 1,104.22 | 28,774.7 ± 12,844.3<br>Mdn 29,496.0, IQR 22,459.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=5, n 1000–10000 | KMP | 30 | 1,114.32 ± 503.90<br>Mdn 1,125.12, IQR 880.72 | 1.879 ± 0.148<br>Mdn 1.880, IQR 0.175 | 1,112.45 ± 503.84<br>Mdn 1,123.24, IQR 880.53 | 28,802.6 ± 12,841.9<br>Mdn 29,519.0, IQR 22,456.5 | 761 ± 30<br>Mdn 760, IQR 28 | 761 ± 30<br>Mdn 760, IQR 28 | 822 ± 37<br>Mdn 818, IQR 43 |
| core, random, q 5–10, k=5, n 1000–10000 | Aho-Corasick | 30 | 382.69 ± 170.26<br>Mdn 392.19, IQR 305.40 | 8.871 ± 1.018<br>Mdn 8.616, IQR 1.060 | 373.82 ± 169.85<br>Mdn 383.60, IQR 302.27 | 6,136.5 ± 2,710.2<br>Mdn 6,289.5, IQR 4,745.2 | 10,390 ± 1,026<br>Mdn 10,288, IQR 1,056 | 10,550 ± 1,059<br>Mdn 10,348, IQR 996 | 11,310 ± 1,059<br>Mdn 11,108, IQR 996 |
| core, random, q 10–20, k=1, n 1000–10000 | Naive | 30 | 295.83 ± 139.52<br>Mdn 312.03, IQR 203.58 | 0.025 ± 0.003<br>Mdn 0.025, IQR 0.005 | 295.80 ± 139.52<br>Mdn 312.01, IQR 203.58 | 6,024.1 ± 2,814.9<br>Mdn 6,214.0, IQR 4,204.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=1, n 1000–10000 | KMP | 30 | 234.16 ± 109.48<br>Mdn 249.08, IQR 164.77 | 0.725 ± 0.136<br>Mdn 0.759, IQR 0.213 | 233.43 ± 109.43<br>Mdn 248.29, IQR 164.57 | 6,037.5 ± 2,815.7<br>Mdn 6,230.5, IQR 4,208.8 | 322 ± 28<br>Mdn 328, IQR 52 | 322 ± 28<br>Mdn 328, IQR 52 | 389 ± 31<br>Mdn 392, IQR 52 |
| core, random, q 10–20, k=1, n 1000–10000 | Aho-Corasick | 30 | 326.96 ± 150.44<br>Mdn 336.70, IQR 226.64 | 3.545 ± 0.713<br>Mdn 3.702, IQR 1.245 | 323.42 ± 150.21<br>Mdn 332.61, IQR 226.61 | 6,053.9 ± 2,816.9<br>Mdn 6,249.5, IQR 4,213.5 | 4,678 ± 921<br>Mdn 4,944, IQR 1,752 | 4,734 ± 932<br>Mdn 5,004, IQR 1,737 | 5,494 ± 932<br>Mdn 5,764, IQR 1,737 |
| core, random, q 10–20, k=5, n 1000–10000 | Naive | 30 | 1,506.33 ± 614.44<br>Mdn 1,702.62, IQR 992.29 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.004 | 1,506.31 ± 614.45<br>Mdn 1,702.59, IQR 992.29 | 30,486.5 ± 12,237.1<br>Mdn 34,548.0, IQR 20,006.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=5, n 1000–10000 | KMP | 30 | 1,193.49 ± 481.90<br>Mdn 1,348.13, IQR 769.84 | 3.370 ± 0.383<br>Mdn 3.369, IQR 0.606 | 1,190.12 ± 481.81<br>Mdn 1,345.08, IQR 769.88 | 30,551.6 ± 12,237.5<br>Mdn 34,621.0, IQR 20,008.8 | 1,055 ± 72<br>Mdn 1,056, IQR 106 | 1,055 ± 72<br>Mdn 1,056, IQR 106 | 1,123 ± 71<br>Mdn 1,122, IQR 101 |
| core, random, q 10–20, k=5, n 1000–10000 | Aho-Corasick | 30 | 412.03 ± 160.61<br>Mdn 465.96, IQR 260.44 | 16.949 ± 2.179<br>Mdn 16.495, IQR 3.124 | 395.08 ± 160.09<br>Mdn 447.81, IQR 261.37 | 6,569.0 ± 2,581.9<br>Mdn 7,428.0, IQR 4,235.2 | 20,119 ± 2,394<br>Mdn 20,032, IQR 3,564 | 20,413 ± 2,413<br>Mdn 20,302, IQR 3,564 | 21,613 ± 2,553<br>Mdn 21,590, IQR 3,564 |
| core, narrative, q 1–5, k=1, n 10–100 | Naive | 30 | 2.51 ± 1.04<br>Mdn 2.77, IQR 1.74 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 2.49 ± 1.04<br>Mdn 2.75, IQR 1.74 | 57.5 ± 25.9<br>Mdn 64.0, IQR 34.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=1, n 10–100 | KMP | 30 | 2.42 ± 0.89<br>Mdn 2.60, IQR 1.38 | 0.233 ± 0.060<br>Mdn 0.221, IQR 0.081 | 2.19 ± 0.91<br>Mdn 2.35, IQR 1.52 | 59.7 ± 25.3<br>Mdn 65.0, IQR 33.2 | 226 ± 10<br>Mdn 224, IQR 14 | 226 ± 10<br>Mdn 224, IQR 14 | 276 ± 14<br>Mdn 272, IQR 22 |
| core, narrative, q 1–5, k=1, n 10–100 | Aho-Corasick | 30 | 3.98 ± 1.18<br>Mdn 4.23, IQR 1.59 | 1.029 ± 0.264<br>Mdn 1.004, IQR 0.373 | 2.95 ± 1.26<br>Mdn 3.24, IQR 2.11 | 64.6 ± 25.3<br>Mdn 71.0, IQR 33.2 | 1,488 ± 311<br>Mdn 1,440, IQR 420 | 1,494 ± 314<br>Mdn 1,440, IQR 465 | 2,254 ± 314<br>Mdn 2,200, IQR 465 |
| core, narrative, q 1–5, k=5, n 10–100 | Naive | 30 | 13.27 ± 5.60<br>Mdn 14.09, IQR 10.23 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 13.24 ± 5.60<br>Mdn 14.07, IQR 10.23 | 312.1 ± 139.5<br>Mdn 333.0, IQR 259.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=5, n 10–100 | KMP | 30 | 12.50 ± 4.96<br>Mdn 13.42, IQR 9.24 | 0.917 ± 0.124<br>Mdn 0.889, IQR 0.183 | 11.58 ± 4.95<br>Mdn 12.47, IQR 9.18 | 320.3 ± 139.2<br>Mdn 342.0, IQR 272.5 | 575 ± 22<br>Mdn 572, IQR 32 | 575 ± 22<br>Mdn 572, IQR 32 | 624 ± 24<br>Mdn 620, IQR 32 |
| core, narrative, q 1–5, k=5, n 10–100 | Aho-Corasick | 30 | 7.55 ± 1.91<br>Mdn 7.85, IQR 3.30 | 3.373 ± 0.646<br>Mdn 3.281, IQR 0.486 | 4.18 ± 1.74<br>Mdn 4.24, IQR 3.07 | 101.7 ± 34.0<br>Mdn 107.0, IQR 66.5 | 3,911 ± 787<br>Mdn 3,776, IQR 696 | 3,929 ± 787<br>Mdn 3,776, IQR 696 | 4,689 ± 787<br>Mdn 4,536, IQR 696 |
| core, narrative, q 5–10, k=1, n 10–100 | Naive | 30 | 2.53 ± 1.19<br>Mdn 2.77, IQR 1.90 | 0.023 ± 0.001<br>Mdn 0.022, IQR 0.000 | 2.51 ± 1.19<br>Mdn 2.75, IQR 1.90 | 59.5 ± 30.5<br>Mdn 65.0, IQR 49.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=1, n 10–100 | KMP | 30 | 2.66 ± 1.04<br>Mdn 2.88, IQR 1.68 | 0.418 ± 0.070<br>Mdn 0.427, IQR 0.107 | 2.24 ± 1.04<br>Mdn 2.45, IQR 1.64 | 66.0 ± 30.0<br>Mdn 71.0, IQR 52.5 | 260 ± 14<br>Mdn 260, IQR 24 | 260 ± 14<br>Mdn 260, IQR 24 | 313 ± 20<br>Mdn 312, IQR 30 |
| core, narrative, q 5–10, k=1, n 10–100 | Aho-Corasick | 30 | 4.88 ± 1.42<br>Mdn 5.07, IQR 2.35 | 1.900 ± 0.370<br>Mdn 1.859, IQR 0.634 | 2.98 ± 1.43<br>Mdn 3.16, IQR 2.26 | 74.8 ± 30.0<br>Mdn 80.0, IQR 55.5 | 2,624 ± 510<br>Mdn 2,616, IQR 912 | 2,634 ± 517<br>Mdn 2,616, IQR 957 | 3,394 ± 517<br>Mdn 3,376, IQR 957 |
| core, narrative, q 5–10, k=5, n 10–100 | Naive | 30 | 12.62 ± 5.61<br>Mdn 14.34, IQR 9.34 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 12.60 ± 5.61<br>Mdn 14.32, IQR 9.34 | 307.9 ± 144.5<br>Mdn 342.5, IQR 231.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=5, n 10–100 | KMP | 30 | 13.17 ± 4.94<br>Mdn 14.63, IQR 7.97 | 1.868 ± 0.147<br>Mdn 1.859, IQR 0.149 | 11.30 ± 4.97<br>Mdn 12.68, IQR 8.01 | 338.8 ± 141.8<br>Mdn 370.5, IQR 224.2 | 757 ± 29<br>Mdn 756, IQR 30 | 757 ± 29<br>Mdn 756, IQR 30 | 809 ± 32<br>Mdn 808, IQR 39 |
| core, narrative, q 5–10, k=5, n 10–100 | Aho-Corasick | 30 | 11.65 ± 2.22<br>Mdn 12.51, IQR 3.34 | 7.933 ± 1.072<br>Mdn 8.036, IQR 1.166 | 3.72 ± 1.64<br>Mdn 4.14, IQR 2.66 | 151.9 ± 40.2<br>Mdn 166.5, IQR 65.5 | 9,597 ± 1,353<br>Mdn 9,744, IQR 1,758 | 9,637 ± 1,354<br>Mdn 9,744, IQR 1,623 | 10,397 ± 1,353<br>Mdn 10,504, IQR 1,623 |
| core, narrative, q 10–20, k=1, n 10–100 | Naive | 30 | 2.57 ± 0.97<br>Mdn 2.61, IQR 0.98 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 2.55 ± 0.97<br>Mdn 2.59, IQR 0.98 | 62.7 ± 25.3<br>Mdn 63.5, IQR 25.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=1, n 10–100 | KMP | 30 | 3.07 ± 0.94<br>Mdn 2.98, IQR 0.92 | 0.719 ± 0.119<br>Mdn 0.708, IQR 0.172 | 2.35 ± 0.88<br>Mdn 2.33, IQR 0.82 | 76.8 ± 26.1<br>Mdn 76.5, IQR 23.0 | 320 ± 25<br>Mdn 320, IQR 38 | 320 ± 25<br>Mdn 320, IQR 38 | 371 ± 29<br>Mdn 372, IQR 41 |
| core, narrative, q 10–20, k=1, n 10–100 | Aho-Corasick | 30 | 6.47 ± 1.52<br>Mdn 6.45, IQR 2.11 | 3.396 ± 0.625<br>Mdn 3.360, IQR 0.957 | 3.08 ± 1.17<br>Mdn 3.12, IQR 0.95 | 93.4 ± 27.8<br>Mdn 93.5, IQR 25.8 | 4,602 ± 837<br>Mdn 4,512, IQR 1,332 | 4,608 ± 842<br>Mdn 4,512, IQR 1,332 | 5,368 ± 842<br>Mdn 5,272, IQR 1,332 |
| core, narrative, q 10–20, k=5, n 10–100 | Naive | 30 | 11.54 ± 5.35<br>Mdn 10.92, IQR 9.65 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 11.51 ± 5.35<br>Mdn 10.90, IQR 9.65 | 287.7 ± 137.6<br>Mdn 270.0, IQR 239.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=5, n 10–100 | KMP | 30 | 13.94 ± 4.61<br>Mdn 13.76, IQR 8.40 | 3.392 ± 0.395<br>Mdn 3.384, IQR 0.633 | 10.55 ± 4.58<br>Mdn 10.11, IQR 8.45 | 358.5 ± 134.2<br>Mdn 340.5, IQR 242.2 | 1,052 ± 65<br>Mdn 1,056, IQR 106 | 1,052 ± 65<br>Mdn 1,056, IQR 106 | 1,106 ± 69<br>Mdn 1,104, IQR 101 |
| core, narrative, q 10–20, k=5, n 10–100 | Aho-Corasick | 30 | 18.22 ± 2.79<br>Mdn 18.42, IQR 3.54 | 14.966 ± 2.106<br>Mdn 14.693, IQR 2.858 | 3.25 ± 1.43<br>Mdn 3.09, IQR 2.44 | 218.6 ± 41.4<br>Mdn 216.5, IQR 60.5 | 18,485 ± 2,654<br>Mdn 18,284, IQR 3,916 | 18,559 ± 2,681<br>Mdn 18,464, IQR 3,906 | 19,671 ± 2,881<br>Mdn 19,752, IQR 4,434 |
| core, narrative, q 1–5, k=1, n 100–1000 | Naive | 30 | 25.55 ± 11.87<br>Mdn 27.35, IQR 16.18 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.001 | 25.53 ± 11.87<br>Mdn 27.33, IQR 16.18 | 566.8 ± 251.1<br>Mdn 590.5, IQR 328.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=1, n 100–1000 | KMP | 30 | 21.31 ± 9.47<br>Mdn 23.31, IQR 11.60 | 0.213 ± 0.061<br>Mdn 0.194, IQR 0.092 | 21.10 ± 9.46<br>Mdn 23.17, IQR 11.58 | 565.0 ± 250.1<br>Mdn 588.5, IQR 325.5 | 222 ± 11<br>Mdn 220, IQR 16 | 222 ± 11<br>Mdn 220, IQR 16 | 270 ± 11<br>Mdn 268, IQR 16 |
| core, narrative, q 1–5, k=1, n 100–1000 | Aho-Corasick | 30 | 30.39 ± 13.10<br>Mdn 32.95, IQR 17.88 | 0.949 ± 0.292<br>Mdn 0.897, IQR 0.448 | 29.44 ± 13.09<br>Mdn 32.04, IQR 17.77 | 580.7 ± 250.6<br>Mdn 615.5, IQR 319.2 | 1,392 ± 342<br>Mdn 1,320, IQR 480 | 1,392 ± 342<br>Mdn 1,320, IQR 480 | 2,152 ± 342<br>Mdn 2,080, IQR 480 |
| core, narrative, q 1–5, k=5, n 100–1000 | Naive | 30 | 131.53 ± 72.27<br>Mdn 130.77, IQR 142.77 | 0.022 ± 0.002<br>Mdn 0.022, IQR 0.000 | 131.50 ± 72.27<br>Mdn 130.75, IQR 142.77 | 2,924.3 ± 1,513.3<br>Mdn 2,957.5, IQR 2,847.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=5, n 100–1000 | KMP | 30 | 110.50 ± 58.52<br>Mdn 110.32, IQR 114.73 | 0.926 ± 0.171<br>Mdn 0.917, IQR 0.236 | 109.58 ± 58.46<br>Mdn 109.48, IQR 114.68 | 2,914.3 ± 1,506.4<br>Mdn 2,944.5, IQR 2,835.2 | 578 ± 30<br>Mdn 580, IQR 38 | 578 ± 30<br>Mdn 580, IQR 38 | 626 ± 30<br>Mdn 628, IQR 38 |
| core, narrative, q 1–5, k=5, n 100–1000 | Aho-Corasick | 30 | 42.51 ± 20.98<br>Mdn 42.32, IQR 40.03 | 3.594 ± 0.852<br>Mdn 3.552, IQR 1.251 | 38.92 ± 20.68<br>Mdn 39.16, IQR 39.60 | 740.0 ± 383.0<br>Mdn 712.5, IQR 731.8 | 4,223 ± 1,030<br>Mdn 4,196, IQR 1,572 | 4,247 ± 1,033<br>Mdn 4,226, IQR 1,602 | 5,007 ± 1,033<br>Mdn 4,986, IQR 1,602 |
| core, narrative, q 5–10, k=1, n 100–1000 | Naive | 30 | 20.70 ± 10.81<br>Mdn 17.94, IQR 17.77 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.001 | 20.68 ± 10.81<br>Mdn 17.92, IQR 17.77 | 479.8 ± 225.7<br>Mdn 422.0, IQR 348.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=1, n 100–1000 | KMP | 30 | 17.86 ± 8.56<br>Mdn 15.47, IQR 14.48 | 0.435 ± 0.072<br>Mdn 0.450, IQR 0.116 | 17.43 ± 8.55<br>Mdn 15.06, IQR 14.57 | 481.4 ± 223.2<br>Mdn 425.5, IQR 346.8 | 263 ± 13<br>Mdn 264, IQR 16 | 263 ± 13<br>Mdn 264, IQR 16 | 313 ± 14<br>Mdn 312, IQR 16 |
| core, narrative, q 5–10, k=1, n 100–1000 | Aho-Corasick | 30 | 25.64 ± 11.52<br>Mdn 23.16, IQR 18.48 | 1.983 ± 0.326<br>Mdn 2.045, IQR 0.504 | 23.66 ± 11.51<br>Mdn 20.97, IQR 18.62 | 490.7 ± 223.3<br>Mdn 434.5, IQR 346.8 | 2,738 ± 474<br>Mdn 2,832, IQR 672 | 2,742 ± 472<br>Mdn 2,832, IQR 672 | 3,502 ± 472<br>Mdn 3,592, IQR 672 |
| core, narrative, q 5–10, k=5, n 100–1000 | Naive | 30 | 132.99 ± 75.23<br>Mdn 129.75, IQR 144.00 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 132.97 ± 75.23<br>Mdn 129.72, IQR 144.00 | 2,979.4 ± 1,567.1<br>Mdn 2,925.0, IQR 2,923.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=5, n 100–1000 | KMP | 30 | 112.01 ± 59.87<br>Mdn 109.65, IQR 113.56 | 1.787 ± 0.135<br>Mdn 1.801, IQR 0.115 | 110.22 ± 59.88<br>Mdn 107.71, IQR 113.67 | 2,974.3 ± 1,549.6<br>Mdn 2,923.5, IQR 2,885.5 | 739 ± 28<br>Mdn 740, IQR 24 | 739 ± 28<br>Mdn 740, IQR 24 | 791 ± 31<br>Mdn 792, IQR 34 |
| core, narrative, q 5–10, k=5, n 100–1000 | Aho-Corasick | 30 | 44.56 ± 19.67<br>Mdn 45.99, IQR 35.72 | 7.933 ± 0.814<br>Mdn 7.917, IQR 0.963 | 36.63 ± 19.70<br>Mdn 36.94, IQR 37.03 | 773.1 ± 363.2<br>Mdn 794.5, IQR 655.8 | 9,478 ± 974<br>Mdn 9,560, IQR 1,140 | 9,536 ± 970<br>Mdn 9,560, IQR 1,170 | 10,296 ± 970<br>Mdn 10,320, IQR 1,170 |
| core, narrative, q 10–20, k=1, n 100–1000 | Naive | 30 | 28.62 ± 17.27<br>Mdn 27.77, IQR 31.28 | 0.023 ± 0.008<br>Mdn 0.022, IQR 0.000 | 28.59 ± 17.28<br>Mdn 27.75, IQR 31.28 | 638.9 ± 358.5<br>Mdn 637.0, IQR 659.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=1, n 100–1000 | KMP | 30 | 24.69 ± 14.02<br>Mdn 24.19, IQR 25.81 | 0.736 ± 0.142<br>Mdn 0.736, IQR 0.219 | 23.95 ± 14.02<br>Mdn 23.47, IQR 25.79 | 645.0 ± 352.7<br>Mdn 634.0, IQR 646.0 | 318 ± 23<br>Mdn 316, IQR 38 | 318 ± 23<br>Mdn 316, IQR 38 | 381 ± 35<br>Mdn 384, IQR 41 |
| core, narrative, q 10–20, k=1, n 100–1000 | Aho-Corasick | 30 | 34.81 ± 17.91<br>Mdn 33.49, IQR 32.67 | 3.385 ± 0.602<br>Mdn 3.336, IQR 0.938 | 31.43 ± 17.94<br>Mdn 30.24, IQR 32.81 | 662.1 ± 352.9<br>Mdn 650.5, IQR 644.2 | 4,554 ± 778<br>Mdn 4,392, IQR 1,332 | 4,584 ± 789<br>Mdn 4,452, IQR 1,332 | 5,344 ± 789<br>Mdn 5,212, IQR 1,332 |
| core, narrative, q 10–20, k=5, n 100–1000 | Naive | 30 | 131.88 ± 64.96<br>Mdn 128.52, IQR 114.81 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 131.86 ± 64.96<br>Mdn 128.50, IQR 114.81 | 2,981.3 ± 1,332.2<br>Mdn 2,967.5, IQR 2,397.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=5, n 100–1000 | KMP | 30 | 113.57 ± 52.22<br>Mdn 109.11, IQR 94.98 | 3.414 ± 0.363<br>Mdn 3.422, IQR 0.479 | 110.16 ± 52.16<br>Mdn 105.97, IQR 94.14 | 3,015.7 ± 1,319.1<br>Mdn 2,917.0, IQR 2,402.8 | 1,061 ± 58<br>Mdn 1,076, IQR 84 | 1,061 ± 58<br>Mdn 1,076, IQR 84 | 1,118 ± 60<br>Mdn 1,128, IQR 80 |
| core, narrative, q 10–20, k=5, n 100–1000 | Aho-Corasick | 30 | 52.56 ± 17.07<br>Mdn 49.64, IQR 30.61 | 16.717 ± 1.658<br>Mdn 16.784, IQR 2.256 | 35.85 ± 16.79<br>Mdn 33.89, IQR 28.21 | 862.8 ± 322.4<br>Mdn 825.0, IQR 586.8 | 20,081 ± 1,852<br>Mdn 20,464, IQR 2,544 | 20,169 ± 1,864<br>Mdn 20,524, IQR 2,482 | 21,386 ± 1,987<br>Mdn 21,812, IQR 2,482 |
| core, narrative, q 1–5, k=1, n 1000–10000 | Naive | 30 | 310.26 ± 160.72<br>Mdn 354.46, IQR 288.72 | 0.026 ± 0.002<br>Mdn 0.026, IQR 0.003 | 310.23 ± 160.72<br>Mdn 354.43, IQR 288.72 | 6,444.7 ± 3,314.0<br>Mdn 7,474.5, IQR 6,257.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=1, n 1000–10000 | KMP | 30 | 250.68 ± 129.16<br>Mdn 284.44, IQR 229.95 | 0.225 ± 0.067<br>Mdn 0.223, IQR 0.130 | 250.46 ± 129.16<br>Mdn 284.17, IQR 229.93 | 6,410.3 ± 3,290.8<br>Mdn 7,420.0, IQR 6,251.8 | 223 ± 13<br>Mdn 224, IQR 30 | 223 ± 13<br>Mdn 224, IQR 30 | 272 ± 15<br>Mdn 272, IQR 30 |
| core, narrative, q 1–5, k=1, n 1000–10000 | Aho-Corasick | 30 | 337.53 ± 170.96<br>Mdn 385.53, IQR 296.30 | 1.028 ± 0.332<br>Mdn 1.046, IQR 0.734 | 336.50 ± 170.96<br>Mdn 384.23, IQR 296.24 | 6,498.2 ± 3,316.6<br>Mdn 7,470.0, IQR 6,042.2 | 1,416 ± 390<br>Mdn 1,440, IQR 900 | 1,418 ± 393<br>Mdn 1,440, IQR 900 | 2,178 ± 393<br>Mdn 2,200, IQR 900 |
| core, narrative, q 1–5, k=5, n 1000–10000 | Naive | 30 | 1,315.26 ± 700.33<br>Mdn 1,278.16, IQR 1,002.58 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.002 | 1,315.23 ± 700.33<br>Mdn 1,278.13, IQR 1,002.58 | 27,053.4 ± 14,402.5<br>Mdn 26,587.0, IQR 20,619.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=5, n 1000–10000 | KMP | 30 | 1,060.00 ± 564.99<br>Mdn 1,037.65, IQR 783.74 | 0.951 ± 0.140<br>Mdn 0.945, IQR 0.166 | 1,059.05 ± 564.98<br>Mdn 1,036.63, IQR 783.64 | 26,808.6 ± 14,241.8<br>Mdn 26,482.0, IQR 20,351.8 | 577 ± 25<br>Mdn 576, IQR 30 | 577 ± 25<br>Mdn 576, IQR 30 | 627 ± 25<br>Mdn 628, IQR 31 |
| core, narrative, q 1–5, k=5, n 1000–10000 | Aho-Corasick | 30 | 374.93 ± 193.27<br>Mdn 372.62, IQR 277.29 | 3.691 ± 0.675<br>Mdn 3.669, IQR 0.984 | 371.24 ± 193.27<br>Mdn 368.59, IQR 277.43 | 6,657.7 ± 3,522.2<br>Mdn 6,505.0, IQR 4,562.2 | 4,168 ± 792<br>Mdn 4,192, IQR 1,096 | 4,192 ± 800<br>Mdn 4,196, IQR 1,137 | 4,952 ± 799<br>Mdn 4,956, IQR 1,137 |
| core, narrative, q 5–10, k=1, n 1000–10000 | Naive | 30 | 284.47 ± 158.69<br>Mdn 310.23, IQR 253.74 | 0.025 ± 0.004<br>Mdn 0.025, IQR 0.005 | 284.45 ± 158.69<br>Mdn 310.21, IQR 253.74 | 5,877.4 ± 3,187.9<br>Mdn 6,459.0, IQR 5,163.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=1, n 1000–10000 | KMP | 30 | 228.41 ± 128.34<br>Mdn 244.38, IQR 196.86 | 0.435 ± 0.069<br>Mdn 0.445, IQR 0.098 | 227.97 ± 128.35<br>Mdn 243.96, IQR 196.94 | 5,791.8 ± 3,125.8<br>Mdn 6,201.0, IQR 5,041.8 | 262 ± 12<br>Mdn 264, IQR 22 | 262 ± 12<br>Mdn 264, IQR 22 | 318 ± 24<br>Mdn 312, IQR 19 |
| core, narrative, q 5–10, k=1, n 1000–10000 | Aho-Corasick | 30 | 297.88 ± 160.79<br>Mdn 322.54, IQR 270.93 | 2.023 ± 0.313<br>Mdn 2.039, IQR 0.455 | 295.86 ± 160.83<br>Mdn 320.59, IQR 270.97 | 5,805.1 ± 3,126.3<br>Mdn 6,261.5, IQR 5,040.2 | 2,677 ± 449<br>Mdn 2,832, IQR 852 | 2,691 ± 445<br>Mdn 2,832, IQR 762 | 3,451 ± 445<br>Mdn 3,592, IQR 762 |
| core, narrative, q 5–10, k=5, n 1000–10000 | Naive | 30 | 1,464.34 ± 749.32<br>Mdn 1,542.96, IQR 1,393.32 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.006 | 1,464.32 ± 749.32<br>Mdn 1,542.93, IQR 1,393.32 | 30,390.9 ± 15,177.7<br>Mdn 32,584.5, IQR 29,234.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=5, n 1000–10000 | KMP | 30 | 1,170.60 ± 589.98<br>Mdn 1,252.51, IQR 1,092.13 | 1.837 ± 0.159<br>Mdn 1.829, IQR 0.106 | 1,168.77 ± 589.98<br>Mdn 1,250.78, IQR 1,092.38 | 30,050.3 ± 14,970.3<br>Mdn 32,260.5, IQR 28,661.5 | 753 ± 28<br>Mdn 752, IQR 32 | 753 ± 28<br>Mdn 752, IQR 32 | 808 ± 34<br>Mdn 800, IQR 38 |
| core, narrative, q 5–10, k=5, n 1000–10000 | Aho-Corasick | 30 | 387.46 ± 188.93<br>Mdn 410.84, IQR 345.49 | 8.415 ± 0.854<br>Mdn 8.371, IQR 0.781 | 379.04 ± 188.89<br>Mdn 403.07, IQR 346.28 | 7,126.4 ± 3,433.8<br>Mdn 7,516.0, IQR 5,915.2 | 9,936 ± 1,047<br>Mdn 9,808, IQR 1,140 | 10,004 ± 1,073<br>Mdn 9,898, IQR 1,140 | 10,764 ± 1,073<br>Mdn 10,658, IQR 1,140 |
| core, narrative, q 10–20, k=1, n 1000–10000 | Naive | 30 | 278.86 ± 150.59<br>Mdn 298.71, IQR 254.62 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.006 | 278.83 ± 150.59<br>Mdn 298.69, IQR 254.62 | 5,868.7 ± 3,144.4<br>Mdn 6,281.0, IQR 5,348.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=1, n 1000–10000 | KMP | 30 | 223.00 ± 120.24<br>Mdn 237.02, IQR 200.78 | 0.691 ± 0.123<br>Mdn 0.682, IQR 0.194 | 222.31 ± 120.21<br>Mdn 236.35, IQR 200.92 | 5,811.5 ± 3,103.0<br>Mdn 6,278.0, IQR 5,295.2 | 314 ± 22<br>Mdn 312, IQR 38 | 314 ± 22<br>Mdn 312, IQR 38 | 367 ± 26<br>Mdn 360, IQR 43 |
| core, narrative, q 10–20, k=1, n 1000–10000 | Aho-Corasick | 30 | 302.90 ± 160.49<br>Mdn 332.48, IQR 269.10 | 3.312 ± 0.565<br>Mdn 3.293, IQR 1.050 | 299.59 ± 160.40<br>Mdn 329.76, IQR 270.04 | 5,827.4 ± 3,103.6<br>Mdn 6,298.5, IQR 5,291.0 | 4,392 ± 735<br>Mdn 4,272, IQR 1,332 | 4,406 ± 739<br>Mdn 4,272, IQR 1,347 | 5,166 ± 739<br>Mdn 5,032, IQR 1,347 |
| core, narrative, q 10–20, k=5, n 1000–10000 | Naive | 30 | 1,459.78 ± 656.71<br>Mdn 1,290.53, IQR 1,169.82 | 0.025 ± 0.003<br>Mdn 0.026, IQR 0.004 | 1,459.75 ± 656.71<br>Mdn 1,290.51, IQR 1,169.81 | 30,651.9 ± 13,573.0<br>Mdn 27,434.0, IQR 24,006.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=5, n 1000–10000 | KMP | 30 | 1,175.57 ± 525.36<br>Mdn 1,047.26, IQR 933.89 | 3.415 ± 0.342<br>Mdn 3.447, IQR 0.534 | 1,172.15 ± 525.31<br>Mdn 1,044.16, IQR 934.12 | 30,399.5 ± 13,446.1<br>Mdn 27,172.0, IQR 23,956.0 | 1,069 ± 64<br>Mdn 1,092, IQR 88 | 1,069 ± 64<br>Mdn 1,092, IQR 88 | 1,126 ± 69<br>Mdn 1,144, IQR 100 |
| core, narrative, q 10–20, k=5, n 1000–10000 | Aho-Corasick | 30 | 396.07 ± 163.32<br>Mdn 359.13, IQR 291.85 | 17.327 ± 1.938<br>Mdn 17.788, IQR 3.179 | 378.74 ± 163.22<br>Mdn 343.26, IQR 295.06 | 7,376.9 ± 3,151.4<br>Mdn 6,799.0, IQR 5,428.2 | 20,418 ± 2,164<br>Mdn 21,136, IQR 3,024 | 20,526 ± 2,186<br>Mdn 21,196, IQR 3,249 | 21,743 ± 2,318<br>Mdn 22,484, IQR 3,249 |
| query_pattern, distinct, n 10–100 | Naive | 30 | 1.99 ± 1.03<br>Mdn 1.97, IQR 1.65 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 1.97 ± 1.03<br>Mdn 1.95, IQR 1.65 | 46.2 ± 26.6<br>Mdn 45.0, IQR 42.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, distinct, n 10–100 | KMP | 30 | 2.30 ± 0.88<br>Mdn 2.25, IQR 1.62 | 0.408 ± 0.060<br>Mdn 0.422, IQR 0.076 | 1.89 ± 0.89<br>Mdn 1.84, IQR 1.56 | 59.7 ± 26.4<br>Mdn 59.0, IQR 46.8 | 262 ± 13<br>Mdn 264, IQR 16 | 262 ± 13<br>Mdn 264, IQR 16 | 310 ± 13<br>Mdn 312, IQR 16 |
| query_pattern, distinct, n 10–100 | Aho-Corasick | 30 | 4.53 ± 1.24<br>Mdn 4.66, IQR 2.15 | 1.929 ± 0.317<br>Mdn 1.981, IQR 0.427 | 2.60 ± 1.23<br>Mdn 2.63, IQR 2.13 | 67.5 ± 26.4<br>Mdn 68.0, IQR 47.0 | 2,691 ± 468<br>Mdn 2,832, IQR 672 | 2,691 ± 468<br>Mdn 2,832, IQR 672 | 3,451 ± 468<br>Mdn 3,592, IQR 672 |
| query_pattern, repeating, n 10–100 | Naive | 30 | 2.13 ± 1.05<br>Mdn 2.11, IQR 1.63 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 2.10 ± 1.05<br>Mdn 2.09, IQR 1.63 | 49.5 ± 27.2<br>Mdn 48.0, IQR 40.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, repeating, n 10–100 | KMP | 30 | 2.43 ± 0.91<br>Mdn 2.28, IQR 1.21 | 0.415 ± 0.054<br>Mdn 0.430, IQR 0.085 | 2.01 ± 0.91<br>Mdn 1.88, IQR 1.27 | 63.9 ± 27.1<br>Mdn 60.0, IQR 35.5 | 265 ± 13<br>Mdn 268, IQR 22 | 265 ± 13<br>Mdn 268, IQR 22 | 313 ± 13<br>Mdn 316, IQR 22 |
| query_pattern, repeating, n 10–100 | Aho-Corasick | 30 | 4.76 ± 1.28<br>Mdn 4.79, IQR 2.21 | 1.967 ± 0.318<br>Mdn 2.040, IQR 0.529 | 2.79 ± 1.26<br>Mdn 2.68, IQR 1.87 | 72.0 ± 27.2<br>Mdn 70.0, IQR 37.2 | 2,808 ± 471<br>Mdn 2,952, IQR 852 | 2,808 ± 471<br>Mdn 2,952, IQR 852 | 3,568 ± 471<br>Mdn 3,712, IQR 852 |
| query_pattern, distinct, n 100–1000 | Naive | 30 | 22.01 ± 11.81<br>Mdn 19.74, IQR 14.31 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 21.98 ± 11.81<br>Mdn 19.72, IQR 14.31 | 504.7 ± 248.8<br>Mdn 462.0, IQR 312.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, distinct, n 100–1000 | KMP | 30 | 18.35 ± 9.17<br>Mdn 16.31, IQR 11.40 | 0.401 ± 0.080<br>Mdn 0.406, IQR 0.094 | 17.95 ± 9.16<br>Mdn 15.98, IQR 11.43 | 517.3 ± 248.9<br>Mdn 472.0, IQR 310.8 | 259 ± 12<br>Mdn 260, IQR 20 | 259 ± 12<br>Mdn 260, IQR 20 | 307 ± 12<br>Mdn 308, IQR 20 |
| query_pattern, distinct, n 100–1000 | Aho-Corasick | 30 | 27.48 ± 12.94<br>Mdn 24.80, IQR 14.01 | 1.831 ± 0.308<br>Mdn 1.834, IQR 0.469 | 25.65 ± 12.92<br>Mdn 23.25, IQR 14.22 | 524.7 ± 249.1<br>Mdn 478.0, IQR 310.0 | 2,576 ± 450<br>Mdn 2,616, IQR 792 | 2,576 ± 450<br>Mdn 2,616, IQR 792 | 3,336 ± 450<br>Mdn 3,376, IQR 792 |
| query_pattern, repeating, n 100–1000 | Naive | 30 | 22.77 ± 11.81<br>Mdn 22.37, IQR 21.36 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 22.75 ± 11.81<br>Mdn 22.34, IQR 21.36 | 520.7 ± 253.2<br>Mdn 513.0, IQR 439.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, repeating, n 100–1000 | KMP | 30 | 19.22 ± 9.38<br>Mdn 18.93, IQR 16.29 | 0.416 ± 0.056<br>Mdn 0.430, IQR 0.084 | 18.80 ± 9.38<br>Mdn 18.48, IQR 16.27 | 534.6 ± 252.5<br>Mdn 528.5, IQR 438.5 | 264 ± 13<br>Mdn 264, IQR 22 | 264 ± 13<br>Mdn 264, IQR 22 | 312 ± 13<br>Mdn 312, IQR 22 |
| query_pattern, repeating, n 100–1000 | Aho-Corasick | 30 | 28.28 ± 12.83<br>Mdn 27.96, IQR 22.69 | 1.925 ± 0.311<br>Mdn 1.942, IQR 0.537 | 26.36 ± 12.87<br>Mdn 25.85, IQR 22.85 | 542.7 ± 252.4<br>Mdn 537.5, IQR 436.8 | 2,763 ± 464<br>Mdn 2,832, IQR 852 | 2,763 ± 464<br>Mdn 2,832, IQR 852 | 3,523 ± 464<br>Mdn 3,592, IQR 852 |
| query_pattern, distinct, n 1000–10000 | Naive | 30 | 233.89 ± 136.13<br>Mdn 271.75, IQR 223.96 | 0.026 ± 0.003<br>Mdn 0.026, IQR 0.007 | 233.87 ± 136.13<br>Mdn 271.73, IQR 223.96 | 4,951.7 ± 2,845.3<br>Mdn 5,745.0, IQR 4,720.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, distinct, n 1000–10000 | KMP | 30 | 183.86 ± 106.35<br>Mdn 214.15, IQR 175.42 | 0.409 ± 0.068<br>Mdn 0.426, IQR 0.110 | 183.45 ± 106.34<br>Mdn 213.77, IQR 175.37 | 4,965.0 ± 2,845.8<br>Mdn 5,756.0, IQR 4,722.0 | 262 ± 15<br>Mdn 264, IQR 24 | 262 ± 15<br>Mdn 264, IQR 24 | 310 ± 15<br>Mdn 312, IQR 24 |
| query_pattern, distinct, n 1000–10000 | Aho-Corasick | 30 | 261.37 ± 151.24<br>Mdn 296.53, IQR 246.84 | 1.983 ± 0.409<br>Mdn 2.059, IQR 0.719 | 259.39 ± 151.19<br>Mdn 294.64, IQR 246.58 | 4,972.7 ± 2,846.1<br>Mdn 5,762.5, IQR 4,723.0 | 2,670 ± 554<br>Mdn 2,832, IQR 912 | 2,670 ± 554<br>Mdn 2,832, IQR 912 | 3,430 ± 554<br>Mdn 3,592, IQR 912 |
| query_pattern, repeating, n 1000–10000 | Naive | 30 | 292.09 ± 114.42<br>Mdn 312.72, IQR 157.87 | 0.026 ± 0.003<br>Mdn 0.027, IQR 0.003 | 292.07 ± 114.42<br>Mdn 312.70, IQR 157.87 | 6,151.2 ± 2,393.6<br>Mdn 6,598.5, IQR 3,332.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, repeating, n 1000–10000 | KMP | 30 | 228.93 ± 89.22<br>Mdn 244.04, IQR 130.40 | 0.385 ± 0.061<br>Mdn 0.367, IQR 0.113 | 228.54 ± 89.21<br>Mdn 243.65, IQR 130.50 | 6,160.2 ± 2,392.4<br>Mdn 6,591.5, IQR 3,315.0 | 257 ± 15<br>Mdn 252, IQR 30 | 257 ± 15<br>Mdn 252, IQR 30 | 305 ± 15<br>Mdn 300, IQR 30 |
| query_pattern, repeating, n 1000–10000 | Aho-Corasick | 30 | 321.77 ± 124.52<br>Mdn 340.54, IQR 171.46 | 1.803 ± 0.335<br>Mdn 1.689, IQR 0.656 | 319.97 ± 124.45<br>Mdn 339.02, IQR 171.96 | 6,167.3 ± 2,392.8<br>Mdn 6,596.5, IQR 3,312.2 | 2,493 ± 526<br>Mdn 2,280, IQR 1,092 | 2,493 ± 526<br>Mdn 2,280, IQR 1,092 | 3,253 ± 526<br>Mdn 3,040, IQR 1,092 |
| alphabet, |Σ|=2, n 10–100 | Naive | 30 | 4.05 ± 1.88<br>Mdn 3.96, IQR 3.12 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 4.03 ± 1.88<br>Mdn 3.94, IQR 3.12 | 98.2 ± 48.3<br>Mdn 95.5, IQR 77.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=2, n 10–100 | KMP | 30 | 3.58 ± 1.34<br>Mdn 3.65, IQR 2.10 | 0.486 ± 0.128<br>Mdn 0.479, IQR 0.244 | 3.09 ± 1.35<br>Mdn 3.19, IQR 2.13 | 82.8 ± 33.6<br>Mdn 82.5, IQR 49.5 | 258 ± 16<br>Mdn 256, IQR 30 | 258 ± 16<br>Mdn 256, IQR 30 | 306 ± 16<br>Mdn 304, IQR 30 |
| alphabet, |Σ|=2, n 10–100 | Aho-Corasick | 30 | 5.35 ± 1.56<br>Mdn 5.22, IQR 2.26 | 1.883 ± 0.429<br>Mdn 1.790, IQR 0.869 | 3.46 ± 1.52<br>Mdn 3.43, IQR 2.50 | 93.7 ± 34.1<br>Mdn 92.0, IQR 47.2 | 2,541 ± 560<br>Mdn 2,400, IQR 1,092 | 2,541 ± 560<br>Mdn 2,400, IQR 1,092 | 3,301 ± 560<br>Mdn 3,160, IQR 1,092 |
| alphabet, |Σ|=2, n 100–1000 | Naive | 30 | 54.17 ± 25.81<br>Mdn 58.52, IQR 49.58 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.001 | 54.15 ± 25.81<br>Mdn 58.50, IQR 49.58 | 1,230.5 ± 550.8<br>Mdn 1,340.5, IQR 1,055.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=2, n 100–1000 | KMP | 30 | 37.45 ± 16.64<br>Mdn 39.34, IQR 30.38 | 0.469 ± 0.125<br>Mdn 0.494, IQR 0.226 | 36.98 ± 16.62<br>Mdn 38.76, IQR 30.17 | 885.3 ± 382.7<br>Mdn 947.0, IQR 698.5 | 256 ± 14<br>Mdn 256, IQR 30 | 256 ± 14<br>Mdn 256, IQR 30 | 304 ± 14<br>Mdn 304, IQR 30 |
| alphabet, |Σ|=2, n 100–1000 | Aho-Corasick | 30 | 43.03 ± 18.46<br>Mdn 46.25, IQR 34.51 | 1.832 ± 0.393<br>Mdn 1.813, IQR 0.750 | 41.20 ± 18.37<br>Mdn 44.08, IQR 33.72 | 903.0 ± 384.7<br>Mdn 961.5, IQR 711.0 | 2,490 ± 522<br>Mdn 2,400, IQR 1,092 | 2,490 ± 522<br>Mdn 2,400, IQR 1,092 | 3,250 ± 522<br>Mdn 3,160, IQR 1,092 |
| alphabet, |Σ|=2, n 1000–10000 | Naive | 30 | 567.93 ± 257.50<br>Mdn 646.73, IQR 448.92 | 0.024 ± 0.003<br>Mdn 0.025, IQR 0.005 | 567.90 ± 257.50<br>Mdn 646.70, IQR 448.92 | 12,077.2 ± 5,416.3<br>Mdn 13,683.5, IQR 9,281.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=2, n 1000–10000 | KMP | 30 | 368.00 ± 163.67<br>Mdn 422.49, IQR 281.10 | 0.538 ± 0.101<br>Mdn 0.552, IQR 0.120 | 367.46 ± 163.68<br>Mdn 421.83, IQR 281.12 | 8,547.4 ± 3,808.4<br>Mdn 9,899.5, IQR 6,503.2 | 263 ± 13<br>Mdn 264, IQR 14 | 263 ± 13<br>Mdn 264, IQR 14 | 311 ± 13<br>Mdn 312, IQR 14 |
| alphabet, |Σ|=2, n 1000–10000 | Aho-Corasick | 30 | 407.51 ± 180.62<br>Mdn 460.93, IQR 315.28 | 2.103 ± 0.348<br>Mdn 2.164, IQR 0.429 | 405.41 ± 180.61<br>Mdn 458.44, IQR 315.70 | 8,604.4 ± 3,821.0<br>Mdn 9,967.0, IQR 6,583.5 | 2,757 ± 467<br>Mdn 2,832, IQR 564 | 2,757 ± 467<br>Mdn 2,832, IQR 564 | 3,517 ± 467<br>Mdn 3,592, IQR 564 |
| alphabet, |Σ|=4, n 10–100 | Naive | 30 | 3.14 ± 1.30<br>Mdn 3.39, IQR 1.64 | 0.023 ± 0.002<br>Mdn 0.022, IQR 0.000 | 3.11 ± 1.30<br>Mdn 3.36, IQR 1.64 | 75.9 ± 33.9<br>Mdn 82.0, IQR 43.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=4, n 10–100 | KMP | 30 | 3.28 ± 1.17<br>Mdn 3.45, IQR 1.32 | 0.456 ± 0.086<br>Mdn 0.465, IQR 0.124 | 2.83 ± 1.16<br>Mdn 3.05, IQR 1.33 | 79.0 ± 31.3<br>Mdn 85.0, IQR 37.8 | 260 ± 14<br>Mdn 256, IQR 24 | 260 ± 14<br>Mdn 256, IQR 24 | 308 ± 14<br>Mdn 304, IQR 24 |
| alphabet, |Σ|=4, n 10–100 | Aho-Corasick | 30 | 5.29 ± 1.38<br>Mdn 5.25, IQR 1.70 | 1.910 ± 0.361<br>Mdn 1.831, IQR 0.619 | 3.38 ± 1.38<br>Mdn 3.69, IQR 1.68 | 88.7 ± 31.5<br>Mdn 93.0, IQR 38.2 | 2,602 ± 509<br>Mdn 2,400, IQR 912 | 2,602 ± 509<br>Mdn 2,400, IQR 912 | 3,362 ± 509<br>Mdn 3,160, IQR 912 |
| alphabet, |Σ|=4, n 100–1000 | Naive | 30 | 28.71 ± 15.64<br>Mdn 27.93, IQR 20.08 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 28.69 ± 15.64<br>Mdn 27.91, IQR 20.08 | 664.5 ± 337.3<br>Mdn 652.5, IQR 417.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=4, n 100–1000 | KMP | 30 | 24.32 ± 12.42<br>Mdn 23.69, IQR 15.77 | 0.478 ± 0.090<br>Mdn 0.482, IQR 0.110 | 23.85 ± 12.42<br>Mdn 23.23, IQR 15.70 | 626.5 ± 314.7<br>Mdn 610.0, IQR 397.5 | 261 ± 12<br>Mdn 256, IQR 16 | 261 ± 12<br>Mdn 256, IQR 16 | 309 ± 12<br>Mdn 304, IQR 16 |
| alphabet, |Σ|=4, n 100–1000 | Aho-Corasick | 30 | 30.70 ± 14.96<br>Mdn 30.25, IQR 18.63 | 1.935 ± 0.339<br>Mdn 1.865, IQR 0.478 | 28.77 ± 14.95<br>Mdn 27.82, IQR 18.31 | 636.6 ± 314.8<br>Mdn 622.5, IQR 399.2 | 2,626 ± 452<br>Mdn 2,400, IQR 672 | 2,626 ± 452<br>Mdn 2,400, IQR 672 | 3,386 ± 452<br>Mdn 3,160, IQR 672 |
| alphabet, |Σ|=4, n 1000–10000 | Naive | 30 | 379.16 ± 171.86<br>Mdn 387.54, IQR 330.73 | 0.026 ± 0.003<br>Mdn 0.027, IQR 0.003 | 379.13 ± 171.86<br>Mdn 387.52, IQR 330.73 | 8,058.1 ± 3,626.2<br>Mdn 8,163.5, IQR 6,950.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=4, n 1000–10000 | KMP | 30 | 299.12 ± 134.91<br>Mdn 301.28, IQR 254.88 | 0.494 ± 0.110<br>Mdn 0.525, IQR 0.168 | 298.62 ± 134.93<br>Mdn 300.85, IQR 255.04 | 7,515.0 ± 3,375.5<br>Mdn 7,628.5, IQR 6,508.0 | 264 ± 14<br>Mdn 268, IQR 24 | 264 ± 14<br>Mdn 268, IQR 24 | 312 ± 14<br>Mdn 316, IQR 24 |
| alphabet, |Σ|=4, n 1000–10000 | Aho-Corasick | 30 | 358.56 ± 161.25<br>Mdn 365.32, IQR 305.77 | 2.129 ± 0.419<br>Mdn 2.210, IQR 0.681 | 356.43 ± 161.31<br>Mdn 363.41, IQR 306.07 | 7,526.9 ± 3,375.8<br>Mdn 7,638.5, IQR 6,507.5 | 2,768 ± 503<br>Mdn 2,952, IQR 912 | 2,768 ± 503<br>Mdn 2,952, IQR 912 | 3,528 ± 503<br>Mdn 3,712, IQR 912 |
| alphabet, |Σ|=26, n 10–100 | Naive | 30 | 2.83 ± 1.01<br>Mdn 2.94, IQR 1.37 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 2.81 ± 1.01<br>Mdn 2.92, IQR 1.37 | 68.9 ± 26.5<br>Mdn 73.0, IQR 37.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=26, n 10–100 | KMP | 30 | 2.93 ± 0.89<br>Mdn 3.04, IQR 1.26 | 0.446 ± 0.067<br>Mdn 0.462, IQR 0.095 | 2.48 ± 0.88<br>Mdn 2.61, IQR 1.31 | 76.4 ± 26.6<br>Mdn 80.5, IQR 36.5 | 267 ± 12<br>Mdn 268, IQR 24 | 267 ± 12<br>Mdn 268, IQR 24 | 315 ± 12<br>Mdn 316, IQR 24 |
| alphabet, |Σ|=26, n 10–100 | Aho-Corasick | 30 | 5.45 ± 1.29<br>Mdn 5.69, IQR 1.68 | 2.066 ± 0.311<br>Mdn 2.096, IQR 0.604 | 3.38 ± 1.24<br>Mdn 3.51, IQR 1.69 | 86.1 ± 26.9<br>Mdn 90.0, IQR 36.8 | 2,864 ± 442<br>Mdn 2,952, IQR 912 | 2,864 ± 442<br>Mdn 2,952, IQR 912 | 3,624 ± 442<br>Mdn 3,712, IQR 912 |
| alphabet, |Σ|=26, n 100–1000 | Naive | 30 | 21.92 ± 12.08<br>Mdn 20.14, IQR 22.61 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 21.90 ± 12.08<br>Mdn 20.12, IQR 22.61 | 511.8 ± 260.9<br>Mdn 477.5, IQR 472.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=26, n 100–1000 | KMP | 30 | 18.76 ± 9.73<br>Mdn 17.44, IQR 17.47 | 0.425 ± 0.075<br>Mdn 0.444, IQR 0.093 | 18.33 ± 9.72<br>Mdn 17.01, IQR 17.54 | 518.2 ± 260.4<br>Mdn 484.5, IQR 464.8 | 263 ± 15<br>Mdn 268, IQR 22 | 263 ± 15<br>Mdn 268, IQR 22 | 311 ± 15<br>Mdn 316, IQR 22 |
| alphabet, |Σ|=26, n 100–1000 | Aho-Corasick | 30 | 27.02 ± 13.08<br>Mdn 25.04, IQR 22.51 | 1.971 ± 0.370<br>Mdn 2.083, IQR 0.600 | 25.05 ± 13.01<br>Mdn 23.07, IQR 22.66 | 527.4 ± 260.8<br>Mdn 494.0, IQR 461.0 | 2,746 ± 523<br>Mdn 2,952, IQR 852 | 2,746 ± 523<br>Mdn 2,952, IQR 852 | 3,506 ± 523<br>Mdn 3,712, IQR 852 |
| alphabet, |Σ|=26, n 1000–10000 | Naive | 30 | 283.38 ± 128.40<br>Mdn 267.45, IQR 230.71 | 0.025 ± 0.003<br>Mdn 0.025, IQR 0.006 | 283.36 ± 128.40<br>Mdn 267.43, IQR 230.72 | 6,032.2 ± 2,694.8<br>Mdn 5,733.5, IQR 4,845.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=26, n 1000–10000 | KMP | 30 | 226.90 ± 101.77<br>Mdn 215.02, IQR 183.46 | 0.427 ± 0.064<br>Mdn 0.442, IQR 0.085 | 226.47 ± 101.79<br>Mdn 214.58, IQR 183.55 | 6,029.5 ± 2,689.3<br>Mdn 5,730.5, IQR 4,834.0 | 262 ± 13<br>Mdn 264, IQR 24 | 262 ± 13<br>Mdn 264, IQR 24 | 310 ± 13<br>Mdn 312, IQR 24 |
| alphabet, |Σ|=26, n 1000–10000 | Aho-Corasick | 30 | 309.03 ± 136.88<br>Mdn 293.29, IQR 242.77 | 2.025 ± 0.346<br>Mdn 2.113, IQR 0.580 | 307.00 ± 137.02<br>Mdn 291.22, IQR 243.29 | 6,038.5 ± 2,688.6<br>Mdn 5,740.0, IQR 4,830.8 | 2,712 ± 486<br>Mdn 2,832, IQR 912 | 2,712 ± 486<br>Mdn 2,832, IQR 912 | 3,472 ± 486<br>Mdn 3,592, IQR 912 |
| alphabet, |Σ|=full, n 10–100 | Naive | 30 | 2.16 ± 0.95<br>Mdn 2.27, IQR 1.25 | 0.022 ± 0.001<br>Mdn 0.022, IQR 0.000 | 2.14 ± 0.95<br>Mdn 2.24, IQR 1.25 | 48.6 ± 23.2<br>Mdn 51.5, IQR 31.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=full, n 10–100 | KMP | 30 | 2.31 ± 0.83<br>Mdn 2.35, IQR 1.08 | 0.401 ± 0.084<br>Mdn 0.394, IQR 0.138 | 1.90 ± 0.82<br>Mdn 1.97, IQR 1.10 | 54.8 ± 23.2<br>Mdn 60.0, IQR 30.8 | 257 ± 15<br>Mdn 256, IQR 30 | 257 ± 15<br>Mdn 256, IQR 30 | 317 ± 24<br>Mdn 316, IQR 34 |
| alphabet, |Σ|=full, n 10–100 | Aho-Corasick | 30 | 4.41 ± 1.20<br>Mdn 4.28, IQR 1.73 | 1.833 ± 0.407<br>Mdn 1.768, IQR 0.729 | 2.57 ± 1.14<br>Mdn 2.68, IQR 1.44 | 63.0 ± 23.4<br>Mdn 66.0, IQR 34.2 | 2,496 ± 531<br>Mdn 2,400, IQR 1,092 | 2,526 ± 549<br>Mdn 2,400, IQR 1,047 | 3,286 ± 549<br>Mdn 3,160, IQR 1,047 |
| alphabet, |Σ|=full, n 100–1000 | Naive | 30 | 26.05 ± 13.48<br>Mdn 26.23, IQR 26.32 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 26.02 ± 13.48<br>Mdn 26.21, IQR 26.32 | 574.4 ± 278.5<br>Mdn 584.0, IQR 531.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=full, n 100–1000 | KMP | 30 | 21.90 ± 10.77<br>Mdn 21.91, IQR 20.19 | 0.405 ± 0.073<br>Mdn 0.421, IQR 0.120 | 21.49 ± 10.77<br>Mdn 21.49, IQR 20.37 | 580.7 ± 278.4<br>Mdn 590.5, IQR 527.0 | 258 ± 14<br>Mdn 260, IQR 30 | 258 ± 14<br>Mdn 260, IQR 30 | 317 ± 19<br>Mdn 316, IQR 24 |
| alphabet, |Σ|=full, n 100–1000 | Aho-Corasick | 30 | 31.87 ± 14.91<br>Mdn 32.57, IQR 27.24 | 1.859 ± 0.360<br>Mdn 1.924, IQR 0.671 | 30.01 ± 14.90<br>Mdn 30.67, IQR 28.19 | 588.9 ± 278.5<br>Mdn 599.0, IQR 522.2 | 2,568 ± 506<br>Mdn 2,616, IQR 1,092 | 2,596 ± 507<br>Mdn 2,706, IQR 1,047 | 3,356 ± 507<br>Mdn 3,466, IQR 1,047 |
| alphabet, |Σ|=full, n 1000–10000 | Naive | 30 | 249.38 ± 116.01<br>Mdn 232.93, IQR 142.69 | 0.026 ± 0.002<br>Mdn 0.026, IQR 0.001 | 249.35 ± 116.01<br>Mdn 232.90, IQR 142.69 | 5,046.0 ± 2,259.7<br>Mdn 4,594.0, IQR 2,951.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=full, n 1000–10000 | KMP | 30 | 196.17 ± 89.58<br>Mdn 182.47, IQR 116.42 | 0.423 ± 0.077<br>Mdn 0.400, IQR 0.126 | 195.75 ± 89.58<br>Mdn 182.08, IQR 116.38 | 5,052.0 ± 2,259.4<br>Mdn 4,600.0, IQR 2,953.8 | 261 ± 14<br>Mdn 256, IQR 24 | 261 ± 14<br>Mdn 256, IQR 24 | 321 ± 26<br>Mdn 318, IQR 27 |
| alphabet, |Σ|=full, n 1000–10000 | Aho-Corasick | 30 | 273.37 ± 122.83<br>Mdn 248.07, IQR 160.68 | 2.010 ± 0.372<br>Mdn 1.922, IQR 0.608 | 271.36 ± 122.82<br>Mdn 246.36, IQR 160.49 | 5,060.7 ± 2,259.4<br>Mdn 4,608.0, IQR 2,954.8 | 2,627 ± 499<br>Mdn 2,400, IQR 912 | 2,655 ± 513<br>Mdn 2,460, IQR 897 | 3,415 ± 513<br>Mdn 3,220, IQR 897 |
| positive_control, n 10–100 | Naive | 30 | 17.65 ± 0.23<br>Mdn 17.62, IQR 0.35 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 17.63 ± 0.23<br>Mdn 17.60, IQR 0.35 | 560.0 ± 0.0<br>Mdn 560.0, IQR 0.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| positive_control, n 10–100 | KMP | 30 | 6.16 ± 0.06<br>Mdn 6.17, IQR 0.08 | 0.653 ± 0.013<br>Mdn 0.651, IQR 0.018 | 5.51 ± 0.06<br>Mdn 5.52, IQR 0.05 | 160.0 ± 0.0<br>Mdn 160.0, IQR 0.0 | 264 ± 0<br>Mdn 264, IQR 0 | 264 ± 0<br>Mdn 264, IQR 0 | 312 ± 0<br>Mdn 312, IQR 0 |
| positive_control, n 10–100 | Aho-Corasick | 30 | 7.31 ± 0.10<br>Mdn 7.33, IQR 0.14 | 2.116 ± 0.029<br>Mdn 2.121, IQR 0.020 | 5.20 ± 0.08<br>Mdn 5.21, IQR 0.12 | 174.0 ± 0.0<br>Mdn 174.0, IQR 0.0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 3,592 ± 0<br>Mdn 3,592, IQR 0 |
| positive_control, n 100–1000 | Naive | 30 | 209.26 ± 1.86<br>Mdn 209.14, IQR 1.26 | 0.022 ± 0.000<br>Mdn 0.022, IQR 0.000 | 209.24 ± 1.86<br>Mdn 209.12, IQR 1.26 | 5,872.0 ± 0.0<br>Mdn 5,872.0, IQR 0.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| positive_control, n 100–1000 | KMP | 30 | 56.37 ± 0.75<br>Mdn 56.38, IQR 0.62 | 0.652 ± 0.020<br>Mdn 0.650, IQR 0.019 | 55.72 ± 0.74<br>Mdn 55.73, IQR 0.63 | 1,488.0 ± 0.0<br>Mdn 1,488.0, IQR 0.0 | 264 ± 0<br>Mdn 264, IQR 0 | 264 ± 0<br>Mdn 264, IQR 0 | 312 ± 0<br>Mdn 312, IQR 0 |
| positive_control, n 100–1000 | Aho-Corasick | 30 | 54.76 ± 0.96<br>Mdn 54.82, IQR 1.56 | 2.102 ± 0.035<br>Mdn 2.102, IQR 0.026 | 52.66 ± 0.94<br>Mdn 52.72, IQR 1.55 | 1,502.0 ± 0.0<br>Mdn 1,502.0, IQR 0.0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 3,592 ± 0<br>Mdn 3,592, IQR 0 |
| positive_control, n 1000–10000 | Naive | 30 | 648.51 ± 6.15<br>Mdn 648.51, IQR 6.23 | 0.025 ± 0.003<br>Mdn 0.025, IQR 0.005 | 648.48 ± 6.15<br>Mdn 648.49, IQR 6.23 | 16,490.0 ± 0.0<br>Mdn 16,490.0, IQR 0.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| positive_control, n 1000–10000 | KMP | 30 | 254.11 ± 6.21<br>Mdn 253.12, IQR 3.61 | 0.443 ± 0.020<br>Mdn 0.437, IQR 0.011 | 253.66 ± 6.21<br>Mdn 252.68, IQR 3.60 | 6,607.0 ± 0.0<br>Mdn 6,607.0, IQR 0.0 | 240 ± 0<br>Mdn 240, IQR 0 | 240 ± 0<br>Mdn 240, IQR 0 | 288 ± 0<br>Mdn 288, IQR 0 |
| positive_control, n 1000–10000 | Aho-Corasick | 30 | 239.13 ± 3.55<br>Mdn 238.75, IQR 3.69 | 1.544 ± 0.081<br>Mdn 1.528, IQR 0.043 | 237.59 ± 3.54<br>Mdn 237.23, IQR 3.58 | 6,615.0 ± 0.0<br>Mdn 6,615.0, IQR 0.0 | 1,920 ± 0<br>Mdn 1,920, IQR 0 | 1,920 ± 0<br>Mdn 1,920, IQR 0 | 2,680 ± 0<br>Mdn 2,680, IQR 0 |

*Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1).*
