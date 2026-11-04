# Replication report

Generated 2026-11-04 09:36:09 UTC by `replicate.py`.

## 1. Inputs and row counts

| Check | Primary | Replication | Result |
| --- | --- | --- | --- |
| Input hash used | `578618582b5aff0ab3cbf18e11be7bbb8bea207c1f1a9b41bf0129ba0ba67cb6` | `578618582b5aff0ab3cbf18e11be7bbb8bea207c1f1a9b41bf0129ba0ba67cb6` | ✅ match |
| Row count | 5,130 | 5,130 | ✅ expected 5,130 |
| Same set of (input_id, algorithm) jobs |  |  | ✅ yes |
| Python | 3.12.13 | 3.12.13 | ✅ same |
| OS | Windows 11 (Core, build 10.0.26300) | CachyOS (kernel 7.3.1-1-cachyos) |  |
| CPU | AMD Ryzen AI 9 HX 370 w/ Radeon 890M | Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz |  |

Manifest hash: `578618582b5aff0ab3cbf18e11be7bbb8bea207c1f1a9b41bf0129ba0ba67cb6`

## 2. Comparison and match counts per (input_id, algorithm)

Columns compared: `prep_comparisons`, `search_comparisons`, `search_failure_steps`, `num_matches` over 5,130 jobs.

**✅ All identical.**

For information: `memory_bytes` differs in 0 of 5,130 jobs (expected 0 with the same Python version, since object sizes are deterministic).

## 3. Winners per condition (Table 5.8)

Winner = the fastest algorithm by median total time in that condition group. Same winner on both machines in **52 of 57** condition groups.

| Condition | Winner (primary) | Winner (replication) | Same direction? | Comparisons identical? |
| --- | --- | --- | :---: | :---: |
| core, random, q 1–5, k=1, n 10–100 | KMP | Naive | ❌ no | ✅ yes |
| core, random, q 1–5, k=5, n 10–100 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, random, q 5–10, k=1, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| core, random, q 5–10, k=5, n 10–100 | Aho-Corasick | Naive | ❌ no | ✅ yes |
| core, random, q 10–20, k=1, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| core, random, q 10–20, k=5, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| core, random, q 1–5, k=1, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| core, random, q 1–5, k=5, n 100–1000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, random, q 5–10, k=1, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| core, random, q 5–10, k=5, n 100–1000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, random, q 10–20, k=1, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| core, random, q 10–20, k=5, n 100–1000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, random, q 1–5, k=1, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| core, random, q 1–5, k=5, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, random, q 5–10, k=1, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| core, random, q 5–10, k=5, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, random, q 10–20, k=1, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| core, random, q 10–20, k=5, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 1–5, k=1, n 10–100 | KMP | Naive | ❌ no | ✅ yes |
| core, narrative, q 1–5, k=5, n 10–100 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 5–10, k=1, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| core, narrative, q 5–10, k=5, n 10–100 | Aho-Corasick | Naive | ❌ no | ✅ yes |
| core, narrative, q 10–20, k=1, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| core, narrative, q 10–20, k=5, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| core, narrative, q 1–5, k=1, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| core, narrative, q 1–5, k=5, n 100–1000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 5–10, k=1, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| core, narrative, q 5–10, k=5, n 100–1000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 10–20, k=1, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| core, narrative, q 10–20, k=5, n 100–1000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 1–5, k=1, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| core, narrative, q 1–5, k=5, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 5–10, k=1, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| core, narrative, q 5–10, k=5, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| core, narrative, q 10–20, k=1, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| core, narrative, q 10–20, k=5, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |
| query_pattern, distinct, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| query_pattern, repeating, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| query_pattern, distinct, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| query_pattern, repeating, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| query_pattern, distinct, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| query_pattern, repeating, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=2, n 10–100 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=2, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=2, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=4, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| alphabet, |Σ|=4, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=4, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=26, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| alphabet, |Σ|=26, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=26, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=full, n 10–100 | Naive | Naive | ✅ yes | ✅ yes |
| alphabet, |Σ|=full, n 100–1000 | KMP | KMP | ✅ yes | ✅ yes |
| alphabet, |Σ|=full, n 1000–10000 | KMP | KMP | ✅ yes | ✅ yes |
| positive_control, n 10–100 | KMP | KMP | ✅ yes | ✅ yes |
| positive_control, n 100–1000 | Aho-Corasick | KMP | ❌ no | ✅ yes |
| positive_control, n 1000–10000 | Aho-Corasick | Aho-Corasick | ✅ yes | ✅ yes |

## 4. Ratio of median total times (replication ÷ primary)

Above 1 means the replication machine was slower.

| Algorithm | Median ratio over condition groups | Min | Max |
| --- | ---: | ---: | ---: |
| Naive | 1.36 | 1.22 | 1.45 |
| KMP | 1.44 | 1.32 | 1.55 |
| Aho-Corasick | 1.51 | 1.42 | 1.64 |

| Condition | Naive | KMP | Aho-Corasick |
| --- | ---: | ---: | ---: |
| core, random, q 1–5, k=1, n 10–100 | 1.27 | 1.42 | 1.51 |
| core, random, q 1–5, k=5, n 10–100 | 1.33 | 1.44 | 1.46 |
| core, random, q 5–10, k=1, n 10–100 | 1.32 | 1.41 | 1.50 |
| core, random, q 5–10, k=5, n 10–100 | 1.30 | 1.42 | 1.45 |
| core, random, q 10–20, k=1, n 10–100 | 1.35 | 1.44 | 1.49 |
| core, random, q 10–20, k=5, n 10–100 | 1.31 | 1.34 | 1.50 |
| core, random, q 1–5, k=1, n 100–1000 | 1.33 | 1.41 | 1.54 |
| core, random, q 1–5, k=5, n 100–1000 | 1.42 | 1.46 | 1.46 |
| core, random, q 5–10, k=1, n 100–1000 | 1.37 | 1.42 | 1.49 |
| core, random, q 5–10, k=5, n 100–1000 | 1.38 | 1.47 | 1.46 |
| core, random, q 10–20, k=1, n 100–1000 | 1.31 | 1.46 | 1.51 |
| core, random, q 10–20, k=5, n 100–1000 | 1.39 | 1.48 | 1.46 |
| core, random, q 1–5, k=1, n 1000–10000 | 1.40 | 1.52 | 1.58 |
| core, random, q 1–5, k=5, n 1000–10000 | 1.43 | 1.55 | 1.50 |
| core, random, q 5–10, k=1, n 1000–10000 | 1.37 | 1.49 | 1.54 |
| core, random, q 5–10, k=5, n 1000–10000 | 1.43 | 1.52 | 1.51 |
| core, random, q 10–20, k=1, n 1000–10000 | 1.44 | 1.52 | 1.61 |
| core, random, q 10–20, k=5, n 1000–10000 | 1.44 | 1.50 | 1.51 |
| core, narrative, q 1–5, k=1, n 10–100 | 1.22 | 1.44 | 1.49 |
| core, narrative, q 1–5, k=5, n 10–100 | 1.34 | 1.37 | 1.52 |
| core, narrative, q 5–10, k=1, n 10–100 | 1.24 | 1.35 | 1.51 |
| core, narrative, q 5–10, k=5, n 10–100 | 1.28 | 1.41 | 1.47 |
| core, narrative, q 10–20, k=1, n 10–100 | 1.27 | 1.44 | 1.53 |
| core, narrative, q 10–20, k=5, n 10–100 | 1.32 | 1.39 | 1.52 |
| core, narrative, q 1–5, k=1, n 100–1000 | 1.40 | 1.47 | 1.54 |
| core, narrative, q 1–5, k=5, n 100–1000 | 1.37 | 1.49 | 1.44 |
| core, narrative, q 5–10, k=1, n 100–1000 | 1.32 | 1.43 | 1.50 |
| core, narrative, q 5–10, k=5, n 100–1000 | 1.38 | 1.46 | 1.42 |
| core, narrative, q 10–20, k=1, n 100–1000 | 1.37 | 1.40 | 1.54 |
| core, narrative, q 10–20, k=5, n 100–1000 | 1.34 | 1.43 | 1.51 |
| core, narrative, q 1–5, k=1, n 1000–10000 | 1.45 | 1.48 | 1.58 |
| core, narrative, q 1–5, k=5, n 1000–10000 | 1.37 | 1.53 | 1.54 |
| core, narrative, q 5–10, k=1, n 1000–10000 | 1.40 | 1.48 | 1.64 |
| core, narrative, q 5–10, k=5, n 1000–10000 | 1.44 | 1.42 | 1.44 |
| core, narrative, q 10–20, k=1, n 1000–10000 | 1.44 | 1.49 | 1.58 |
| core, narrative, q 10–20, k=5, n 1000–10000 | 1.44 | 1.52 | 1.50 |
| query_pattern, distinct, n 10–100 | 1.26 | 1.43 | 1.51 |
| query_pattern, repeating, n 10–100 | 1.23 | 1.47 | 1.53 |
| query_pattern, distinct, n 100–1000 | 1.35 | 1.49 | 1.54 |
| query_pattern, repeating, n 100–1000 | 1.34 | 1.41 | 1.54 |
| query_pattern, distinct, n 1000–10000 | 1.39 | 1.52 | 1.55 |
| query_pattern, repeating, n 1000–10000 | 1.45 | 1.55 | 1.60 |
| alphabet, |Σ|=2, n 10–100 | 1.29 | 1.32 | 1.47 |
| alphabet, |Σ|=2, n 100–1000 | 1.31 | 1.43 | 1.43 |
| alphabet, |Σ|=2, n 1000–10000 | 1.38 | 1.38 | 1.51 |
| alphabet, |Σ|=4, n 10–100 | 1.27 | 1.40 | 1.49 |
| alphabet, |Σ|=4, n 100–1000 | 1.32 | 1.39 | 1.50 |
| alphabet, |Σ|=4, n 1000–10000 | 1.38 | 1.45 | 1.59 |
| alphabet, |Σ|=26, n 10–100 | 1.28 | 1.39 | 1.48 |
| alphabet, |Σ|=26, n 100–1000 | 1.36 | 1.44 | 1.59 |
| alphabet, |Σ|=26, n 1000–10000 | 1.42 | 1.39 | 1.54 |
| alphabet, |Σ|=full, n 10–100 | 1.33 | 1.41 | 1.55 |
| alphabet, |Σ|=full, n 100–1000 | 1.36 | 1.45 | 1.55 |
| alphabet, |Σ|=full, n 1000–10000 | 1.34 | 1.48 | 1.60 |
| positive_control, n 10–100 | 1.38 | 1.36 | 1.48 |
| positive_control, n 100–1000 | 1.43 | 1.42 | 1.49 |
| positive_control, n 1000–10000 | 1.41 | 1.44 | 1.50 |
