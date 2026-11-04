# Run report: replication machine

Generated 2026-11-04 09:20:37 UTC by `run_benchmark.py`. Raw data: `raw_runs.csv` (5,130 rows).

## Environment

| Item | Value |
| --- | --- |
| Operating system | CachyOS (kernel 7.3.1-1-cachyos) |
| Platform string | Linux-7.3.1-1-cachyos-x86_64-with-glibc2.44 |
| CPU model | Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz |
| Cores (physical / logical) | 4 / 8 |
| CPU frequency as reported by psutil (current / max, MHz) | 2,158 / 4,500 |
| RAM | 15.4 GiB |
| Python | CPython 3.12.13 |
| Python build | main Aug  7 2026 02:25:39; Clang 22.1.3  |
| Packages | numpy 2.5.4, scipy 1.18.1, pandas 3.1.0, matplotlib 3.11.2, psutil 7.2.2, pytest 9.2.0 |
| Timer | time.perf_counter (clock_gettime(CLOCK_MONOTONIC), resolution 1 ns) |
| Pinned core | 2 — OK (cpu_affinity set to [2]) |
| Priority raised | yes (nice -5) |

**Pinned core type.** Logical core 2 is a **single core type (homogeneous CPU)** core. Detected with: Linux sysfs L3 cache size per logical CPU (larger L3 = faster core type).

| Core type | Class value | Logical processors |
| --- | ---: | --- |
| single core type (homogeneous CPU) | 8192 | 0, 1, 2, 3, 4, 5, 6, 7 |

psutil per-core max frequency (MHz): 4500 for every core. On Windows psutil only reports the nominal base clock, so this cannot tell core types apart.

**Run sessions** (a resumed run has several):

| Session | Start (UTC) | End (UTC) | Duration | Jobs run | Interrupted? | Priority raised? |
| ---: | --- | --- | ---: | ---: | :---: | :---: |
| 1 | 2026-11-04T09:08:23+00:00 | 2026-11-04T09:16:29+00:00 | 8m 06s | 5,130 | no | yes |

Total measured duration: **8m 06s**

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
| Machine label | ✅ PASS | replication |

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

`perf_counter` resolution on this machine: 1 ns. A timing is flagged when the whole timed interval (min per-call time × R) is below 1,000 × resolution (= 1 µs), i.e. when clock quantisation could exceed 0.1 %, or when a value is 0.

| Algorithm | Text length | Phase | R | Min per call (µs) | Median per call (µs) | Min timed interval (µs) | Zeros | Flagged? |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | :---: |
| Naive | 10–100 | prep | 10000 | 0.0315 | 0.0320 | 315.16 | 0 | no |
| Naive | 10–100 | search | 10000 | 0.4541 | 4.6671 | 4,540.66 | 0 | no |
| Naive | 100–1000 | prep | 1000 | 0.0299 | 0.0307 | 29.88 | 0 | no |
| Naive | 100–1000 | search | 1000 | 4.6773 | 51.1110 | 4,677.28 | 0 | no |
| Naive | 1000–10000 | prep | 100 | 0.0271 | 0.0334 | 2.71 | 0 | no |
| Naive | 1000–10000 | search | 100 | 56.9329 | 614.9173 | 5,693.29 | 0 | no |
| KMP | 10–100 | prep | 10000 | 0.2168 | 0.7766 | 2,168.25 | 0 | no |
| KMP | 10–100 | search | 10000 | 0.6649 | 4.3482 | 6,649.20 | 0 | no |
| KMP | 100–1000 | prep | 1000 | 0.2155 | 0.7348 | 215.51 | 0 | no |
| KMP | 100–1000 | search | 1000 | 4.7835 | 44.3353 | 4,783.52 | 0 | no |
| KMP | 1000–10000 | prep | 100 | 0.2304 | 0.7282 | 23.04 | 0 | no |
| KMP | 1000–10000 | search | 100 | 51.5941 | 471.5604 | 5,159.41 | 0 | no |
| Aho-Corasick | 10–100 | prep | 10000 | 0.7311 | 3.4933 | 7,310.84 | 0 | no |
| Aho-Corasick | 10–100 | search | 10000 | 0.9182 | 5.0492 | 9,181.82 | 0 | no |
| Aho-Corasick | 100–1000 | prep | 1000 | 0.7195 | 3.1445 | 719.45 | 0 | no |
| Aho-Corasick | 100–1000 | search | 1000 | 7.0854 | 49.4736 | 7,085.45 | 0 | no |
| Aho-Corasick | 1000–10000 | prep | 100 | 0.7617 | 3.2663 | 76.17 | 0 | no |
| Aho-Corasick | 1000–10000 | search | 100 | 81.0166 | 504.3183 | 8,101.66 | 0 | no |


## Summary tables

### Core grid: random vs. narrative text

*Pooled over the 3 query lengths and both query counts.*

**Total time (prep + search)** (µs per call)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 9.74 ± 8.19<br>Mdn 5.33, IQR 13.23 | 9.85 ± 8.31<br>Mdn 5.51, IQR 13.42 |
| Naive | 100–1000 | 108.99 ± 99.09<br>Mdn 54.93, IQR 152.13 | 107.99 ± 103.36<br>Mdn 59.02, IQR 142.49 |
| Naive | 1000–10000 | 1,240.89 ± 1,060.32<br>Mdn 682.81, IQR 1,618.82 | 1,210.30 ± 1,075.31<br>Mdn 699.19, IQR 1,400.61 |
| KMP | 10–100 | 11.04 ± 8.94<br>Mdn 5.88, IQR 14.73 | 11.13 ± 8.70<br>Mdn 6.54, IQR 15.67 |
| KMP | 100–1000 | 98.00 ± 87.73<br>Mdn 50.38, IQR 135.77 | 96.84 ± 90.17<br>Mdn 52.28, IQR 127.91 |
| KMP | 1000–10000 | 1,049.43 ± 894.60<br>Mdn 557.43, IQR 1,382.15 | 1,029.15 ± 914.47<br>Mdn 596.46, IQR 1,253.51 |
| Aho-Corasick | 10–100 | 13.27 ± 8.62<br>Mdn 10.00, IQR 10.23 | 13.18 ± 7.87<br>Mdn 10.26, IQR 10.74 |
| Aho-Corasick | 100–1000 | 58.39 ± 27.31<br>Mdn 59.37, IQR 43.27 | 57.46 ± 28.75<br>Mdn 54.32, IQR 46.04 |
| Aho-Corasick | 1000–10000 | 548.87 ± 246.50<br>Mdn 564.54, IQR 412.58 | 537.18 ± 273.50<br>Mdn 558.18, IQR 448.32 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 0.034 ± 0.003<br>Mdn 0.032, IQR 0.004 |
| Naive | 100–1000 | 0.032 ± 0.006<br>Mdn 0.031, IQR 0.000 | 0.032 ± 0.005<br>Mdn 0.031, IQR 0.001 |
| Naive | 1000–10000 | 0.034 ± 0.015<br>Mdn 0.033, IQR 0.005 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.005 |
| KMP | 10–100 | 1.832 ± 1.574<br>Mdn 1.271, IQR 2.048 | 1.836 ± 1.586<br>Mdn 1.250, IQR 2.155 |
| KMP | 100–1000 | 1.758 ± 1.506<br>Mdn 1.243, IQR 2.019 | 1.741 ± 1.479<br>Mdn 1.199, IQR 1.863 |
| KMP | 1000–10000 | 1.756 ± 1.460<br>Mdn 1.222, IQR 1.933 | 1.776 ± 1.521<br>Mdn 1.149, IQR 1.904 |
| Aho-Corasick | 10–100 | 8.347 ± 7.745<br>Mdn 5.270, IQR 8.941 | 8.117 ± 7.407<br>Mdn 4.916, IQR 9.387 |
| Aho-Corasick | 100–1000 | 8.466 ± 8.290<br>Mdn 4.766, IQR 9.642 | 8.171 ± 7.881<br>Mdn 4.732, IQR 8.311 |
| Aho-Corasick | 1000–10000 | 8.079 ± 7.586<br>Mdn 4.845, IQR 9.076 | 8.036 ± 7.649<br>Mdn 4.718, IQR 8.414 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Search time** (µs per call)

| Algorithm | Text length | Random | Narrative |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 9.71 ± 8.19<br>Mdn 5.30, IQR 13.22 | 9.82 ± 8.31<br>Mdn 5.48, IQR 13.41 |
| Naive | 100–1000 | 108.96 ± 99.09<br>Mdn 54.90, IQR 152.13 | 107.96 ± 103.36<br>Mdn 58.99, IQR 142.49 |
| Naive | 1000–10000 | 1,240.85 ± 1,060.32<br>Mdn 682.79, IQR 1,618.82 | 1,210.27 ± 1,075.31<br>Mdn 699.16, IQR 1,400.61 |
| KMP | 10–100 | 9.21 ± 7.74<br>Mdn 4.95, IQR 12.83 | 9.30 ± 7.72<br>Mdn 5.23, IQR 12.96 |
| KMP | 100–1000 | 96.24 ± 86.79<br>Mdn 49.51, IQR 132.95 | 95.10 ± 89.34<br>Mdn 50.66, IQR 126.46 |
| KMP | 1000–10000 | 1,047.67 ± 893.69<br>Mdn 556.61, IQR 1,380.74 | 1,027.38 ± 913.58<br>Mdn 594.53, IQR 1,251.14 |
| Aho-Corasick | 10–100 | 4.92 ± 2.07<br>Mdn 4.68, IQR 3.24 | 5.06 ± 2.19<br>Mdn 5.10, IQR 3.71 |
| Aho-Corasick | 100–1000 | 49.92 ± 24.53<br>Mdn 51.27, IQR 42.72 | 49.29 ± 26.68<br>Mdn 47.40, IQR 44.82 |
| Aho-Corasick | 1000–10000 | 540.79 ± 245.26<br>Mdn 558.50, IQR 410.91 | 529.14 ± 272.65<br>Mdn 548.58, IQR 449.69 |

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
| Naive | 10–100 | 3.22 ± 1.33<br>Mdn 3.24, IQR 2.13 | 16.37 ± 6.89<br>Mdn 16.76, IQR 11.77 |
| Naive | 100–1000 | 34.06 ± 18.95<br>Mdn 34.21, IQR 33.94 | 182.93 ± 94.87<br>Mdn 182.42, IQR 174.00 |
| Naive | 1000–10000 | 408.34 ± 209.12<br>Mdn 434.19, IQR 365.53 | 2,042.85 ± 945.54<br>Mdn 2,018.03, IQR 1,665.08 |
| KMP | 10–100 | 3.72 ± 1.30<br>Mdn 3.80, IQR 1.91 | 18.45 ± 6.69<br>Mdn 19.30, IQR 11.38 |
| KMP | 100–1000 | 30.71 ± 16.22<br>Mdn 29.94, IQR 28.54 | 164.12 ± 81.33<br>Mdn 164.31, IQR 144.70 |
| KMP | 1000–10000 | 344.41 ± 174.69<br>Mdn 364.52, IQR 312.96 | 1,734.17 ± 796.97<br>Mdn 1,703.84, IQR 1,389.19 |
| Aho-Corasick | 10–100 | 7.64 ± 2.59<br>Mdn 7.51, IQR 3.62 | 18.81 ± 8.18<br>Mdn 17.89, IQR 12.48 |
| Aho-Corasick | 100–1000 | 47.31 ± 23.02<br>Mdn 47.33, IQR 40.31 | 68.54 ± 28.56<br>Mdn 69.50, IQR 47.41 |
| Aho-Corasick | 1000–10000 | 498.79 ± 247.87<br>Mdn 534.98, IQR 470.69 | 587.26 ± 265.06<br>Mdn 576.32, IQR 463.15 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0.033 ± 0.003<br>Mdn 0.032, IQR 0.004 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 |
| Naive | 100–1000 | 0.032 ± 0.005<br>Mdn 0.031, IQR 0.001 | 0.032 ± 0.005<br>Mdn 0.031, IQR 0.000 |
| Naive | 1000–10000 | 0.033 ± 0.011<br>Mdn 0.033, IQR 0.005 | 0.033 ± 0.011<br>Mdn 0.034, IQR 0.004 |
| KMP | 10–100 | 0.661 ± 0.313<br>Mdn 0.608, IQR 0.477 | 3.007 ± 1.458<br>Mdn 2.694, IQR 2.945 |
| KMP | 100–1000 | 0.645 ± 0.294<br>Mdn 0.622, IQR 0.428 | 2.854 ± 1.384<br>Mdn 2.539, IQR 2.827 |
| KMP | 1000–10000 | 0.659 ± 0.288<br>Mdn 0.610, IQR 0.413 | 2.873 ± 1.378<br>Mdn 2.539, IQR 2.742 |
| Aho-Corasick | 10–100 | 3.157 ± 1.730<br>Mdn 2.815, IQR 2.736 | 13.308 ± 7.751<br>Mdn 12.089, IQR 15.276 |
| Aho-Corasick | 100–1000 | 2.902 ± 1.535<br>Mdn 2.754, IQR 2.213 | 13.736 ± 8.337<br>Mdn 11.552, IQR 17.020 |
| Aho-Corasick | 1000–10000 | 2.900 ± 1.520<br>Mdn 2.725, IQR 2.164 | 13.215 ± 7.763<br>Mdn 11.421, IQR 15.595 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 180.*


**Search time** (µs per call)

