# Naive trace

| Item | Value |
| --- | --- |
| Text | `the␠cat␠sat␠on␠the␠mat` |
| Text length n | 22 |
| Queries | 0: `abab` |
| Preprocessing comparisons | 0 |
| Search comparisons | 21 |
| Matches (start, query) | none |
| Agrees with `src/` counted version | ✓ yes |

Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.

## Search

| Step | Query | Alignment i | Text index | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 0 | 0 | 0 | 0 | `t` vs `a` | ✗ | mismatch → shift pattern to i = 1 |
| 2 | 0 | 1 | 1 | 0 | `h` vs `a` | ✗ | mismatch → shift pattern to i = 2 |
| 3 | 0 | 2 | 2 | 0 | `e` vs `a` | ✗ | mismatch → shift pattern to i = 3 |
| 4 | 0 | 3 | 3 | 0 | `␠` vs `a` | ✗ | mismatch → shift pattern to i = 4 |
| 5 | 0 | 4 | 4 | 0 | `c` vs `a` | ✗ | mismatch → shift pattern to i = 5 |
| 6 | 0 | 5 | 5 | 0 | `a` vs `a` | ✓ | advance j |
| 7 | 0 | 5 | 6 | 1 | `t` vs `b` | ✗ | mismatch → shift pattern to i = 6 |
| 8 | 0 | 6 | 6 | 0 | `t` vs `a` | ✗ | mismatch → shift pattern to i = 7 |
| 9 | 0 | 7 | 7 | 0 | `␠` vs `a` | ✗ | mismatch → shift pattern to i = 8 |
| 10 | 0 | 8 | 8 | 0 | `s` vs `a` | ✗ | mismatch → shift pattern to i = 9 |
| 11 | 0 | 9 | 9 | 0 | `a` vs `a` | ✓ | advance j |
| 12 | 0 | 9 | 10 | 1 | `t` vs `b` | ✗ | mismatch → shift pattern to i = 10 |
| 13 | 0 | 10 | 10 | 0 | `t` vs `a` | ✗ | mismatch → shift pattern to i = 11 |
| 14 | 0 | 11 | 11 | 0 | `␠` vs `a` | ✗ | mismatch → shift pattern to i = 12 |
| 15 | 0 | 12 | 12 | 0 | `o` vs `a` | ✗ | mismatch → shift pattern to i = 13 |
| 16 | 0 | 13 | 13 | 0 | `n` vs `a` | ✗ | mismatch → shift pattern to i = 14 |
| 17 | 0 | 14 | 14 | 0 | `␠` vs `a` | ✗ | mismatch → shift pattern to i = 15 |
| 18 | 0 | 15 | 15 | 0 | `t` vs `a` | ✗ | mismatch → shift pattern to i = 16 |
| 19 | 0 | 16 | 16 | 0 | `h` vs `a` | ✗ | mismatch → shift pattern to i = 17 |
| 20 | 0 | 17 | 17 | 0 | `e` vs `a` | ✗ | mismatch → shift pattern to i = 18 |
| 21 | 0 | 18 | 18 | 0 | `␠` vs `a` | ✗ | mismatch → shift pattern to i = 19 |

