# KMP trace

| Item | Value |
| --- | --- |
| Text | `aaaaaaaaaa` |
| Text length n | 10 |
| Queries | 0: `aaab` |
| Preprocessing comparisons | 5 |
| Search comparisons | 17 |
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


## Query 0 `aaab`: search (17 comparisons)

| Step | Text index i | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 0 | 0 | `a` vs `a` | ✓ | advance i and j |
| 2 | 1 | 1 | `a` vs `a` | ✓ | advance i and j |
| 3 | 2 | 2 | `a` vs `a` | ✓ | advance i and j |
| 4 | 3 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[3]) |
| 5 | 3 | 2 | `a` vs `a` | ✓ | advance i and j |
| 6 | 4 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[4]) |
| 7 | 4 | 2 | `a` vs `a` | ✓ | advance i and j |
| 8 | 5 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[5]) |
| 9 | 5 | 2 | `a` vs `a` | ✓ | advance i and j |
| 10 | 6 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[6]) |
| 11 | 6 | 2 | `a` vs `a` | ✓ | advance i and j |
| 12 | 7 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[7]) |
| 13 | 7 | 2 | `a` vs `a` | ✓ | advance i and j |
| 14 | 8 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[8]) |
| 15 | 8 | 2 | `a` vs `a` | ✓ | advance i and j |
| 16 | 9 | 3 | `a` vs `b` | ✗ | fall back via LPS[2] = 2 (re-check text[9]) |
| 17 | 9 | 2 | `a` vs `a` | ✓ | advance i and j |