| Algorithm | Text length | 1 query | 5 queries |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 3.19 ± 1.33<br>Mdn 3.20, IQR 2.13 | 16.34 ± 6.89<br>Mdn 16.73, IQR 11.77 |
| Naive | 100–1000 | 34.02 ± 18.95<br>Mdn 34.18, IQR 33.94 | 182.90 ± 94.87<br>Mdn 182.39, IQR 174.02 |
| Naive | 1000–10000 | 408.31 ± 209.12<br>Mdn 434.16, IQR 365.53 | 2,042.81 ± 945.54<br>Mdn 2,018.00, IQR 1,665.09 |
| KMP | 10–100 | 3.06 ± 1.24<br>Mdn 3.09, IQR 1.92 | 15.45 ± 6.39<br>Mdn 16.04, IQR 11.28 |
| KMP | 100–1000 | 30.07 ± 16.21<br>Mdn 29.26, IQR 28.29 | 161.27 ± 81.22<br>Mdn 161.21, IQR 145.63 |
| KMP | 1000–10000 | 343.75 ± 174.68<br>Mdn 363.61, IQR 312.93 | 1,731.30 ± 796.86<br>Mdn 1,700.72, IQR 1,390.53 |
| Aho-Corasick | 10–100 | 4.48 ± 1.90<br>Mdn 4.58, IQR 2.96 | 5.50 ± 2.23<br>Mdn 5.45, IQR 3.61 |
| Aho-Corasick | 100–1000 | 44.40 ± 22.92<br>Mdn 44.64, IQR 40.58 | 54.81 ± 27.09<br>Mdn 54.62, IQR 49.26 |
| Aho-Corasick | 1000–10000 | 495.88 ± 247.92<br>Mdn 531.18, IQR 470.30 | 574.05 ± 264.61<br>Mdn 566.35, IQR 456.64 |

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
| Naive | 10–100 | 2.57 ± 1.30<br>Mdn 2.48, IQR 2.11 | 2.74 ± 1.33<br>Mdn 2.61, IQR 2.02 |
| Naive | 100–1000 | 29.64 ± 16.90<br>Mdn 26.74, IQR 22.18 | 31.19 ± 17.25<br>Mdn 29.87, IQR 31.73 |
| Naive | 1000–10000 | 330.78 ± 195.73<br>Mdn 377.69, IQR 334.65 | 417.10 ± 167.35<br>Mdn 454.54, IQR 225.65 |
| KMP | 10–100 | 3.28 ± 1.21<br>Mdn 3.23, IQR 2.13 | 3.47 ± 1.25<br>Mdn 3.35, IQR 1.86 |
| KMP | 100–1000 | 27.14 ± 14.43<br>Mdn 24.35, IQR 18.21 | 28.08 ± 14.37<br>Mdn 26.68, IQR 25.96 |
| KMP | 1000–10000 | 280.91 ± 167.49<br>Mdn 326.00, IQR 268.09 | 348.32 ± 139.57<br>Mdn 378.71, IQR 201.16 |
| Aho-Corasick | 10–100 | 6.92 ± 1.91<br>Mdn 7.06, IQR 3.25 | 7.26 ± 1.97<br>Mdn 7.32, IQR 3.37 |
| Aho-Corasick | 100–1000 | 42.20 ± 21.03<br>Mdn 38.17, IQR 23.68 | 43.46 ± 20.68<br>Mdn 43.20, IQR 37.30 |
| Aho-Corasick | 1000–10000 | 413.35 ± 242.87<br>Mdn 460.93, IQR 386.02 | 505.49 ± 197.82<br>Mdn 545.48, IQR 263.98 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 0.034 ± 0.002<br>Mdn 0.032, IQR 0.004 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 |
| Naive | 100–1000 | 0.032 ± 0.006<br>Mdn 0.031, IQR 0.000 | 0.033 ± 0.007<br>Mdn 0.031, IQR 0.001 |
| Naive | 1000–10000 | 0.039 ± 0.036<br>Mdn 0.033, IQR 0.005 | 0.033 ± 0.003<br>Mdn 0.034, IQR 0.002 |
| KMP | 10–100 | 0.596 ± 0.084<br>Mdn 0.600, IQR 0.111 | 0.606 ± 0.085<br>Mdn 0.624, IQR 0.122 |
| KMP | 100–1000 | 0.580 ± 0.079<br>Mdn 0.583, IQR 0.104 | 0.596 ± 0.080<br>Mdn 0.605, IQR 0.125 |
| KMP | 1000–10000 | 0.613 ± 0.140<br>Mdn 0.621, IQR 0.173 | 0.549 ± 0.090<br>Mdn 0.539, IQR 0.160 |
| Aho-Corasick | 10–100 | 2.885 ± 0.521<br>Mdn 2.982, IQR 0.848 | 2.940 ± 0.490<br>Mdn 3.022, IQR 0.837 |
| Aho-Corasick | 100–1000 | 2.576 ± 0.457<br>Mdn 2.612, IQR 0.659 | 2.704 ± 0.458<br>Mdn 2.666, IQR 0.755 |
| Aho-Corasick | 1000–10000 | 2.741 ± 0.607<br>Mdn 2.762, IQR 0.914 | 2.494 ± 0.525<br>Mdn 2.451, IQR 0.789 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Search time** (µs per call)

| Algorithm | Text length | Distinct | Repeating |
| --- | --- | ---: | ---: |
| Naive | 10–100 | 2.54 ± 1.30<br>Mdn 2.45, IQR 2.11 | 2.71 ± 1.33<br>Mdn 2.58, IQR 2.02 |
| Naive | 100–1000 | 29.61 ± 16.90<br>Mdn 26.71, IQR 22.18 | 31.16 ± 17.26<br>Mdn 29.82, IQR 31.73 |
| Naive | 1000–10000 | 330.74 ± 195.72<br>Mdn 377.66, IQR 334.65 | 417.07 ± 167.35<br>Mdn 454.52, IQR 225.65 |
| KMP | 10–100 | 2.68 ± 1.22<br>Mdn 2.63, IQR 2.08 | 2.86 ± 1.25<br>Mdn 2.71, IQR 1.88 |
| KMP | 100–1000 | 26.56 ± 14.42<br>Mdn 23.79, IQR 18.29 | 27.48 ± 14.38<br>Mdn 26.05, IQR 25.90 |
| KMP | 1000–10000 | 280.30 ± 167.50<br>Mdn 325.48, IQR 267.94 | 347.77 ± 139.57<br>Mdn 378.27, IQR 201.21 |
| Aho-Corasick | 10–100 | 4.03 ± 1.88<br>Mdn 3.96, IQR 3.18 | 4.32 ± 1.93<br>Mdn 4.23, IQR 2.86 |
| Aho-Corasick | 100–1000 | 39.62 ± 20.99<br>Mdn 35.61, IQR 23.63 | 40.76 ± 20.72<br>Mdn 40.26, IQR 37.71 |
| Aho-Corasick | 1000–10000 | 410.61 ± 242.88<br>Mdn 458.60, IQR 385.60 | 503.00 ± 197.70<br>Mdn 543.49, IQR 263.53 |

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
| Naive | 10–100 | 5.22 ± 2.40<br>Mdn 5.13, IQR 3.91 | 4.10 ± 1.70<br>Mdn 4.31, IQR 2.22 | 3.70 ± 1.29<br>Mdn 3.77, IQR 1.86 | 2.85 ± 1.23<br>Mdn 3.01, IQR 1.60 |
| Naive | 100–1000 | 72.68 ± 35.82<br>Mdn 76.86, IQR 70.40 | 38.51 ± 22.11<br>Mdn 36.85, IQR 29.47 | 29.63 ± 16.94<br>Mdn 27.42, IQR 30.94 | 35.34 ± 19.24<br>Mdn 35.68, IQR 37.83 |
| Naive | 1000–10000 | 780.23 ± 354.89<br>Mdn 889.53, IQR 597.59 | 528.17 ± 244.17<br>Mdn 535.22, IQR 464.03 | 403.46 ± 187.64<br>Mdn 378.78, IQR 332.52 | 349.01 ± 164.01<br>Mdn 312.99, IQR 215.13 |
| KMP | 10–100 | 4.86 ± 1.79<br>Mdn 4.81, IQR 2.88 | 4.51 ± 1.54<br>Mdn 4.84, IQR 1.77 | 4.11 ± 1.22<br>Mdn 4.23, IQR 1.69 | 3.30 ± 1.15<br>Mdn 3.32, IQR 1.47 |
| KMP | 100–1000 | 52.76 ± 24.06<br>Mdn 56.36, IQR 44.00 | 34.10 ± 17.95<br>Mdn 32.95, IQR 23.36 | 26.94 ± 14.64<br>Mdn 25.07, IQR 25.35 | 31.66 ± 16.55<br>Mdn 31.79, IQR 31.08 |
| KMP | 1000–10000 | 522.42 ± 237.82<br>Mdn 582.33, IQR 396.46 | 437.05 ± 200.64<br>Mdn 437.20, IQR 383.80 | 333.15 ± 157.75<br>Mdn 299.57, IQR 282.46 | 297.36 ± 139.53<br>Mdn 269.64, IQR 185.75 |
| Aho-Corasick | 10–100 | 7.80 ± 2.14<br>Mdn 7.66, IQR 3.11 | 7.90 ± 2.02<br>Mdn 7.81, IQR 2.45 | 8.13 ± 1.87<br>Mdn 8.44, IQR 2.59 | 6.66 ± 1.83<br>Mdn 6.62, IQR 2.69 |
| Aho-Corasick | 100–1000 | 62.08 ± 27.38<br>Mdn 66.06, IQR 51.22 | 46.44 ± 23.33<br>Mdn 45.48, IQR 29.90 | 41.61 ± 21.23<br>Mdn 39.86, IQR 37.37 | 49.04 ± 23.54<br>Mdn 50.52, IQR 44.47 |
| Aho-Corasick | 1000–10000 | 602.89 ± 273.78<br>Mdn 695.82, IQR 476.11 | 563.70 ± 257.91<br>Mdn 580.80, IQR 474.59 | 480.07 ± 217.45<br>Mdn 451.97, IQR 371.67 | 431.31 ± 198.68<br>Mdn 397.95, IQR 259.83 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Preprocessing time** (µs per call)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 0.035 ± 0.006<br>Mdn 0.032, IQR 0.004 | 0.034 ± 0.002<br>Mdn 0.032, IQR 0.004 | 0.032 ± 0.001<br>Mdn 0.032, IQR 0.000 |
| Naive | 100–1000 | 0.031 ± 0.003<br>Mdn 0.031, IQR 0.000 | 0.034 ± 0.008<br>Mdn 0.031, IQR 0.000 | 0.031 ± 0.001<br>Mdn 0.031, IQR 0.001 | 0.034 ± 0.010<br>Mdn 0.031, IQR 0.000 |
| Naive | 1000–10000 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.005 | 0.037 ± 0.026<br>Mdn 0.033, IQR 0.001 | 0.036 ± 0.026<br>Mdn 0.032, IQR 0.006 | 0.033 ± 0.002<br>Mdn 0.034, IQR 0.001 |
| KMP | 10–100 | 0.677 ± 0.171<br>Mdn 0.648, IQR 0.290 | 0.647 ± 0.112<br>Mdn 0.660, IQR 0.166 | 0.638 ± 0.087<br>Mdn 0.659, IQR 0.142 | 0.590 ± 0.117<br>Mdn 0.576, IQR 0.180 |
| KMP | 100–1000 | 0.653 ± 0.146<br>Mdn 0.660, IQR 0.222 | 0.659 ± 0.122<br>Mdn 0.661, IQR 0.159 | 0.616 ± 0.092<br>Mdn 0.655, IQR 0.139 | 0.582 ± 0.095<br>Mdn 0.600, IQR 0.168 |
| KMP | 1000–10000 | 0.732 ± 0.148<br>Mdn 0.723, IQR 0.187 | 0.686 ± 0.147<br>Mdn 0.698, IQR 0.206 | 0.609 ± 0.077<br>Mdn 0.639, IQR 0.098 | 0.632 ± 0.129<br>Mdn 0.607, IQR 0.156 |
| Aho-Corasick | 10–100 | 2.793 ± 0.645<br>Mdn 2.702, IQR 1.256 | 2.841 ± 0.576<br>Mdn 2.786, IQR 0.916 | 3.050 ± 0.483<br>Mdn 3.061, IQR 0.952 | 2.694 ± 0.607<br>Mdn 2.618, IQR 0.963 |
| Aho-Corasick | 100–1000 | 2.522 ± 0.551<br>Mdn 2.464, IQR 1.012 | 2.695 ± 0.465<br>Mdn 2.587, IQR 0.676 | 2.757 ± 0.522<br>Mdn 2.953, IQR 0.886 | 2.570 ± 0.500<br>Mdn 2.651, IQR 0.841 |
| Aho-Corasick | 1000–10000 | 2.812 ± 0.495<br>Mdn 2.850, IQR 0.621 | 2.930 ± 0.607<br>Mdn 3.017, IQR 1.122 | 2.770 ± 0.554<br>Mdn 2.772, IQR 0.928 | 2.717 ± 0.484<br>Mdn 2.691, IQR 0.863 |

*Units: µs per call. Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1). N per cell: 30.*


**Search time** (µs per call)

| Algorithm | Text length | |Σ| = 2 | |Σ| = 4 | |Σ| = 26 | Full Alice Σ |
| --- | --- | ---: | ---: | ---: | ---: |
| Naive | 10–100 | 5.18 ± 2.40<br>Mdn 5.09, IQR 3.91 | 4.06 ± 1.69<br>Mdn 4.28, IQR 2.22 | 3.67 ± 1.29<br>Mdn 3.74, IQR 1.86 | 2.82 ± 1.23<br>Mdn 2.98, IQR 1.60 |
| Naive | 100–1000 | 72.65 ± 35.82<br>Mdn 76.82, IQR 70.40 | 38.48 ± 22.12<br>Mdn 36.82, IQR 29.49 | 29.60 ± 16.94<br>Mdn 27.39, IQR 30.94 | 35.30 ± 19.24<br>Mdn 35.65, IQR 37.83 |
| Naive | 1000–10000 | 780.20 ± 354.89<br>Mdn 889.50, IQR 597.59 | 528.13 ± 244.17<br>Mdn 535.19, IQR 464.03 | 403.42 ± 187.65<br>Mdn 378.75, IQR 332.52 | 348.98 ± 164.01<br>Mdn 312.96, IQR 215.14 |
| KMP | 10–100 | 4.18 ± 1.80<br>Mdn 4.29, IQR 2.83 | 3.86 ± 1.54<br>Mdn 4.16, IQR 1.91 | 3.47 ± 1.21<br>Mdn 3.55, IQR 1.79 | 2.71 ± 1.15<br>Mdn 2.75, IQR 1.54 |
| KMP | 100–1000 | 52.11 ± 24.05<br>Mdn 55.54, IQR 43.84 | 33.44 ± 17.94<br>Mdn 32.31, IQR 23.22 | 26.33 ± 14.63<br>Mdn 24.41, IQR 25.34 | 31.08 ± 16.55<br>Mdn 31.16, IQR 31.14 |
| KMP | 1000–10000 | 521.69 ± 237.82<br>Mdn 581.75, IQR 396.40 | 436.36 ± 200.66<br>Mdn 436.70, IQR 383.90 | 332.54 ± 157.79<br>Mdn 298.89, IQR 282.62 | 296.73 ± 139.52<br>Mdn 269.08, IQR 185.91 |
| Aho-Corasick | 10–100 | 5.01 ± 2.10<br>Mdn 4.90, IQR 3.38 | 5.06 ± 2.05<br>Mdn 5.42, IQR 2.45 | 5.08 ± 1.81<br>Mdn 5.25, IQR 2.65 | 3.97 ± 1.71<br>Mdn 4.09, IQR 2.24 |
| Aho-Corasick | 100–1000 | 59.56 ± 27.26<br>Mdn 63.05, IQR 51.12 | 43.75 ± 23.32<br>Mdn 42.14, IQR 29.57 | 38.86 ± 21.12<br>Mdn 36.85, IQR 38.02 | 46.47 ± 23.55<br>Mdn 47.89, IQR 45.83 |
| Aho-Corasick | 1000–10000 | 600.07 ± 273.78<br>Mdn 692.40, IQR 476.56 | 560.77 ± 258.01<br>Mdn 577.90, IQR 474.61 | 477.30 ± 217.71<br>Mdn 448.83, IQR 372.35 | 428.59 ± 198.71<br>Mdn 395.30, IQR 258.69 |

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
| 10–100 | 77 | 8 | 560 | 560 | 7.27 | 24.30 | 160 | 2.08 | 8.39 | 174 | 2.26 | 10.84 |
| 100–1000 | 741 | 8 | 5,872 | 5,872 | 7.92 | 298.72 | 1,488 | 2.01 | 79.94 | 1,502 | 2.03 | 81.75 |
| 1000–10000 | 3,302 | 5 | 16,490 | 16,490 | 4.99 | 916.56 | 6,607 | 2.00 | 364.24 | 6,615 | 2.00 | 358.05 |

