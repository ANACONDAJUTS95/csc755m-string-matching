# Naive trace

| Item | Value |
| --- | --- |
| Text | `hello␠world` |
| Text length n | 11 |
| Queries | 0: `wor` |
| Preprocessing comparisons | 0 |
| Search comparisons | 11 |
| Matches (start, query) | (6, 0) |
| Agrees with `src/` counted version | ✓ yes |

Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.

## Search

| Step | Query | Alignment i | Text index | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 0 | 0 | 0 | 0 | `h` vs `w` | ✗ | mismatch → shift pattern to i = 1 |
| 2 | 0 | 1 | 1 | 0 | `e` vs `w` | ✗ | mismatch → shift pattern to i = 2 |
| 3 | 0 | 2 | 2 | 0 | `l` vs `w` | ✗ | mismatch → shift pattern to i = 3 |
| 4 | 0 | 3 | 3 | 0 | `l` vs `w` | ✗ | mismatch → shift pattern to i = 4 |
| 5 | 0 | 4 | 4 | 0 | `o` vs `w` | ✗ | mismatch → shift pattern to i = 5 |
| 6 | 0 | 5 | 5 | 0 | `␠` vs `w` | ✗ | mismatch → shift pattern to i = 6 |
| 7 | 0 | 6 | 6 | 0 | `w` vs `w` | ✓ | advance j |
| 8 | 0 | 6 | 7 | 1 | `o` vs `o` | ✓ | advance j |
| 9 | 0 | 6 | 8 | 2 | `r` vs `r` | ✓ | **report match at 6** → shift pattern to i = 7 |
| 10 | 0 | 7 | 7 | 0 | `o` vs `w` | ✗ | mismatch → shift pattern to i = 8 |
| 11 | 0 | 8 | 8 | 0 | `r` vs `w` | ✗ | mismatch → shift pattern to i = 9 |

