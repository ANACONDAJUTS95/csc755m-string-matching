# Naive trace

| Item | Value |
| --- | --- |
| Text | `aaaaaaaaaa` |
| Text length n | 10 |
| Queries | 0: `aaab` |
| Preprocessing comparisons | 0 |
| Search comparisons | 28 |
| Matches (start, query) | none |
| Agrees with `src/` counted version | ✓ yes |

Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.

## Search

| Step | Query | Alignment i | Text index | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 0 | 0 | 0 | 0 | `a` vs `a` | ✓ | advance j |
| 2 | 0 | 0 | 1 | 1 | `a` vs `a` | ✓ | advance j |
| 3 | 0 | 0 | 2 | 2 | `a` vs `a` | ✓ | advance j |
| 4 | 0 | 0 | 3 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 1 |
| 5 | 0 | 1 | 1 | 0 | `a` vs `a` | ✓ | advance j |
| 6 | 0 | 1 | 2 | 1 | `a` vs `a` | ✓ | advance j |
| 7 | 0 | 1 | 3 | 2 | `a` vs `a` | ✓ | advance j |
| 8 | 0 | 1 | 4 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 2 |
| 9 | 0 | 2 | 2 | 0 | `a` vs `a` | ✓ | advance j |
| 10 | 0 | 2 | 3 | 1 | `a` vs `a` | ✓ | advance j |
| 11 | 0 | 2 | 4 | 2 | `a` vs `a` | ✓ | advance j |
| 12 | 0 | 2 | 5 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 3 |
| 13 | 0 | 3 | 3 | 0 | `a` vs `a` | ✓ | advance j |
| 14 | 0 | 3 | 4 | 1 | `a` vs `a` | ✓ | advance j |
| 15 | 0 | 3 | 5 | 2 | `a` vs `a` | ✓ | advance j |
| 16 | 0 | 3 | 6 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 4 |
| 17 | 0 | 4 | 4 | 0 | `a` vs `a` | ✓ | advance j |
| 18 | 0 | 4 | 5 | 1 | `a` vs `a` | ✓ | advance j |
| 19 | 0 | 4 | 6 | 2 | `a` vs `a` | ✓ | advance j |
| 20 | 0 | 4 | 7 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 5 |
| 21 | 0 | 5 | 5 | 0 | `a` vs `a` | ✓ | advance j |
| 22 | 0 | 5 | 6 | 1 | `a` vs `a` | ✓ | advance j |
| 23 | 0 | 5 | 7 | 2 | `a` vs `a` | ✓ | advance j |
| 24 | 0 | 5 | 8 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 6 |
| 25 | 0 | 6 | 6 | 0 | `a` vs `a` | ✓ | advance j |
| 26 | 0 | 6 | 7 | 1 | `a` vs `a` | ✓ | advance j |
| 27 | 0 | 6 | 8 | 2 | `a` vs `a` | ✓ | advance j |
| 28 | 0 | 6 | 9 | 3 | `a` vs `b` | ✗ | mismatch → shift pattern to i = 7 |