*Comparisons = prep + search (identical in every run, so the median equals every value). Comparisons / char = comparisons ÷ n. Time = median total time in µs per call over the runs.*


## Appendix: every condition

All factor levels, not pooled. Units as above: times in µs per call, comparisons as counts, memory in bytes.

| Condition | Algorithm | N | Total time (prep + search) (µs per call) | Preprocessing time (µs per call) | Search time (µs per call) | Comparisons (prep + search) (count) | Memory, structure only (memory_bytes, tested) (bytes) | Memory, raw retained size (descriptive only) (bytes) | Peak memory during preprocessing (descriptive only) (bytes) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| core, random, q 1–5, k=1, n 10–100 | Naive | 30 | 3.19 ± 1.46<br>Mdn 3.10, IQR 2.04 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.001 | 3.16 ± 1.46<br>Mdn 3.07, IQR 2.04 | 54.0 ± 27.2<br>Mdn 55.0, IQR 41.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=1, n 10–100 | KMP | 30 | 3.22 ± 1.31<br>Mdn 3.33, IQR 2.13 | 0.332 ± 0.088<br>Mdn 0.333, IQR 0.149 | 2.89 ± 1.29<br>Mdn 2.95, IQR 2.00 | 55.8 ± 27.4<br>Mdn 57.0, IQR 43.8 | 222 ± 12<br>Mdn 224, IQR 22 | 222 ± 12<br>Mdn 224, IQR 22 | 275 ± 18<br>Mdn 272, IQR 28 |
| core, random, q 1–5, k=1, n 10–100 | Aho-Corasick | 30 | 5.74 ± 2.21<br>Mdn 5.91, IQR 3.52 | 1.331 ± 0.457<br>Mdn 1.343, IQR 0.827 | 4.41 ± 2.11<br>Mdn 4.53, IQR 3.03 | 59.6 ± 28.0<br>Mdn 61.0, IQR 44.5 | 1,384 ± 349<br>Mdn 1,440, IQR 660 | 1,398 ± 352<br>Mdn 1,440, IQR 615 | 2,158 ± 352<br>Mdn 2,200, IQR 615 |
| core, random, q 1–5, k=5, n 10–100 | Naive | 30 | 14.67 ± 6.64<br>Mdn 12.94, IQR 7.13 | 0.034 ± 0.002<br>Mdn 0.033, IQR 0.004 | 14.63 ± 6.64<br>Mdn 12.90, IQR 7.13 | 255.7 ± 124.1<br>Mdn 226.0, IQR 150.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=5, n 10–100 | KMP | 30 | 14.87 ± 6.05<br>Mdn 13.27, IQR 7.48 | 1.425 ± 0.179<br>Mdn 1.393, IQR 0.205 | 13.45 ± 6.05<br>Mdn 11.86, IQR 7.12 | 265.6 ± 124.0<br>Mdn 238.0, IQR 154.5 | 576 ± 21<br>Mdn 572, IQR 24 | 576 ± 21<br>Mdn 572, IQR 24 | 627 ± 24<br>Mdn 624, IQR 39 |
| core, random, q 1–5, k=5, n 10–100 | Aho-Corasick | 30 | 10.20 ± 2.33<br>Mdn 9.89, IQR 3.48 | 5.195 ± 0.913<br>Mdn 5.108, IQR 1.276 | 5.00 ± 2.15<br>Mdn 4.50, IQR 2.37 | 83.6 ± 27.2<br>Mdn 79.0, IQR 39.5 | 4,100 ± 729<br>Mdn 3,956, IQR 920 | 4,158 ± 738<br>Mdn 4,102, IQR 969 | 4,918 ± 738<br>Mdn 4,862, IQR 969 |
| core, random, q 5–10, k=1, n 10–100 | Naive | 30 | 3.17 ± 1.17<br>Mdn 3.22, IQR 1.53 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 3.13 ± 1.17<br>Mdn 3.19, IQR 1.53 | 55.6 ± 23.6<br>Mdn 55.0, IQR 31.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=1, n 10–100 | KMP | 30 | 3.63 ± 1.13<br>Mdn 3.67, IQR 1.54 | 0.613 ± 0.104<br>Mdn 0.620, IQR 0.168 | 3.02 ± 1.12<br>Mdn 3.06, IQR 1.64 | 62.2 ± 23.5<br>Mdn 62.0, IQR 31.5 | 261 ± 14<br>Mdn 264, IQR 24 | 261 ± 14<br>Mdn 264, IQR 24 | 326 ± 30<br>Mdn 322, IQR 36 |
| core, random, q 5–10, k=1, n 10–100 | Aho-Corasick | 30 | 7.37 ± 1.78<br>Mdn 7.24, IQR 2.35 | 2.886 ± 0.567<br>Mdn 2.949, IQR 1.052 | 4.48 ± 1.73<br>Mdn 4.62, IQR 2.40 | 70.9 ± 23.6<br>Mdn 71.5, IQR 30.0 | 2,654 ± 509<br>Mdn 2,832, IQR 912 | 2,692 ± 523<br>Mdn 2,862, IQR 972 | 3,452 ± 523<br>Mdn 3,622, IQR 972 |
| core, random, q 5–10, k=5, n 10–100 | Naive | 30 | 15.87 ± 7.26<br>Mdn 17.01, IQR 11.02 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 15.84 ± 7.26<br>Mdn 16.98, IQR 11.02 | 286.7 ± 138.5<br>Mdn 303.0, IQR 215.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=5, n 10–100 | KMP | 30 | 17.85 ± 6.97<br>Mdn 19.16, IQR 10.11 | 2.730 ± 0.228<br>Mdn 2.669, IQR 0.284 | 15.12 ± 6.90<br>Mdn 16.40, IQR 10.04 | 319.0 ± 139.1<br>Mdn 334.0, IQR 214.8 | 751 ± 27<br>Mdn 752, IQR 44 | 751 ± 27<br>Mdn 752, IQR 44 | 818 ± 40<br>Mdn 820, IQR 44 |
| core, random, q 5–10, k=5, n 10–100 | Aho-Corasick | 30 | 17.18 ± 3.46<br>Mdn 17.47, IQR 4.75 | 11.862 ± 1.633<br>Mdn 12.034, IQR 1.647 | 5.32 ± 2.34<br>Mdn 5.45, IQR 3.69 | 134.3 ± 33.7<br>Mdn 142.0, IQR 50.5 | 9,650 ± 1,329<br>Mdn 9,808, IQR 888 | 9,790 ± 1,355<br>Mdn 10,040, IQR 1,062 | 10,550 ± 1,355<br>Mdn 10,800, IQR 1,062 |
| core, random, q 10–20, k=1, n 10–100 | Naive | 30 | 2.99 ± 1.26<br>Mdn 2.69, IQR 2.09 | 0.034 ± 0.003<br>Mdn 0.032, IQR 0.004 | 2.96 ± 1.26<br>Mdn 2.65, IQR 2.09 | 52.8 ± 24.7<br>Mdn 47.0, IQR 39.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=1, n 10–100 | KMP | 30 | 3.99 ± 1.20<br>Mdn 3.67, IQR 1.66 | 1.051 ± 0.191<br>Mdn 1.044, IQR 0.313 | 2.94 ± 1.18<br>Mdn 2.56, IQR 1.83 | 67.6 ± 25.0<br>Mdn 62.5, IQR 37.5 | 325 ± 24<br>Mdn 328, IQR 36 | 325 ± 24<br>Mdn 328, IQR 36 | 392 ± 29<br>Mdn 392, IQR 32 |
| core, random, q 10–20, k=1, n 10–100 | Aho-Corasick | 30 | 9.64 ± 2.15<br>Mdn 9.31, IQR 2.67 | 5.370 ± 0.962<br>Mdn 5.403, IQR 1.429 | 4.27 ± 1.86<br>Mdn 3.69, IQR 3.11 | 84.5 ± 25.8<br>Mdn 82.0, IQR 35.0 | 4,787 ± 791<br>Mdn 4,944, IQR 1,272 | 4,867 ± 806<br>Mdn 4,974, IQR 1,242 | 5,627 ± 806<br>Mdn 5,734, IQR 1,242 |
| core, random, q 10–20, k=5, n 10–100 | Naive | 30 | 18.55 ± 5.65<br>Mdn 19.57, IQR 9.62 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 18.51 ± 5.65<br>Mdn 19.54, IQR 9.62 | 341.5 ± 107.2<br>Mdn 366.5, IQR 181.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=5, n 10–100 | KMP | 30 | 22.67 ± 5.38<br>Mdn 22.70, IQR 10.23 | 4.840 ± 0.538<br>Mdn 4.748, IQR 0.646 | 17.83 ± 5.25<br>Mdn 18.57, IQR 9.37 | 411.6 ± 107.8<br>Mdn 430.5, IQR 189.5 | 1,050 ± 59<br>Mdn 1,060, IQR 90 | 1,050 ± 59<br>Mdn 1,060, IQR 90 | 1,119 ± 61<br>Mdn 1,118, IQR 92 |
| core, random, q 10–20, k=5, n 10–100 | Aho-Corasick | 30 | 29.50 ± 4.78<br>Mdn 30.40, IQR 5.34 | 23.439 ± 3.961<br>Mdn 24.263, IQR 4.267 | 6.06 ± 1.77<br>Mdn 6.40, IQR 2.99 | 218.6 ± 32.8<br>Mdn 220.5, IQR 46.8 | 18,922 ± 3,201<br>Mdn 19,492, IQR 3,118 | 19,268 ± 3,293<br>Mdn 19,976, IQR 3,325 | 20,415 ± 3,491<br>Mdn 21,264, IQR 3,591 |
| core, random, q 1–5, k=1, n 100–1000 | Naive | 30 | 32.74 ± 17.00<br>Mdn 32.97, IQR 25.03 | 0.032 ± 0.006<br>Mdn 0.031, IQR 0.001 | 32.71 ± 17.00<br>Mdn 32.93, IQR 25.02 | 532.4 ± 244.0<br>Mdn 562.5, IQR 395.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=1, n 100–1000 | KMP | 30 | 29.12 ± 14.99<br>Mdn 29.43, IQR 25.19 | 0.352 ± 0.078<br>Mdn 0.360, IQR 0.115 | 28.77 ± 14.98<br>Mdn 28.98, IQR 25.04 | 534.4 ± 244.3<br>Mdn 566.0, IQR 397.0 | 225 ± 10<br>Mdn 224, IQR 16 | 225 ± 10<br>Mdn 224, IQR 16 | 277 ± 16<br>Mdn 272, IQR 24 |
| core, random, q 1–5, k=1, n 100–1000 | Aho-Corasick | 30 | 44.47 ± 21.21<br>Mdn 47.07, IQR 33.39 | 1.352 ± 0.374<br>Mdn 1.366, IQR 0.553 | 43.11 ± 21.15<br>Mdn 45.19, IQR 33.22 | 539.9 ± 245.4<br>Mdn 572.5, IQR 398.2 | 1,456 ± 308<br>Mdn 1,440, IQR 480 | 1,470 ± 314<br>Mdn 1,440, IQR 480 | 2,230 ± 314<br>Mdn 2,200, IQR 480 |
| core, random, q 1–5, k=5, n 100–1000 | Naive | 30 | 181.95 ± 90.07<br>Mdn 210.13, IQR 148.86 | 0.031 ± 0.003<br>Mdn 0.031, IQR 0.000 | 181.92 ± 90.07<br>Mdn 210.10, IQR 148.86 | 2,892.8 ± 1,309.7<br>Mdn 3,189.0, IQR 2,177.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=5, n 100–1000 | KMP | 30 | 161.13 ± 77.45<br>Mdn 179.13, IQR 129.11 | 1.386 ± 0.162<br>Mdn 1.401, IQR 0.231 | 159.74 ± 77.45<br>Mdn 177.80, IQR 129.19 | 2,902.8 ± 1,309.8<br>Mdn 3,195.5, IQR 2,183.0 | 579 ± 21<br>Mdn 576, IQR 24 | 579 ± 21<br>Mdn 576, IQR 24 | 634 ± 32<br>Mdn 624, IQR 31 |
| core, random, q 1–5, k=5, n 100–1000 | Aho-Corasick | 30 | 60.06 ± 26.55<br>Mdn 64.54, IQR 46.36 | 5.103 ± 0.807<br>Mdn 5.025, IQR 0.710 | 54.95 ± 26.42<br>Mdn 60.58, IQR 44.43 | 640.6 ± 277.6<br>Mdn 693.0, IQR 468.0 | 4,342 ± 717<br>Mdn 4,192, IQR 852 | 4,408 ± 719<br>Mdn 4,252, IQR 867 | 5,168 ± 719<br>Mdn 5,012, IQR 867 |
| core, random, q 5–10, k=1, n 100–1000 | Naive | 30 | 38.65 ± 18.12<br>Mdn 44.69, IQR 27.56 | 0.033 ± 0.010<br>Mdn 0.031, IQR 0.001 | 38.62 ± 18.12<br>Mdn 44.66, IQR 27.56 | 626.2 ± 257.6<br>Mdn 723.5, IQR 402.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=1, n 100–1000 | KMP | 30 | 34.96 ± 15.80<br>Mdn 39.19, IQR 24.51 | 0.594 ± 0.088<br>Mdn 0.592, IQR 0.107 | 34.36 ± 15.78<br>Mdn 38.61, IQR 24.37 | 632.7 ± 258.0<br>Mdn 730.5, IQR 405.0 | 260 ± 13<br>Mdn 260, IQR 16 | 260 ± 13<br>Mdn 260, IQR 16 | 315 ± 18<br>Mdn 314, IQR 23 |
| core, random, q 5–10, k=1, n 100–1000 | Aho-Corasick | 30 | 53.38 ± 22.24<br>Mdn 59.44, IQR 36.80 | 2.624 ± 0.467<br>Mdn 2.683, IQR 0.550 | 50.75 ± 22.13<br>Mdn 56.65, IQR 35.91 | 641.2 ± 258.3<br>Mdn 739.0, IQR 407.8 | 2,616 ± 462<br>Mdn 2,616, IQR 672 | 2,638 ± 472<br>Mdn 2,646, IQR 672 | 3,398 ± 472<br>Mdn 3,406, IQR 672 |
| core, random, q 5–10, k=5, n 100–1000 | Naive | 30 | 173.56 ± 83.60<br>Mdn 175.81, IQR 97.21 | 0.032 ± 0.004<br>Mdn 0.031, IQR 0.001 | 173.52 ± 83.60<br>Mdn 175.78, IQR 97.21 | 2,767.7 ± 1,212.0<br>Mdn 2,823.0, IQR 1,417.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=5, n 100–1000 | KMP | 30 | 155.72 ± 73.01<br>Mdn 158.15, IQR 80.53 | 2.594 ± 0.213<br>Mdn 2.620, IQR 0.249 | 153.12 ± 72.91<br>Mdn 155.51, IQR 80.51 | 2,800.5 ± 1,213.5<br>Mdn 2,857.0, IQR 1,417.0 | 760 ± 29<br>Mdn 768, IQR 38 | 760 ± 29<br>Mdn 768, IQR 38 | 826 ± 38<br>Mdn 824, IQR 43 |
| core, random, q 5–10, k=5, n 100–1000 | Aho-Corasick | 30 | 63.18 ± 23.64<br>Mdn 64.21, IQR 27.72 | 11.988 ± 1.163<br>Mdn 12.411, IQR 1.635 | 51.19 ± 23.21<br>Mdn 51.81, IQR 27.39 | 658.2 ± 259.3<br>Mdn 676.5, IQR 299.5 | 10,324 ± 1,072<br>Mdn 10,528, IQR 1,428 | 10,472 ± 1,077<br>Mdn 10,648, IQR 1,503 | 11,232 ± 1,077<br>Mdn 11,408, IQR 1,503 |
| core, random, q 10–20, k=1, n 100–1000 | Naive | 30 | 30.85 ± 18.68<br>Mdn 31.01, IQR 30.97 | 0.031 ± 0.000<br>Mdn 0.031, IQR 0.000 | 30.82 ± 18.68<br>Mdn 30.98, IQR 30.97 | 508.9 ± 267.3<br>Mdn 506.0, IQR 381.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=1, n 100–1000 | KMP | 30 | 28.28 ± 15.63<br>Mdn 29.47, IQR 22.77 | 0.960 ± 0.197<br>Mdn 0.916, IQR 0.308 | 27.32 ± 15.63<br>Mdn 28.42, IQR 22.55 | 522.4 ± 267.4<br>Mdn 517.5, IQR 383.8 | 316 ± 29<br>Mdn 312, IQR 62 | 316 ± 29<br>Mdn 312, IQR 62 | 387 ± 35<br>Mdn 390, IQR 53 |
| core, random, q 10–20, k=1, n 100–1000 | Aho-Corasick | 30 | 45.87 ± 23.32<br>Mdn 43.60, IQR 32.67 | 4.614 ± 1.032<br>Mdn 4.350, IQR 2.022 | 41.26 ± 23.25<br>Mdn 39.58, IQR 33.66 | 538.0 ± 267.5<br>Mdn 529.0, IQR 377.8 | 4,448 ± 940<br>Mdn 4,272, IQR 2,052 | 4,506 ± 947<br>Mdn 4,332, IQR 1,917 | 5,266 ± 947<br>Mdn 5,092, IQR 1,917 |
| core, random, q 10–20, k=5, n 100–1000 | Naive | 30 | 196.19 ± 96.98<br>Mdn 192.34, IQR 152.48 | 0.033 ± 0.006<br>Mdn 0.031, IQR 0.000 | 196.16 ± 96.98<br>Mdn 192.31, IQR 152.50 | 3,103.3 ± 1,413.4<br>Mdn 3,057.0, IQR 2,245.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=5, n 100–1000 | KMP | 30 | 178.77 ± 84.22<br>Mdn 174.80, IQR 131.14 | 4.659 ± 0.439<br>Mdn 4.701, IQR 0.642 | 174.11 ± 84.16<br>Mdn 170.04, IQR 130.77 | 3,176.3 ± 1,413.8<br>Mdn 3,137.5, IQR 2,239.8 | 1,075 ± 58<br>Mdn 1,080, IQR 80 | 1,075 ± 58<br>Mdn 1,080, IQR 80 | 1,141 ± 61<br>Mdn 1,152, IQR 81 |
| core, random, q 10–20, k=5, n 100–1000 | Aho-Corasick | 30 | 83.38 ± 28.09<br>Mdn 83.53, IQR 42.60 | 25.116 ± 2.539<br>Mdn 25.429, IQR 3.438 | 58.27 ± 27.79<br>Mdn 56.84, IQR 45.36 | 810.1 ± 298.1<br>Mdn 820.5, IQR 464.5 | 20,669 ± 1,979<br>Mdn 21,016, IQR 3,024 | 20,955 ± 2,015<br>Mdn 21,346, IQR 2,739 | 22,190 ± 2,120<br>Mdn 22,634, IQR 2,739 |
| core, random, q 1–5, k=1, n 1000–10000 | Naive | 30 | 389.92 ± 186.40<br>Mdn 384.43, IQR 329.03 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.004 | 389.89 ± 186.40<br>Mdn 384.39, IQR 329.03 | 5,702.4 ± 2,645.3<br>Mdn 5,561.5, IQR 4,699.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=1, n 1000–10000 | KMP | 30 | 328.60 ± 152.78<br>Mdn 321.70, IQR 261.70 | 0.411 ± 0.143<br>Mdn 0.354, IQR 0.160 | 328.19 ± 152.79<br>Mdn 321.35, IQR 261.90 | 5,703.5 ± 2,644.5<br>Mdn 5,563.5, IQR 4,701.5 | 223 ± 11<br>Mdn 224, IQR 14 | 223 ± 11<br>Mdn 224, IQR 14 | 277 ± 23<br>Mdn 272, IQR 24 |
| core, random, q 1–5, k=1, n 1000–10000 | Aho-Corasick | 30 | 489.67 ± 229.58<br>Mdn 476.48, IQR 413.20 | 1.347 ± 0.354<br>Mdn 1.352, IQR 0.573 | 488.33 ± 229.64<br>Mdn 475.14, IQR 412.36 | 5,723.1 ± 2,647.1<br>Mdn 5,567.5, IQR 4,674.2 | 1,400 ± 322<br>Mdn 1,440, IQR 420 | 1,412 ± 331<br>Mdn 1,440, IQR 435 | 2,172 ± 331<br>Mdn 2,200, IQR 435 |
| core, random, q 1–5, k=5, n 1000–10000 | Naive | 30 | 2,092.59 ± 927.09<br>Mdn 2,032.24, IQR 1,767.11 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.005 | 2,092.56 ± 927.09<br>Mdn 2,032.20, IQR 1,767.11 | 30,185.0 ± 13,189.6<br>Mdn 29,276.5, IQR 26,030.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 1–5, k=5, n 1000–10000 | KMP | 30 | 1,778.88 ± 770.29<br>Mdn 1,755.84, IQR 1,408.81 | 1.406 ± 0.247<br>Mdn 1.328, IQR 0.272 | 1,777.48 ± 770.25<br>Mdn 1,754.33, IQR 1,408.77 | 30,190.5 ± 13,188.2<br>Mdn 29,285.5, IQR 26,028.8 | 578 ± 28<br>Mdn 572, IQR 38 | 578 ± 28<br>Mdn 572, IQR 38 | 632 ± 29<br>Mdn 628, IQR 42 |
| core, random, q 1–5, k=5, n 1000–10000 | Aho-Corasick | 30 | 600.53 ± 266.30<br>Mdn 584.34, IQR 519.39 | 5.017 ± 0.957<br>Mdn 4.790, IQR 1.383 | 595.51 ± 266.30<br>Mdn 578.29, IQR 518.56 | 6,401.6 ± 2,785.1<br>Mdn 6,229.5, IQR 5,551.0 | 4,302 ± 901<br>Mdn 4,072, IQR 1,332 | 4,360 ± 907<br>Mdn 4,132, IQR 1,332 | 5,120 ± 907<br>Mdn 4,892, IQR 1,332 |
| core, random, q 5–10, k=1, n 1000–10000 | Naive | 30 | 404.94 ± 195.09<br>Mdn 396.95, IQR 345.16 | 0.037 ± 0.026<br>Mdn 0.034, IQR 0.004 | 404.91 ± 195.09<br>Mdn 396.91, IQR 345.16 | 5,905.7 ± 2,726.5<br>Mdn 5,946.5, IQR 5,197.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=1, n 1000–10000 | KMP | 30 | 340.57 ± 160.00<br>Mdn 340.01, IQR 315.57 | 0.597 ± 0.144<br>Mdn 0.579, IQR 0.167 | 339.97 ± 160.02<br>Mdn 339.34, IQR 315.56 | 5,911.1 ± 2,726.0<br>Mdn 5,952.0, IQR 5,198.5 | 258 ± 14<br>Mdn 256, IQR 22 | 258 ± 14<br>Mdn 256, IQR 22 | 314 ± 22<br>Mdn 312, IQR 35 |
| core, random, q 5–10, k=1, n 1000–10000 | Aho-Corasick | 30 | 502.06 ± 235.29<br>Mdn 498.18, IQR 447.46 | 2.583 ± 0.568<br>Mdn 2.537, IQR 1.031 | 499.48 ± 235.38<br>Mdn 495.66, IQR 447.12 | 5,919.4 ± 2,725.8<br>Mdn 5,959.5, IQR 5,199.5 | 2,531 ± 500<br>Mdn 2,400, IQR 852 | 2,549 ± 510<br>Mdn 2,430, IQR 867 | 3,309 ± 510<br>Mdn 3,190, IQR 867 |
| core, random, q 5–10, k=5, n 1000–10000 | Naive | 30 | 1,994.20 ± 907.97<br>Mdn 2,010.73, IQR 1,608.46 | 0.037 ± 0.026<br>Mdn 0.033, IQR 0.004 | 1,994.17 ± 907.97<br>Mdn 2,010.70, IQR 1,608.35 | 28,774.7 ± 12,844.3<br>Mdn 29,496.0, IQR 22,459.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 5–10, k=5, n 1000–10000 | KMP | 30 | 1,696.19 ± 773.72<br>Mdn 1,705.88, IQR 1,363.23 | 2.592 ± 0.250<br>Mdn 2.547, IQR 0.260 | 1,693.60 ± 773.62<br>Mdn 1,703.55, IQR 1,362.84 | 28,802.6 ± 12,841.9<br>Mdn 29,519.0, IQR 22,456.5 | 761 ± 30<br>Mdn 760, IQR 28 | 761 ± 30<br>Mdn 760, IQR 28 | 822 ± 37<br>Mdn 818, IQR 43 |
| core, random, q 5–10, k=5, n 1000–10000 | Aho-Corasick | 30 | 565.96 ± 248.63<br>Mdn 592.00, IQR 432.69 | 11.715 ± 1.139<br>Mdn 11.626, IQR 1.511 | 554.24 ± 248.28<br>Mdn 580.36, IQR 431.95 | 6,136.5 ± 2,710.2<br>Mdn 6,289.5, IQR 4,745.2 | 10,390 ± 1,026<br>Mdn 10,288, IQR 1,056 | 10,550 ± 1,059<br>Mdn 10,348, IQR 996 | 11,310 ± 1,059<br>Mdn 11,108, IQR 996 |
| core, random, q 10–20, k=1, n 1000–10000 | Naive | 30 | 416.36 ± 200.36<br>Mdn 448.65, IQR 313.96 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.005 | 416.33 ± 200.36<br>Mdn 448.62, IQR 313.96 | 6,024.1 ± 2,814.9<br>Mdn 6,214.0, IQR 4,204.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=1, n 1000–10000 | KMP | 30 | 353.49 ± 171.70<br>Mdn 378.00, IQR 254.19 | 1.002 ± 0.195<br>Mdn 1.039, IQR 0.291 | 352.49 ± 171.65<br>Mdn 376.96, IQR 254.22 | 6,037.5 ± 2,815.7<br>Mdn 6,230.5, IQR 4,208.8 | 322 ± 28<br>Mdn 328, IQR 52 | 322 ± 28<br>Mdn 328, IQR 52 | 389 ± 31<br>Mdn 392, IQR 52 |
| core, random, q 10–20, k=1, n 1000–10000 | Aho-Corasick | 30 | 517.13 ± 244.49<br>Mdn 541.39, IQR 366.90 | 4.819 ± 0.973<br>Mdn 4.904, IQR 1.766 | 512.31 ± 244.23<br>Mdn 535.94, IQR 367.30 | 6,053.9 ± 2,816.9<br>Mdn 6,249.5, IQR 4,213.5 | 4,678 ± 921<br>Mdn 4,944, IQR 1,752 | 4,734 ± 932<br>Mdn 5,004, IQR 1,737 | 5,494 ± 932<br>Mdn 5,764, IQR 1,737 |
| core, random, q 10–20, k=5, n 1000–10000 | Naive | 30 | 2,147.31 ± 883.16<br>Mdn 2,449.53, IQR 1,393.30 | 0.033 ± 0.003<br>Mdn 0.033, IQR 0.004 | 2,147.28 ± 883.16<br>Mdn 2,449.50, IQR 1,393.30 | 30,486.5 ± 12,237.1<br>Mdn 34,548.0, IQR 20,006.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, random, q 10–20, k=5, n 1000–10000 | KMP | 30 | 1,798.83 ± 739.56<br>Mdn 2,022.55, IQR 1,224.53 | 4.528 ± 0.561<br>Mdn 4.541, IQR 0.499 | 1,794.31 ± 739.44<br>Mdn 2,018.45, IQR 1,224.70 | 30,551.6 ± 12,237.5<br>Mdn 34,621.0, IQR 20,008.8 | 1,055 ± 72<br>Mdn 1,056, IQR 106 | 1,055 ± 72<br>Mdn 1,056, IQR 106 | 1,123 ± 71<br>Mdn 1,122, IQR 101 |
| core, random, q 10–20, k=5, n 1000–10000 | Aho-Corasick | 30 | 617.87 ± 244.01<br>Mdn 703.68, IQR 397.82 | 22.993 ± 3.006<br>Mdn 22.745, IQR 4.093 | 594.87 ± 243.28<br>Mdn 679.29, IQR 396.91 | 6,569.0 ± 2,581.9<br>Mdn 7,428.0, IQR 4,235.2 | 20,119 ± 2,394<br>Mdn 20,032, IQR 3,564 | 20,413 ± 2,413<br>Mdn 20,302, IQR 3,564 | 21,613 ± 2,553<br>Mdn 21,590, IQR 3,564 |
| core, narrative, q 1–5, k=1, n 10–100 | Naive | 30 | 3.32 ± 1.39<br>Mdn 3.39, IQR 2.37 | 0.034 ± 0.002<br>Mdn 0.032, IQR 0.004 | 3.29 ± 1.39<br>Mdn 3.36, IQR 2.37 | 57.5 ± 25.9<br>Mdn 64.0, IQR 34.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=1, n 10–100 | KMP | 30 | 3.43 ± 1.23<br>Mdn 3.74, IQR 1.87 | 0.358 ± 0.081<br>Mdn 0.341, IQR 0.101 | 3.07 ± 1.25<br>Mdn 3.40, IQR 2.00 | 59.7 ± 25.3<br>Mdn 65.0, IQR 33.2 | 226 ± 10<br>Mdn 224, IQR 14 | 226 ± 10<br>Mdn 224, IQR 14 | 276 ± 14<br>Mdn 272, IQR 22 |
| core, narrative, q 1–5, k=1, n 10–100 | Aho-Corasick | 30 | 5.95 ± 1.78<br>Mdn 6.29, IQR 2.63 | 1.451 ± 0.407<br>Mdn 1.395, IQR 0.566 | 4.50 ± 1.89<br>Mdn 4.79, IQR 3.26 | 64.6 ± 25.3<br>Mdn 71.0, IQR 33.2 | 1,488 ± 311<br>Mdn 1,440, IQR 420 | 1,494 ± 314<br>Mdn 1,440, IQR 465 | 2,254 ± 314<br>Mdn 2,200, IQR 465 |
| core, narrative, q 1–5, k=5, n 10–100 | Naive | 30 | 17.70 ± 7.49<br>Mdn 18.85, IQR 13.51 | 0.034 ± 0.002<br>Mdn 0.033, IQR 0.004 | 17.67 ± 7.49<br>Mdn 18.81, IQR 13.51 | 312.1 ± 139.5<br>Mdn 333.0, IQR 259.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=5, n 10–100 | KMP | 30 | 17.62 ± 6.86<br>Mdn 18.35, IQR 12.29 | 1.418 ± 0.187<br>Mdn 1.394, IQR 0.251 | 16.20 ± 6.84<br>Mdn 16.87, IQR 12.35 | 320.3 ± 139.2<br>Mdn 342.0, IQR 272.5 | 575 ± 22<br>Mdn 572, IQR 32 | 575 ± 22<br>Mdn 572, IQR 32 | 624 ± 24<br>Mdn 620, IQR 32 |
| core, narrative, q 1–5, k=5, n 10–100 | Aho-Corasick | 30 | 11.19 ± 2.73<br>Mdn 11.90, IQR 4.93 | 4.984 ± 0.982<br>Mdn 4.892, IQR 0.910 | 6.21 ± 2.49<br>Mdn 6.31, IQR 4.34 | 101.7 ± 34.0<br>Mdn 107.0, IQR 66.5 | 3,911 ± 787<br>Mdn 3,776, IQR 696 | 3,929 ± 787<br>Mdn 3,776, IQR 696 | 4,689 ± 787<br>Mdn 4,536, IQR 696 |
| core, narrative, q 5–10, k=1, n 10–100 | Naive | 30 | 3.30 ± 1.52<br>Mdn 3.44, IQR 2.41 | 0.033 ± 0.006<br>Mdn 0.032, IQR 0.001 | 3.27 ± 1.52<br>Mdn 3.40, IQR 2.41 | 59.5 ± 30.5<br>Mdn 65.0, IQR 49.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=1, n 10–100 | KMP | 30 | 3.70 ± 1.40<br>Mdn 3.88, IQR 2.32 | 0.598 ± 0.097<br>Mdn 0.604, IQR 0.151 | 3.11 ± 1.41<br>Mdn 3.26, IQR 2.18 | 66.0 ± 30.0<br>Mdn 71.0, IQR 52.5 | 260 ± 14<br>Mdn 260, IQR 24 | 260 ± 14<br>Mdn 260, IQR 24 | 313 ± 20<br>Mdn 312, IQR 30 |
| core, narrative, q 5–10, k=1, n 10–100 | Aho-Corasick | 30 | 7.30 ± 2.09<br>Mdn 7.65, IQR 3.58 | 2.794 ± 0.515<br>Mdn 2.705, IQR 0.925 | 4.51 ± 2.13<br>Mdn 4.85, IQR 3.33 | 74.8 ± 30.0<br>Mdn 80.0, IQR 55.5 | 2,624 ± 510<br>Mdn 2,616, IQR 912 | 2,634 ± 517<br>Mdn 2,616, IQR 957 | 3,394 ± 517<br>Mdn 3,376, IQR 957 |
| core, narrative, q 5–10, k=5, n 10–100 | Naive | 30 | 16.35 ± 7.14<br>Mdn 18.30, IQR 12.00 | 0.034 ± 0.003<br>Mdn 0.033, IQR 0.004 | 16.32 ± 7.14<br>Mdn 18.26, IQR 12.00 | 307.9 ± 144.5<br>Mdn 342.5, IQR 231.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=5, n 10–100 | KMP | 30 | 18.33 ± 6.59<br>Mdn 20.66, IQR 10.56 | 2.767 ± 0.215<br>Mdn 2.781, IQR 0.238 | 15.56 ± 6.65<br>Mdn 17.72, IQR 10.51 | 338.8 ± 141.8<br>Mdn 370.5, IQR 224.2 | 757 ± 29<br>Mdn 756, IQR 30 | 757 ± 29<br>Mdn 756, IQR 30 | 809 ± 32<br>Mdn 808, IQR 39 |
| core, narrative, q 5–10, k=5, n 10–100 | Aho-Corasick | 30 | 17.39 ± 3.23<br>Mdn 18.39, IQR 4.85 | 11.882 ± 1.626<br>Mdn 12.089, IQR 1.701 | 5.51 ± 2.33<br>Mdn 6.01, IQR 3.77 | 151.9 ± 40.2<br>Mdn 166.5, IQR 65.5 | 9,597 ± 1,353<br>Mdn 9,744, IQR 1,758 | 9,637 ± 1,354<br>Mdn 9,744, IQR 1,623 | 10,397 ± 1,353<br>Mdn 10,504, IQR 1,623 |
| core, narrative, q 10–20, k=1, n 10–100 | Naive | 30 | 3.36 ± 1.24<br>Mdn 3.32, IQR 1.18 | 0.033 ± 0.003<br>Mdn 0.032, IQR 0.004 | 3.32 ± 1.24<br>Mdn 3.29, IQR 1.19 | 62.7 ± 25.3<br>Mdn 63.5, IQR 25.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=1, n 10–100 | KMP | 30 | 4.34 ± 1.29<br>Mdn 4.27, IQR 1.22 | 1.013 ± 0.190<br>Mdn 0.984, IQR 0.262 | 3.33 ± 1.20<br>Mdn 3.29, IQR 1.11 | 76.8 ± 26.1<br>Mdn 76.5, IQR 23.0 | 320 ± 25<br>Mdn 320, IQR 38 | 320 ± 25<br>Mdn 320, IQR 38 | 371 ± 29<br>Mdn 372, IQR 41 |
| core, narrative, q 10–20, k=1, n 10–100 | Aho-Corasick | 30 | 9.82 ± 2.27<br>Mdn 9.84, IQR 3.32 | 5.109 ± 0.954<br>Mdn 5.095, IQR 1.507 | 4.71 ± 1.75<br>Mdn 4.83, IQR 1.64 | 93.4 ± 27.8<br>Mdn 93.5, IQR 25.8 | 4,602 ± 837<br>Mdn 4,512, IQR 1,332 | 4,608 ± 842<br>Mdn 4,512, IQR 1,332 | 5,368 ± 842<br>Mdn 5,272, IQR 1,332 |
| core, narrative, q 10–20, k=5, n 10–100 | Naive | 30 | 15.09 ± 6.76<br>Mdn 14.39, IQR 11.87 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.001 | 15.05 ± 6.76<br>Mdn 14.35, IQR 11.86 | 287.7 ± 137.6<br>Mdn 270.0, IQR 239.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=5, n 10–100 | KMP | 30 | 19.38 ± 6.15<br>Mdn 19.14, IQR 10.90 | 4.862 ± 0.545<br>Mdn 4.820, IQR 0.849 | 14.51 ± 6.13<br>Mdn 13.91, IQR 10.93 | 358.5 ± 134.2<br>Mdn 340.5, IQR 242.2 | 1,052 ± 65<br>Mdn 1,056, IQR 106 | 1,052 ± 65<br>Mdn 1,056, IQR 106 | 1,106 ± 69<br>Mdn 1,104, IQR 101 |
| core, narrative, q 10–20, k=5, n 10–100 | Aho-Corasick | 30 | 27.41 ± 4.33<br>Mdn 27.97, IQR 6.06 | 22.484 ± 3.269<br>Mdn 22.133, IQR 4.529 | 4.92 ± 2.10<br>Mdn 4.71, IQR 3.64 | 218.6 ± 41.4<br>Mdn 216.5, IQR 60.5 | 18,485 ± 2,654<br>Mdn 18,284, IQR 3,916 | 18,559 ± 2,681<br>Mdn 18,464, IQR 3,906 | 19,671 ± 2,881<br>Mdn 19,752, IQR 4,434 |
| core, narrative, q 1–5, k=1, n 100–1000 | Naive | 30 | 35.07 ± 16.96<br>Mdn 38.17, IQR 22.92 | 0.031 ± 0.003<br>Mdn 0.031, IQR 0.001 | 35.04 ± 16.96<br>Mdn 38.14, IQR 22.92 | 566.8 ± 251.1<br>Mdn 590.5, IQR 328.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=1, n 100–1000 | KMP | 30 | 31.13 ± 14.34<br>Mdn 34.31, IQR 19.01 | 0.337 ± 0.086<br>Mdn 0.322, IQR 0.138 | 30.80 ± 14.34<br>Mdn 34.09, IQR 18.93 | 565.0 ± 250.1<br>Mdn 588.5, IQR 325.5 | 222 ± 11<br>Mdn 220, IQR 16 | 222 ± 11<br>Mdn 220, IQR 16 | 270 ± 11<br>Mdn 268, IQR 16 |
| core, narrative, q 1–5, k=1, n 100–1000 | Aho-Corasick | 30 | 46.99 ± 21.10<br>Mdn 50.85, IQR 30.77 | 1.275 ± 0.405<br>Mdn 1.209, IQR 0.629 | 45.72 ± 21.08<br>Mdn 49.66, IQR 30.65 | 580.7 ± 250.6<br>Mdn 615.5, IQR 319.2 | 1,392 ± 342<br>Mdn 1,320, IQR 480 | 1,392 ± 342<br>Mdn 1,320, IQR 480 | 2,152 ± 342<br>Mdn 2,080, IQR 480 |
| core, narrative, q 1–5, k=5, n 100–1000 | Naive | 30 | 181.62 ± 103.90<br>Mdn 178.86, IQR 206.39 | 0.032 ± 0.005<br>Mdn 0.031, IQR 0.001 | 181.59 ± 103.90<br>Mdn 178.83, IQR 206.39 | 2,924.3 ± 1,513.3<br>Mdn 2,957.5, IQR 2,847.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=5, n 100–1000 | KMP | 30 | 162.14 ± 89.42<br>Mdn 164.05, IQR 175.20 | 1.387 ± 0.233<br>Mdn 1.373, IQR 0.315 | 160.75 ± 89.35<br>Mdn 162.75, IQR 175.00 | 2,914.3 ± 1,506.4<br>Mdn 2,944.5, IQR 2,835.2 | 578 ± 30<br>Mdn 580, IQR 38 | 578 ± 30<br>Mdn 580, IQR 38 | 626 ± 30<br>Mdn 628, IQR 38 |
| core, narrative, q 1–5, k=5, n 100–1000 | Aho-Corasick | 30 | 62.34 ± 31.90<br>Mdn 60.79, IQR 60.61 | 4.979 ± 1.159<br>Mdn 4.976, IQR 1.761 | 57.36 ± 31.47<br>Mdn 56.29, IQR 60.46 | 740.0 ± 383.0<br>Mdn 712.5, IQR 731.8 | 4,223 ± 1,030<br>Mdn 4,196, IQR 1,572 | 4,247 ± 1,033<br>Mdn 4,226, IQR 1,602 | 5,007 ± 1,033<br>Mdn 4,986, IQR 1,602 |
| core, narrative, q 5–10, k=1, n 100–1000 | Naive | 30 | 27.72 ± 15.60<br>Mdn 23.66, IQR 25.95 | 0.032 ± 0.006<br>Mdn 0.031, IQR 0.001 | 27.69 ± 15.60<br>Mdn 23.63, IQR 25.94 | 479.8 ± 225.7<br>Mdn 422.0, IQR 348.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=1, n 100–1000 | KMP | 30 | 25.19 ± 13.03<br>Mdn 22.18, IQR 21.60 | 0.619 ± 0.092<br>Mdn 0.627, IQR 0.143 | 24.57 ± 13.03<br>Mdn 21.56, IQR 21.49 | 481.4 ± 223.2<br>Mdn 425.5, IQR 346.8 | 263 ± 13<br>Mdn 264, IQR 16 | 263 ± 13<br>Mdn 264, IQR 16 | 313 ± 14<br>Mdn 312, IQR 16 |
| core, narrative, q 5–10, k=1, n 100–1000 | Aho-Corasick | 30 | 39.09 ± 18.64<br>Mdn 34.63, IQR 30.07 | 2.760 ± 0.463<br>Mdn 2.857, IQR 0.692 | 36.33 ± 18.63<br>Mdn 31.94, IQR 30.42 | 490.7 ± 223.3<br>Mdn 434.5, IQR 346.8 | 2,738 ± 474<br>Mdn 2,832, IQR 672 | 2,742 ± 472<br>Mdn 2,832, IQR 672 | 3,502 ± 472<br>Mdn 3,592, IQR 672 |
| core, narrative, q 5–10, k=5, n 100–1000 | Naive | 30 | 183.59 ± 107.54<br>Mdn 179.37, IQR 202.69 | 0.032 ± 0.009<br>Mdn 0.031, IQR 0.001 | 183.56 ± 107.54<br>Mdn 179.34, IQR 202.70 | 2,979.4 ± 1,567.1<br>Mdn 2,925.0, IQR 2,923.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=5, n 100–1000 | KMP | 30 | 162.99 ± 89.64<br>Mdn 159.73, IQR 170.62 | 2.488 ± 0.209<br>Mdn 2.495, IQR 0.232 | 160.50 ± 89.66<br>Mdn 157.04, IQR 171.23 | 2,974.3 ± 1,549.6<br>Mdn 2,923.5, IQR 2,885.5 | 739 ± 28<br>Mdn 740, IQR 24 | 739 ± 28<br>Mdn 740, IQR 24 | 791 ± 31<br>Mdn 792, IQR 34 |
| core, narrative, q 5–10, k=5, n 100–1000 | Aho-Corasick | 30 | 65.18 ± 29.26<br>Mdn 65.29, IQR 54.01 | 11.159 ± 1.145<br>Mdn 11.189, IQR 1.266 | 54.02 ± 29.41<br>Mdn 52.84, IQR 56.42 | 773.1 ± 363.2<br>Mdn 794.5, IQR 655.8 | 9,478 ± 974<br>Mdn 9,560, IQR 1,140 | 9,536 ± 970<br>Mdn 9,560, IQR 1,170 | 10,296 ± 970<br>Mdn 10,320, IQR 1,170 |
| core, narrative, q 10–20, k=1, n 100–1000 | Naive | 30 | 39.29 ± 24.77<br>Mdn 38.04, IQR 45.10 | 0.031 ± 0.001<br>Mdn 0.031, IQR 0.001 | 39.26 ± 24.77<br>Mdn 38.01, IQR 45.10 | 638.9 ± 358.5<br>Mdn 637.0, IQR 659.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=1, n 100–1000 | KMP | 30 | 35.60 ± 21.13<br>Mdn 33.89, IQR 39.05 | 1.006 ± 0.193<br>Mdn 0.997, IQR 0.286 | 34.59 ± 21.13<br>Mdn 32.90, IQR 39.38 | 645.0 ± 352.7<br>Mdn 634.0, IQR 646.0 | 318 ± 23<br>Mdn 316, IQR 38 | 318 ± 23<br>Mdn 316, IQR 38 | 381 ± 35<br>Mdn 384, IQR 41 |
| core, narrative, q 10–20, k=1, n 100–1000 | Aho-Corasick | 30 | 54.04 ± 28.71<br>Mdn 51.60, IQR 53.99 | 4.784 ± 0.846<br>Mdn 4.692, IQR 1.067 | 49.25 ± 28.76<br>Mdn 46.80, IQR 53.83 | 662.1 ± 352.9<br>Mdn 650.5, IQR 644.2 | 4,554 ± 778<br>Mdn 4,392, IQR 1,332 | 4,584 ± 789<br>Mdn 4,452, IQR 1,332 | 5,344 ± 789<br>Mdn 5,212, IQR 1,332 |
| core, narrative, q 10–20, k=5, n 100–1000 | Naive | 30 | 180.67 ± 91.67<br>Mdn 172.85, IQR 165.87 | 0.032 ± 0.005<br>Mdn 0.031, IQR 0.001 | 180.63 ± 91.67<br>Mdn 172.82, IQR 165.86 | 2,981.3 ± 1,332.2<br>Mdn 2,967.5, IQR 2,397.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=5, n 100–1000 | KMP | 30 | 164.00 ± 77.89<br>Mdn 155.58, IQR 139.75 | 4.611 ± 0.477<br>Mdn 4.634, IQR 0.525 | 159.39 ± 77.81<br>Mdn 151.22, IQR 139.63 | 3,015.7 ± 1,319.1<br>Mdn 2,917.0, IQR 2,402.8 | 1,061 ± 58<br>Mdn 1,076, IQR 84 | 1,061 ± 58<br>Mdn 1,076, IQR 84 | 1,118 ± 60<br>Mdn 1,128, IQR 80 |
| core, narrative, q 10–20, k=5, n 100–1000 | Aho-Corasick | 30 | 77.11 ± 25.50<br>Mdn 74.72, IQR 48.04 | 24.068 ± 2.649<br>Mdn 24.103, IQR 3.190 | 53.04 ± 25.07<br>Mdn 51.65, IQR 43.85 | 862.8 ± 322.4<br>Mdn 825.0, IQR 586.8 | 20,081 ± 1,852<br>Mdn 20,464, IQR 2,544 | 20,169 ± 1,864<br>Mdn 20,524, IQR 2,482 | 21,386 ± 1,987<br>Mdn 21,812, IQR 2,482 |
| core, narrative, q 1–5, k=1, n 1000–10000 | Naive | 30 | 438.18 ± 231.84<br>Mdn 513.87, IQR 427.20 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.002 | 438.15 ± 231.84<br>Mdn 513.83, IQR 427.20 | 6,444.7 ± 3,314.0<br>Mdn 7,474.5, IQR 6,257.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=1, n 1000–10000 | KMP | 30 | 374.62 ± 197.14<br>Mdn 420.18, IQR 352.89 | 0.359 ± 0.110<br>Mdn 0.345, IQR 0.183 | 374.26 ± 197.16<br>Mdn 419.86, IQR 352.84 | 6,410.3 ± 3,290.8<br>Mdn 7,420.0, IQR 6,251.8 | 223 ± 13<br>Mdn 224, IQR 30 | 223 ± 13<br>Mdn 224, IQR 30 | 272 ± 15<br>Mdn 272, IQR 30 |
| core, narrative, q 1–5, k=1, n 1000–10000 | Aho-Corasick | 30 | 532.03 ± 275.15<br>Mdn 608.07, IQR 493.22 | 1.331 ± 0.464<br>Mdn 1.366, IQR 1.052 | 530.70 ± 275.15<br>Mdn 606.22, IQR 493.01 | 6,498.2 ± 3,316.6<br>Mdn 7,470.0, IQR 6,042.2 | 1,416 ± 390<br>Mdn 1,440, IQR 900 | 1,418 ± 393<br>Mdn 1,440, IQR 900 | 2,178 ± 393<br>Mdn 2,200, IQR 900 |
| core, narrative, q 1–5, k=5, n 1000–10000 | Naive | 30 | 1,870.75 ± 1,001.95<br>Mdn 1,754.52, IQR 1,424.64 | 0.033 ± 0.002<br>Mdn 0.034, IQR 0.001 | 1,870.71 ± 1,001.95<br>Mdn 1,754.48, IQR 1,424.63 | 27,053.4 ± 14,402.5<br>Mdn 26,587.0, IQR 20,619.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 1–5, k=5, n 1000–10000 | KMP | 30 | 1,603.98 ± 849.43<br>Mdn 1,590.18, IQR 1,206.22 | 1.415 ± 0.228<br>Mdn 1.410, IQR 0.248 | 1,602.56 ± 849.43<br>Mdn 1,588.70, IQR 1,206.05 | 26,808.6 ± 14,241.8<br>Mdn 26,482.0, IQR 20,351.8 | 577 ± 25<br>Mdn 576, IQR 30 | 577 ± 25<br>Mdn 576, IQR 30 | 627 ± 25<br>Mdn 628, IQR 31 |
| core, narrative, q 1–5, k=5, n 1000–10000 | Aho-Corasick | 30 | 561.42 ± 294.71<br>Mdn 574.49, IQR 408.28 | 4.933 ± 0.876<br>Mdn 4.971, IQR 0.969 | 556.49 ± 294.77<br>Mdn 569.04, IQR 408.22 | 6,657.7 ± 3,522.2<br>Mdn 6,505.0, IQR 4,562.2 | 4,168 ± 792<br>Mdn 4,192, IQR 1,096 | 4,192 ± 800<br>Mdn 4,196, IQR 1,137 | 4,952 ± 799<br>Mdn 4,956, IQR 1,137 |
| core, narrative, q 5–10, k=1, n 1000–10000 | Naive | 30 | 408.28 ± 233.30<br>Mdn 434.17, IQR 377.05 | 0.031 ± 0.003<br>Mdn 0.032, IQR 0.006 | 408.25 ± 233.30<br>Mdn 434.14, IQR 377.06 | 5,877.4 ± 3,187.9<br>Mdn 6,459.0, IQR 5,163.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=1, n 1000–10000 | KMP | 30 | 340.33 ± 194.04<br>Mdn 361.00, IQR 323.99 | 0.630 ± 0.127<br>Mdn 0.606, IQR 0.114 | 339.70 ± 194.04<br>Mdn 360.41, IQR 324.06 | 5,791.8 ± 3,125.8<br>Mdn 6,201.0, IQR 5,041.8 | 262 ± 12<br>Mdn 264, IQR 22 | 262 ± 12<br>Mdn 264, IQR 22 | 318 ± 24<br>Mdn 312, IQR 19 |
| core, narrative, q 5–10, k=1, n 1000–10000 | Aho-Corasick | 30 | 475.02 ± 260.02<br>Mdn 528.50, IQR 448.25 | 2.763 ± 0.511<br>Mdn 2.786, IQR 0.862 | 472.25 ± 260.19<br>Mdn 525.88, IQR 448.28 | 5,805.1 ± 3,126.3<br>Mdn 6,261.5, IQR 5,040.2 | 2,677 ± 449<br>Mdn 2,832, IQR 852 | 2,691 ± 445<br>Mdn 2,832, IQR 762 | 3,451 ± 445<br>Mdn 3,592, IQR 762 |
| core, narrative, q 5–10, k=5, n 1000–10000 | Naive | 30 | 2,092.15 ± 1,088.35<br>Mdn 2,223.93, IQR 2,055.27 | 0.033 ± 0.003<br>Mdn 0.034, IQR 0.004 | 2,092.12 ± 1,088.35<br>Mdn 2,223.89, IQR 2,055.27 | 30,390.9 ± 15,177.7<br>Mdn 32,584.5, IQR 29,234.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 5–10, k=5, n 1000–10000 | KMP | 30 | 1,768.13 ± 906.89<br>Mdn 1,783.14, IQR 1,692.14 | 2.677 ± 0.657<br>Mdn 2.530, IQR 0.260 | 1,765.46 ± 906.90<br>Mdn 1,780.77, IQR 1,692.22 | 30,050.3 ± 14,970.3<br>Mdn 32,260.5, IQR 28,661.5 | 753 ± 28<br>Mdn 752, IQR 32 | 753 ± 28<br>Mdn 752, IQR 32 | 808 ± 34<br>Mdn 800, IQR 38 |
| core, narrative, q 5–10, k=5, n 1000–10000 | Aho-Corasick | 30 | 581.25 ± 291.12<br>Mdn 590.88, IQR 507.21 | 11.304 ± 1.181<br>Mdn 11.260, IQR 1.342 | 569.95 ± 291.14<br>Mdn 580.56, IQR 507.86 | 7,126.4 ± 3,433.8<br>Mdn 7,516.0, IQR 5,915.2 | 9,936 ± 1,047<br>Mdn 9,808, IQR 1,140 | 10,004 ± 1,073<br>Mdn 9,898, IQR 1,140 | 10,764 ± 1,073<br>Mdn 10,658, IQR 1,140 |
| core, narrative, q 10–20, k=1, n 1000–10000 | Naive | 30 | 392.38 ± 217.22<br>Mdn 430.78, IQR 369.18 | 0.032 ± 0.004<br>Mdn 0.033, IQR 0.006 | 392.35 ± 217.22<br>Mdn 430.75, IQR 369.20 | 5,868.7 ± 3,144.4<br>Mdn 6,281.0, IQR 5,348.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=1, n 1000–10000 | KMP | 30 | 328.86 ± 178.44<br>Mdn 353.38, IQR 274.23 | 0.954 ± 0.175<br>Mdn 0.975, IQR 0.250 | 327.90 ± 178.39<br>Mdn 352.36, IQR 274.53 | 5,811.5 ± 3,103.0<br>Mdn 6,278.0, IQR 5,295.2 | 314 ± 22<br>Mdn 312, IQR 38 | 314 ± 22<br>Mdn 312, IQR 38 | 367 ± 26<br>Mdn 360, IQR 43 |
| core, narrative, q 10–20, k=1, n 1000–10000 | Aho-Corasick | 30 | 476.81 ± 255.75<br>Mdn 524.37, IQR 416.29 | 4.559 ± 0.748<br>Mdn 4.445, IQR 1.207 | 472.25 ± 255.80<br>Mdn 520.72, IQR 417.37 | 5,827.4 ± 3,103.6<br>Mdn 6,298.5, IQR 5,291.0 | 4,392 ± 735<br>Mdn 4,272, IQR 1,332 | 4,406 ± 739<br>Mdn 4,272, IQR 1,347 | 5,166 ± 739<br>Mdn 5,032, IQR 1,347 |
| core, narrative, q 10–20, k=5, n 1000–10000 | Naive | 30 | 2,060.08 ± 903.56<br>Mdn 1,853.47, IQR 1,565.60 | 0.033 ± 0.003<br>Mdn 0.033, IQR 0.004 | 2,060.05 ± 903.55<br>Mdn 1,853.44, IQR 1,565.60 | 30,651.9 ± 13,573.0<br>Mdn 27,434.0, IQR 24,006.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| core, narrative, q 10–20, k=5, n 1000–10000 | KMP | 30 | 1,759.00 ± 781.21<br>Mdn 1,592.40, IQR 1,269.43 | 4.624 ± 0.489<br>Mdn 4.642, IQR 0.510 | 1,754.37 ± 781.12<br>Mdn 1,588.32, IQR 1,269.46 | 30,399.5 ± 13,446.1<br>Mdn 27,172.0, IQR 23,956.0 | 1,069 ± 64<br>Mdn 1,092, IQR 88 | 1,069 ± 64<br>Mdn 1,092, IQR 88 | 1,126 ± 69<br>Mdn 1,144, IQR 100 |
| core, narrative, q 10–20, k=5, n 1000–10000 | Aho-Corasick | 30 | 596.54 ± 259.48<br>Mdn 538.61, IQR 453.01 | 23.325 ± 2.704<br>Mdn 23.591, IQR 3.921 | 573.22 ± 259.10<br>Mdn 517.36, IQR 457.95 | 7,376.9 ± 3,151.4<br>Mdn 6,799.0, IQR 5,428.2 | 20,418 ± 2,164<br>Mdn 21,136, IQR 3,024 | 20,526 ± 2,186<br>Mdn 21,196, IQR 3,249 | 21,743 ± 2,318<br>Mdn 22,484, IQR 3,249 |
| query_pattern, distinct, n 10–100 | Naive | 30 | 2.57 ± 1.30<br>Mdn 2.48, IQR 2.11 | 0.034 ± 0.002<br>Mdn 0.032, IQR 0.004 | 2.54 ± 1.30<br>Mdn 2.45, IQR 2.11 | 46.2 ± 26.6<br>Mdn 45.0, IQR 42.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, distinct, n 10–100 | KMP | 30 | 3.28 ± 1.21<br>Mdn 3.23, IQR 2.13 | 0.596 ± 0.084<br>Mdn 0.600, IQR 0.111 | 2.68 ± 1.22<br>Mdn 2.63, IQR 2.08 | 59.7 ± 26.4<br>Mdn 59.0, IQR 46.8 | 262 ± 13<br>Mdn 264, IQR 16 | 262 ± 13<br>Mdn 264, IQR 16 | 310 ± 13<br>Mdn 312, IQR 16 |
| query_pattern, distinct, n 10–100 | Aho-Corasick | 30 | 6.92 ± 1.91<br>Mdn 7.06, IQR 3.25 | 2.885 ± 0.521<br>Mdn 2.982, IQR 0.848 | 4.03 ± 1.88<br>Mdn 3.96, IQR 3.18 | 67.5 ± 26.4<br>Mdn 68.0, IQR 47.0 | 2,691 ± 468<br>Mdn 2,832, IQR 672 | 2,691 ± 468<br>Mdn 2,832, IQR 672 | 3,451 ± 468<br>Mdn 3,592, IQR 672 |
| query_pattern, repeating, n 10–100 | Naive | 30 | 2.74 ± 1.33<br>Mdn 2.61, IQR 2.02 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 2.71 ± 1.33<br>Mdn 2.58, IQR 2.02 | 49.5 ± 27.2<br>Mdn 48.0, IQR 40.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, repeating, n 10–100 | KMP | 30 | 3.47 ± 1.25<br>Mdn 3.35, IQR 1.86 | 0.606 ± 0.085<br>Mdn 0.624, IQR 0.122 | 2.86 ± 1.25<br>Mdn 2.71, IQR 1.88 | 63.9 ± 27.1<br>Mdn 60.0, IQR 35.5 | 265 ± 13<br>Mdn 268, IQR 22 | 265 ± 13<br>Mdn 268, IQR 22 | 313 ± 13<br>Mdn 316, IQR 22 |
| query_pattern, repeating, n 10–100 | Aho-Corasick | 30 | 7.26 ± 1.97<br>Mdn 7.32, IQR 3.37 | 2.940 ± 0.490<br>Mdn 3.022, IQR 0.837 | 4.32 ± 1.93<br>Mdn 4.23, IQR 2.86 | 72.0 ± 27.2<br>Mdn 70.0, IQR 37.2 | 2,808 ± 471<br>Mdn 2,952, IQR 852 | 2,808 ± 471<br>Mdn 2,952, IQR 852 | 3,568 ± 471<br>Mdn 3,712, IQR 852 |
| query_pattern, distinct, n 100–1000 | Naive | 30 | 29.64 ± 16.90<br>Mdn 26.74, IQR 22.18 | 0.032 ± 0.006<br>Mdn 0.031, IQR 0.000 | 29.61 ± 16.90<br>Mdn 26.71, IQR 22.18 | 504.7 ± 248.8<br>Mdn 462.0, IQR 312.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, distinct, n 100–1000 | KMP | 30 | 27.14 ± 14.43<br>Mdn 24.35, IQR 18.21 | 0.580 ± 0.079<br>Mdn 0.583, IQR 0.104 | 26.56 ± 14.42<br>Mdn 23.79, IQR 18.29 | 517.3 ± 248.9<br>Mdn 472.0, IQR 310.8 | 259 ± 12<br>Mdn 260, IQR 20 | 259 ± 12<br>Mdn 260, IQR 20 | 307 ± 12<br>Mdn 308, IQR 20 |
| query_pattern, distinct, n 100–1000 | Aho-Corasick | 30 | 42.20 ± 21.03<br>Mdn 38.17, IQR 23.68 | 2.576 ± 0.457<br>Mdn 2.612, IQR 0.659 | 39.62 ± 20.99<br>Mdn 35.61, IQR 23.63 | 524.7 ± 249.1<br>Mdn 478.0, IQR 310.0 | 2,576 ± 450<br>Mdn 2,616, IQR 792 | 2,576 ± 450<br>Mdn 2,616, IQR 792 | 3,336 ± 450<br>Mdn 3,376, IQR 792 |
| query_pattern, repeating, n 100–1000 | Naive | 30 | 31.19 ± 17.25<br>Mdn 29.87, IQR 31.73 | 0.033 ± 0.007<br>Mdn 0.031, IQR 0.001 | 31.16 ± 17.26<br>Mdn 29.82, IQR 31.73 | 520.7 ± 253.2<br>Mdn 513.0, IQR 439.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, repeating, n 100–1000 | KMP | 30 | 28.08 ± 14.37<br>Mdn 26.68, IQR 25.96 | 0.596 ± 0.080<br>Mdn 0.605, IQR 0.125 | 27.48 ± 14.38<br>Mdn 26.05, IQR 25.90 | 534.6 ± 252.5<br>Mdn 528.5, IQR 438.5 | 264 ± 13<br>Mdn 264, IQR 22 | 264 ± 13<br>Mdn 264, IQR 22 | 312 ± 13<br>Mdn 312, IQR 22 |
| query_pattern, repeating, n 100–1000 | Aho-Corasick | 30 | 43.46 ± 20.68<br>Mdn 43.20, IQR 37.30 | 2.704 ± 0.458<br>Mdn 2.666, IQR 0.755 | 40.76 ± 20.72<br>Mdn 40.26, IQR 37.71 | 542.7 ± 252.4<br>Mdn 537.5, IQR 436.8 | 2,763 ± 464<br>Mdn 2,832, IQR 852 | 2,763 ± 464<br>Mdn 2,832, IQR 852 | 3,523 ± 464<br>Mdn 3,592, IQR 852 |
| query_pattern, distinct, n 1000–10000 | Naive | 30 | 330.78 ± 195.73<br>Mdn 377.69, IQR 334.65 | 0.039 ± 0.036<br>Mdn 0.033, IQR 0.005 | 330.74 ± 195.72<br>Mdn 377.66, IQR 334.65 | 4,951.7 ± 2,845.3<br>Mdn 5,745.0, IQR 4,720.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, distinct, n 1000–10000 | KMP | 30 | 280.91 ± 167.49<br>Mdn 326.00, IQR 268.09 | 0.613 ± 0.140<br>Mdn 0.621, IQR 0.173 | 280.30 ± 167.50<br>Mdn 325.48, IQR 267.94 | 4,965.0 ± 2,845.8<br>Mdn 5,756.0, IQR 4,722.0 | 262 ± 15<br>Mdn 264, IQR 24 | 262 ± 15<br>Mdn 264, IQR 24 | 310 ± 15<br>Mdn 312, IQR 24 |
| query_pattern, distinct, n 1000–10000 | Aho-Corasick | 30 | 413.35 ± 242.87<br>Mdn 460.93, IQR 386.02 | 2.741 ± 0.607<br>Mdn 2.762, IQR 0.914 | 410.61 ± 242.88<br>Mdn 458.60, IQR 385.60 | 4,972.7 ± 2,846.1<br>Mdn 5,762.5, IQR 4,723.0 | 2,670 ± 554<br>Mdn 2,832, IQR 912 | 2,670 ± 554<br>Mdn 2,832, IQR 912 | 3,430 ± 554<br>Mdn 3,592, IQR 912 |
| query_pattern, repeating, n 1000–10000 | Naive | 30 | 417.10 ± 167.35<br>Mdn 454.54, IQR 225.65 | 0.033 ± 0.003<br>Mdn 0.034, IQR 0.002 | 417.07 ± 167.35<br>Mdn 454.52, IQR 225.65 | 6,151.2 ± 2,393.6<br>Mdn 6,598.5, IQR 3,332.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| query_pattern, repeating, n 1000–10000 | KMP | 30 | 348.32 ± 139.57<br>Mdn 378.71, IQR 201.16 | 0.549 ± 0.090<br>Mdn 0.539, IQR 0.160 | 347.77 ± 139.57<br>Mdn 378.27, IQR 201.21 | 6,160.2 ± 2,392.4<br>Mdn 6,591.5, IQR 3,315.0 | 257 ± 15<br>Mdn 252, IQR 30 | 257 ± 15<br>Mdn 252, IQR 30 | 305 ± 15<br>Mdn 300, IQR 30 |
| query_pattern, repeating, n 1000–10000 | Aho-Corasick | 30 | 505.49 ± 197.82<br>Mdn 545.48, IQR 263.98 | 2.494 ± 0.525<br>Mdn 2.451, IQR 0.789 | 503.00 ± 197.70<br>Mdn 543.49, IQR 263.53 | 6,167.3 ± 2,392.8<br>Mdn 6,596.5, IQR 3,312.2 | 2,493 ± 526<br>Mdn 2,280, IQR 1,092 | 2,493 ± 526<br>Mdn 2,280, IQR 1,092 | 3,253 ± 526<br>Mdn 3,040, IQR 1,092 |
| alphabet, |Σ|=2, n 10–100 | Naive | 30 | 5.22 ± 2.40<br>Mdn 5.13, IQR 3.91 | 0.033 ± 0.002<br>Mdn 0.032, IQR 0.004 | 5.18 ± 2.40<br>Mdn 5.09, IQR 3.91 | 98.2 ± 48.3<br>Mdn 95.5, IQR 77.5 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=2, n 10–100 | KMP | 30 | 4.86 ± 1.79<br>Mdn 4.81, IQR 2.88 | 0.677 ± 0.171<br>Mdn 0.648, IQR 0.290 | 4.18 ± 1.80<br>Mdn 4.29, IQR 2.83 | 82.8 ± 33.6<br>Mdn 82.5, IQR 49.5 | 258 ± 16<br>Mdn 256, IQR 30 | 258 ± 16<br>Mdn 256, IQR 30 | 306 ± 16<br>Mdn 304, IQR 30 |
| alphabet, |Σ|=2, n 10–100 | Aho-Corasick | 30 | 7.80 ± 2.14<br>Mdn 7.66, IQR 3.11 | 2.793 ± 0.645<br>Mdn 2.702, IQR 1.256 | 5.01 ± 2.10<br>Mdn 4.90, IQR 3.38 | 93.7 ± 34.1<br>Mdn 92.0, IQR 47.2 | 2,541 ± 560<br>Mdn 2,400, IQR 1,092 | 2,541 ± 560<br>Mdn 2,400, IQR 1,092 | 3,301 ± 560<br>Mdn 3,160, IQR 1,092 |
| alphabet, |Σ|=2, n 100–1000 | Naive | 30 | 72.68 ± 35.82<br>Mdn 76.86, IQR 70.40 | 0.031 ± 0.003<br>Mdn 0.031, IQR 0.000 | 72.65 ± 35.82<br>Mdn 76.82, IQR 70.40 | 1,230.5 ± 550.8<br>Mdn 1,340.5, IQR 1,055.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=2, n 100–1000 | KMP | 30 | 52.76 ± 24.06<br>Mdn 56.36, IQR 44.00 | 0.653 ± 0.146<br>Mdn 0.660, IQR 0.222 | 52.11 ± 24.05<br>Mdn 55.54, IQR 43.84 | 885.3 ± 382.7<br>Mdn 947.0, IQR 698.5 | 256 ± 14<br>Mdn 256, IQR 30 | 256 ± 14<br>Mdn 256, IQR 30 | 304 ± 14<br>Mdn 304, IQR 30 |
| alphabet, |Σ|=2, n 100–1000 | Aho-Corasick | 30 | 62.08 ± 27.38<br>Mdn 66.06, IQR 51.22 | 2.522 ± 0.551<br>Mdn 2.464, IQR 1.012 | 59.56 ± 27.26<br>Mdn 63.05, IQR 51.12 | 903.0 ± 384.7<br>Mdn 961.5, IQR 711.0 | 2,490 ± 522<br>Mdn 2,400, IQR 1,092 | 2,490 ± 522<br>Mdn 2,400, IQR 1,092 | 3,250 ± 522<br>Mdn 3,160, IQR 1,092 |
| alphabet, |Σ|=2, n 1000–10000 | Naive | 30 | 780.23 ± 354.89<br>Mdn 889.53, IQR 597.59 | 0.032 ± 0.003<br>Mdn 0.033, IQR 0.005 | 780.20 ± 354.89<br>Mdn 889.50, IQR 597.59 | 12,077.2 ± 5,416.3<br>Mdn 13,683.5, IQR 9,281.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=2, n 1000–10000 | KMP | 30 | 522.42 ± 237.82<br>Mdn 582.33, IQR 396.46 | 0.732 ± 0.148<br>Mdn 0.723, IQR 0.187 | 521.69 ± 237.82<br>Mdn 581.75, IQR 396.40 | 8,547.4 ± 3,808.4<br>Mdn 9,899.5, IQR 6,503.2 | 263 ± 13<br>Mdn 264, IQR 14 | 263 ± 13<br>Mdn 264, IQR 14 | 311 ± 13<br>Mdn 312, IQR 14 |
| alphabet, |Σ|=2, n 1000–10000 | Aho-Corasick | 30 | 602.89 ± 273.78<br>Mdn 695.82, IQR 476.11 | 2.812 ± 0.495<br>Mdn 2.850, IQR 0.621 | 600.07 ± 273.78<br>Mdn 692.40, IQR 476.56 | 8,604.4 ± 3,821.0<br>Mdn 9,967.0, IQR 6,583.5 | 2,757 ± 467<br>Mdn 2,832, IQR 564 | 2,757 ± 467<br>Mdn 2,832, IQR 564 | 3,517 ± 467<br>Mdn 3,592, IQR 564 |
| alphabet, |Σ|=4, n 10–100 | Naive | 30 | 4.10 ± 1.70<br>Mdn 4.31, IQR 2.22 | 0.035 ± 0.006<br>Mdn 0.032, IQR 0.004 | 4.06 ± 1.69<br>Mdn 4.28, IQR 2.22 | 75.9 ± 33.9<br>Mdn 82.0, IQR 43.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=4, n 10–100 | KMP | 30 | 4.51 ± 1.54<br>Mdn 4.84, IQR 1.77 | 0.647 ± 0.112<br>Mdn 0.660, IQR 0.166 | 3.86 ± 1.54<br>Mdn 4.16, IQR 1.91 | 79.0 ± 31.3<br>Mdn 85.0, IQR 37.8 | 260 ± 14<br>Mdn 256, IQR 24 | 260 ± 14<br>Mdn 256, IQR 24 | 308 ± 14<br>Mdn 304, IQR 24 |
| alphabet, |Σ|=4, n 10–100 | Aho-Corasick | 30 | 7.90 ± 2.02<br>Mdn 7.81, IQR 2.45 | 2.841 ± 0.576<br>Mdn 2.786, IQR 0.916 | 5.06 ± 2.05<br>Mdn 5.42, IQR 2.45 | 88.7 ± 31.5<br>Mdn 93.0, IQR 38.2 | 2,602 ± 509<br>Mdn 2,400, IQR 912 | 2,602 ± 509<br>Mdn 2,400, IQR 912 | 3,362 ± 509<br>Mdn 3,160, IQR 912 |
| alphabet, |Σ|=4, n 100–1000 | Naive | 30 | 38.51 ± 22.11<br>Mdn 36.85, IQR 29.47 | 0.034 ± 0.008<br>Mdn 0.031, IQR 0.000 | 38.48 ± 22.12<br>Mdn 36.82, IQR 29.49 | 664.5 ± 337.3<br>Mdn 652.5, IQR 417.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=4, n 100–1000 | KMP | 30 | 34.10 ± 17.95<br>Mdn 32.95, IQR 23.36 | 0.659 ± 0.122<br>Mdn 0.661, IQR 0.159 | 33.44 ± 17.94<br>Mdn 32.31, IQR 23.22 | 626.5 ± 314.7<br>Mdn 610.0, IQR 397.5 | 261 ± 12<br>Mdn 256, IQR 16 | 261 ± 12<br>Mdn 256, IQR 16 | 309 ± 12<br>Mdn 304, IQR 16 |
| alphabet, |Σ|=4, n 100–1000 | Aho-Corasick | 30 | 46.44 ± 23.33<br>Mdn 45.48, IQR 29.90 | 2.695 ± 0.465<br>Mdn 2.587, IQR 0.676 | 43.75 ± 23.32<br>Mdn 42.14, IQR 29.57 | 636.6 ± 314.8<br>Mdn 622.5, IQR 399.2 | 2,626 ± 452<br>Mdn 2,400, IQR 672 | 2,626 ± 452<br>Mdn 2,400, IQR 672 | 3,386 ± 452<br>Mdn 3,160, IQR 672 |
| alphabet, |Σ|=4, n 1000–10000 | Naive | 30 | 528.17 ± 244.17<br>Mdn 535.22, IQR 464.03 | 0.037 ± 0.026<br>Mdn 0.033, IQR 0.001 | 528.13 ± 244.17<br>Mdn 535.19, IQR 464.03 | 8,058.1 ± 3,626.2<br>Mdn 8,163.5, IQR 6,950.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=4, n 1000–10000 | KMP | 30 | 437.05 ± 200.64<br>Mdn 437.20, IQR 383.80 | 0.686 ± 0.147<br>Mdn 0.698, IQR 0.206 | 436.36 ± 200.66<br>Mdn 436.70, IQR 383.90 | 7,515.0 ± 3,375.5<br>Mdn 7,628.5, IQR 6,508.0 | 264 ± 14<br>Mdn 268, IQR 24 | 264 ± 14<br>Mdn 268, IQR 24 | 312 ± 14<br>Mdn 316, IQR 24 |
| alphabet, |Σ|=4, n 1000–10000 | Aho-Corasick | 30 | 563.70 ± 257.91<br>Mdn 580.80, IQR 474.59 | 2.930 ± 0.607<br>Mdn 3.017, IQR 1.122 | 560.77 ± 258.01<br>Mdn 577.90, IQR 474.61 | 7,526.9 ± 3,375.8<br>Mdn 7,638.5, IQR 6,507.5 | 2,768 ± 503<br>Mdn 2,952, IQR 912 | 2,768 ± 503<br>Mdn 2,952, IQR 912 | 3,528 ± 503<br>Mdn 3,712, IQR 912 |
| alphabet, |Σ|=26, n 10–100 | Naive | 30 | 3.70 ± 1.29<br>Mdn 3.77, IQR 1.86 | 0.034 ± 0.002<br>Mdn 0.032, IQR 0.004 | 3.67 ± 1.29<br>Mdn 3.74, IQR 1.86 | 68.9 ± 26.5<br>Mdn 73.0, IQR 37.2 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=26, n 10–100 | KMP | 30 | 4.11 ± 1.22<br>Mdn 4.23, IQR 1.69 | 0.638 ± 0.087<br>Mdn 0.659, IQR 0.142 | 3.47 ± 1.21<br>Mdn 3.55, IQR 1.79 | 76.4 ± 26.6<br>Mdn 80.5, IQR 36.5 | 267 ± 12<br>Mdn 268, IQR 24 | 267 ± 12<br>Mdn 268, IQR 24 | 315 ± 12<br>Mdn 316, IQR 24 |
| alphabet, |Σ|=26, n 10–100 | Aho-Corasick | 30 | 8.13 ± 1.87<br>Mdn 8.44, IQR 2.59 | 3.050 ± 0.483<br>Mdn 3.061, IQR 0.952 | 5.08 ± 1.81<br>Mdn 5.25, IQR 2.65 | 86.1 ± 26.9<br>Mdn 90.0, IQR 36.8 | 2,864 ± 442<br>Mdn 2,952, IQR 912 | 2,864 ± 442<br>Mdn 2,952, IQR 912 | 3,624 ± 442<br>Mdn 3,712, IQR 912 |
| alphabet, |Σ|=26, n 100–1000 | Naive | 30 | 29.63 ± 16.94<br>Mdn 27.42, IQR 30.94 | 0.031 ± 0.001<br>Mdn 0.031, IQR 0.001 | 29.60 ± 16.94<br>Mdn 27.39, IQR 30.94 | 511.8 ± 260.9<br>Mdn 477.5, IQR 472.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=26, n 100–1000 | KMP | 30 | 26.94 ± 14.64<br>Mdn 25.07, IQR 25.35 | 0.616 ± 0.092<br>Mdn 0.655, IQR 0.139 | 26.33 ± 14.63<br>Mdn 24.41, IQR 25.34 | 518.2 ± 260.4<br>Mdn 484.5, IQR 464.8 | 263 ± 15<br>Mdn 268, IQR 22 | 263 ± 15<br>Mdn 268, IQR 22 | 311 ± 15<br>Mdn 316, IQR 22 |
| alphabet, |Σ|=26, n 100–1000 | Aho-Corasick | 30 | 41.61 ± 21.23<br>Mdn 39.86, IQR 37.37 | 2.757 ± 0.522<br>Mdn 2.953, IQR 0.886 | 38.86 ± 21.12<br>Mdn 36.85, IQR 38.02 | 527.4 ± 260.8<br>Mdn 494.0, IQR 461.0 | 2,746 ± 523<br>Mdn 2,952, IQR 852 | 2,746 ± 523<br>Mdn 2,952, IQR 852 | 3,506 ± 523<br>Mdn 3,712, IQR 852 |
| alphabet, |Σ|=26, n 1000–10000 | Naive | 30 | 403.46 ± 187.64<br>Mdn 378.78, IQR 332.52 | 0.036 ± 0.026<br>Mdn 0.032, IQR 0.006 | 403.42 ± 187.65<br>Mdn 378.75, IQR 332.52 | 6,032.2 ± 2,694.8<br>Mdn 5,733.5, IQR 4,845.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=26, n 1000–10000 | KMP | 30 | 333.15 ± 157.75<br>Mdn 299.57, IQR 282.46 | 0.609 ± 0.077<br>Mdn 0.639, IQR 0.098 | 332.54 ± 157.79<br>Mdn 298.89, IQR 282.62 | 6,029.5 ± 2,689.3<br>Mdn 5,730.5, IQR 4,834.0 | 262 ± 13<br>Mdn 264, IQR 24 | 262 ± 13<br>Mdn 264, IQR 24 | 310 ± 13<br>Mdn 312, IQR 24 |
| alphabet, |Σ|=26, n 1000–10000 | Aho-Corasick | 30 | 480.07 ± 217.45<br>Mdn 451.97, IQR 371.67 | 2.770 ± 0.554<br>Mdn 2.772, IQR 0.928 | 477.30 ± 217.71<br>Mdn 448.83, IQR 372.35 | 6,038.5 ± 2,688.6<br>Mdn 5,740.0, IQR 4,830.8 | 2,712 ± 486<br>Mdn 2,832, IQR 912 | 2,712 ± 486<br>Mdn 2,832, IQR 912 | 3,472 ± 486<br>Mdn 3,592, IQR 912 |
| alphabet, |Σ|=full, n 10–100 | Naive | 30 | 2.85 ± 1.23<br>Mdn 3.01, IQR 1.60 | 0.032 ± 0.001<br>Mdn 0.032, IQR 0.000 | 2.82 ± 1.23<br>Mdn 2.98, IQR 1.60 | 48.6 ± 23.2<br>Mdn 51.5, IQR 31.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=full, n 10–100 | KMP | 30 | 3.30 ± 1.15<br>Mdn 3.32, IQR 1.47 | 0.590 ± 0.117<br>Mdn 0.576, IQR 0.180 | 2.71 ± 1.15<br>Mdn 2.75, IQR 1.54 | 54.8 ± 23.2<br>Mdn 60.0, IQR 30.8 | 257 ± 15<br>Mdn 256, IQR 30 | 257 ± 15<br>Mdn 256, IQR 30 | 317 ± 24<br>Mdn 316, IQR 34 |
| alphabet, |Σ|=full, n 10–100 | Aho-Corasick | 30 | 6.66 ± 1.83<br>Mdn 6.62, IQR 2.69 | 2.694 ± 0.607<br>Mdn 2.618, IQR 0.963 | 3.97 ± 1.71<br>Mdn 4.09, IQR 2.24 | 63.0 ± 23.4<br>Mdn 66.0, IQR 34.2 | 2,496 ± 531<br>Mdn 2,400, IQR 1,092 | 2,526 ± 549<br>Mdn 2,400, IQR 1,047 | 3,286 ± 549<br>Mdn 3,160, IQR 1,047 |
| alphabet, |Σ|=full, n 100–1000 | Naive | 30 | 35.34 ± 19.24<br>Mdn 35.68, IQR 37.83 | 0.034 ± 0.010<br>Mdn 0.031, IQR 0.000 | 35.30 ± 19.24<br>Mdn 35.65, IQR 37.83 | 574.4 ± 278.5<br>Mdn 584.0, IQR 531.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=full, n 100–1000 | KMP | 30 | 31.66 ± 16.55<br>Mdn 31.79, IQR 31.08 | 0.582 ± 0.095<br>Mdn 0.600, IQR 0.168 | 31.08 ± 16.55<br>Mdn 31.16, IQR 31.14 | 580.7 ± 278.4<br>Mdn 590.5, IQR 527.0 | 258 ± 14<br>Mdn 260, IQR 30 | 258 ± 14<br>Mdn 260, IQR 30 | 317 ± 19<br>Mdn 316, IQR 24 |
| alphabet, |Σ|=full, n 100–1000 | Aho-Corasick | 30 | 49.04 ± 23.54<br>Mdn 50.52, IQR 44.47 | 2.570 ± 0.500<br>Mdn 2.651, IQR 0.841 | 46.47 ± 23.55<br>Mdn 47.89, IQR 45.83 | 588.9 ± 278.5<br>Mdn 599.0, IQR 522.2 | 2,568 ± 506<br>Mdn 2,616, IQR 1,092 | 2,596 ± 507<br>Mdn 2,706, IQR 1,047 | 3,356 ± 507<br>Mdn 3,466, IQR 1,047 |
| alphabet, |Σ|=full, n 1000–10000 | Naive | 30 | 349.01 ± 164.01<br>Mdn 312.99, IQR 215.13 | 0.033 ± 0.002<br>Mdn 0.034, IQR 0.001 | 348.98 ± 164.01<br>Mdn 312.96, IQR 215.14 | 5,046.0 ± 2,259.7<br>Mdn 4,594.0, IQR 2,951.8 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| alphabet, |Σ|=full, n 1000–10000 | KMP | 30 | 297.36 ± 139.53<br>Mdn 269.64, IQR 185.75 | 0.632 ± 0.129<br>Mdn 0.607, IQR 0.156 | 296.73 ± 139.52<br>Mdn 269.08, IQR 185.91 | 5,052.0 ± 2,259.4<br>Mdn 4,600.0, IQR 2,953.8 | 261 ± 14<br>Mdn 256, IQR 24 | 261 ± 14<br>Mdn 256, IQR 24 | 321 ± 26<br>Mdn 318, IQR 27 |
| alphabet, |Σ|=full, n 1000–10000 | Aho-Corasick | 30 | 431.31 ± 198.68<br>Mdn 397.95, IQR 259.83 | 2.717 ± 0.484<br>Mdn 2.691, IQR 0.863 | 428.59 ± 198.71<br>Mdn 395.30, IQR 258.69 | 5,060.7 ± 2,259.4<br>Mdn 4,608.0, IQR 2,954.8 | 2,627 ± 499<br>Mdn 2,400, IQR 912 | 2,655 ± 513<br>Mdn 2,460, IQR 897 | 3,415 ± 513<br>Mdn 3,220, IQR 897 |
| positive_control, n 10–100 | Naive | 30 | 23.99 ± 0.71<br>Mdn 24.30, IQR 0.73 | 0.034 ± 0.002<br>Mdn 0.032, IQR 0.004 | 23.95 ± 0.71<br>Mdn 24.27, IQR 0.73 | 560.0 ± 0.0<br>Mdn 560.0, IQR 0.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| positive_control, n 10–100 | KMP | 30 | 8.35 ± 0.11<br>Mdn 8.39, IQR 0.14 | 0.891 ± 0.027<br>Mdn 0.889, IQR 0.043 | 7.46 ± 0.09<br>Mdn 7.49, IQR 0.10 | 160.0 ± 0.0<br>Mdn 160.0, IQR 0.0 | 264 ± 0<br>Mdn 264, IQR 0 | 264 ± 0<br>Mdn 264, IQR 0 | 312 ± 0<br>Mdn 312, IQR 0 |
| positive_control, n 10–100 | Aho-Corasick | 30 | 10.76 ± 0.23<br>Mdn 10.84, IQR 0.15 | 3.112 ± 0.088<br>Mdn 3.148, IQR 0.109 | 7.65 ± 0.15<br>Mdn 7.70, IQR 0.03 | 174.0 ± 0.0<br>Mdn 174.0, IQR 0.0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 3,592 ± 0<br>Mdn 3,592, IQR 0 |
| positive_control, n 100–1000 | Naive | 30 | 297.77 ± 7.65<br>Mdn 298.72, IQR 2.63 | 0.032 ± 0.004<br>Mdn 0.031, IQR 0.000 | 297.74 ± 7.65<br>Mdn 298.69, IQR 2.63 | 5,872.0 ± 0.0<br>Mdn 5,872.0, IQR 0.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| positive_control, n 100–1000 | KMP | 30 | 79.54 ± 2.03<br>Mdn 79.94, IQR 1.34 | 0.865 ± 0.023<br>Mdn 0.865, IQR 0.036 | 78.68 ± 2.03<br>Mdn 79.05, IQR 1.34 | 1,488.0 ± 0.0<br>Mdn 1,488.0, IQR 0.0 | 264 ± 0<br>Mdn 264, IQR 0 | 264 ± 0<br>Mdn 264, IQR 0 | 312 ± 0<br>Mdn 312, IQR 0 |
| positive_control, n 100–1000 | Aho-Corasick | 30 | 80.62 ± 2.20<br>Mdn 81.75, IQR 2.88 | 2.911 ± 0.069<br>Mdn 2.899, IQR 0.118 | 77.71 ± 2.18<br>Mdn 78.81, IQR 2.87 | 1,502.0 ± 0.0<br>Mdn 1,502.0, IQR 0.0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 2,832 ± 0<br>Mdn 2,832, IQR 0 | 3,592 ± 0<br>Mdn 3,592, IQR 0 |
| positive_control, n 1000–10000 | Naive | 30 | 913.17 ± 15.42<br>Mdn 916.56, IQR 18.16 | 0.033 ± 0.003<br>Mdn 0.034, IQR 0.006 | 913.14 ± 15.42<br>Mdn 916.53, IQR 18.16 | 16,490.0 ± 0.0<br>Mdn 16,490.0, IQR 0.0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 | 0 ± 0<br>Mdn 0, IQR 0 |
| positive_control, n 1000–10000 | KMP | 30 | 362.54 ± 7.15<br>Mdn 364.24, IQR 9.91 | 0.617 ± 0.076<br>Mdn 0.603, IQR 0.013 | 361.93 ± 7.17<br>Mdn 363.58, IQR 9.93 | 6,607.0 ± 0.0<br>Mdn 6,607.0, IQR 0.0 | 240 ± 0<br>Mdn 240, IQR 0 | 240 ± 0<br>Mdn 240, IQR 0 | 288 ± 0<br>Mdn 288, IQR 0 |
| positive_control, n 1000–10000 | Aho-Corasick | 30 | 355.08 ± 9.02<br>Mdn 358.05, IQR 11.68 | 2.094 ± 0.192<br>Mdn 2.004, IQR 0.050 | 352.98 ± 8.98<br>Mdn 356.04, IQR 11.65 | 6,615.0 ± 0.0<br>Mdn 6,615.0, IQR 0.0 | 1,920 ± 0<br>Mdn 1,920, IQR 0 | 1,920 ± 0<br>Mdn 1,920, IQR 0 | 2,680 ± 0<br>Mdn 2,680, IQR 0 |

*Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1).*
