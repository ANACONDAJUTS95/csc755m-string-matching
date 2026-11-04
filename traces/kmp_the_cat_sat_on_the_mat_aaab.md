# KMP trace

| Item | Value |
| --- | --- |
| Text | `the␠cat␠sat␠on␠the␠mat` |
| Text length n | 22 |
| Queries | 0: `aaab` |
| Preprocessing comparisons | 5 |
| Search comparisons | 25 |
| Matches (start, query) | none |
| Agrees with `src/` counted version | ✓ yes |

Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.

## Query 0 `aaab`: building the LPS table (5 comparisons)

| Step | i | len | Compared p[i] vs p[len] | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 1 | 0 | `a` vs `a` | ✓ | lps[1] = 1; advance i |
| 2 | 2 | 1 | `a` vs `a` | ✓ | lps[2] = 2; advance i |
| 3 | 3 | 2 | `b` vs `a` | ✗ | fall back: len = LPS[1] = 1 (i stays) |
| 4 | 3 | 1 | `b` vs `a` | ✗ | fall back: len = LPS[0] = 0 (i stays) |
| 5 | 3 | 0 | `b` vs `a` | ✗ | lps[3] = 0; advance i |

Resulting LPS table:

| Index | 0 | 1 | 2 | 3 |
| --- | :---: | :---: | :---: | :---: |
| Character | `a` | `a` | `a` | `b` |
| LPS | 0 | 1 | 2 | 0 |


## Query 0 `aaab`: search (25 comparisons)

| Step | Text index i | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 0 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 2 | 1 | 0 | `h` vs `a` | ✗ | shift: i → i + 1 |
| 3 | 2 | 0 | `e` vs `a` | ✗ | shift: i → i + 1 |
| 4 | 3 | 0 | `␠` vs `a` | ✗ | shift: i → i + 1 |
| 5 | 4 | 0 | `c` vs `a` | ✗ | shift: i → i + 1 |
| 6 | 5 | 0 | `a` vs `a` | ✓ | advance i and j |
| 7 | 6 | 1 | `t` vs `a` | ✗ | fall back via LPS[0] = 0 (re-check text[6]) |
| 8 | 6 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 9 | 7 | 0 | `␠` vs `a` | ✗ | shift: i → i + 1 |
| 10 | 8 | 0 | `s` vs `a` | ✗ | shift: i → i + 1 |
| 11 | 9 | 0 | `a` vs `a` | ✓ | advance i and j |
| 12 | 10 | 1 | `t` vs `a` | ✗ | fall back via LPS[0] = 0 (re-check text[10]) |
| 13 | 10 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 14 | 11 | 0 | `␠` vs `a` | ✗ | shift: i → i + 1 |
| 15 | 12 | 0 | `o` vs `a` | ✗ | shift: i → i + 1 |
| 16 | 13 | 0 | `n` vs `a` | ✗ | shift: i → i + 1 |
| 17 | 14 | 0 | `␠` vs `a` | ✗ | shift: i → i + 1 |
| 18 | 15 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 19 | 16 | 0 | `h` vs `a` | ✗ | shift: i → i + 1 |
| 20 | 17 | 0 | `e` vs `a` | ✗ | shift: i → i + 1 |
| 21 | 18 | 0 | `␠` vs `a` | ✗ | shift: i → i + 1 |
| 22 | 19 | 0 | `m` vs `a` | ✗ | shift: i → i + 1 |
| 23 | 20 | 0 | `a` vs `a` | ✓ | advance i and j |
| 24 | 21 | 1 | `t` vs `a` | ✗ | fall back via LPS[0] = 0 (re-check text[21]) |
| 25 | 21 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |

