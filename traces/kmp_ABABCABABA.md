# KMP trace

| Item | Value |
| --- | --- |
| Text | `ABABCABABA` |
| Text length n | 10 |
| Queries | 0: `ABABA` |
| Preprocessing comparisons | 4 |
| Search comparisons | 12 |
| Matches (start, query) | (5, 0) |
| Agrees with `src/` counted version | ✓ yes |

Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.

## Query 0 `ABABA`: building the LPS table (4 comparisons)

| Step | i | len | Compared p[i] vs p[len] | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 1 | 0 | `B` vs `A` | ✗ | lps[1] = 0; advance i |
| 2 | 2 | 0 | `A` vs `A` | ✓ | lps[2] = 1; advance i |
| 3 | 3 | 1 | `B` vs `B` | ✓ | lps[3] = 2; advance i |
| 4 | 4 | 2 | `A` vs `A` | ✓ | lps[4] = 3; advance i |

Resulting LPS table:

| Index | 0 | 1 | 2 | 3 | 4 |
| --- | :---: | :---: | :---: | :---: | :---: |
| Character | `A` | `B` | `A` | `B` | `A` |
| LPS | 0 | 0 | 1 | 2 | 3 |


## Query 0 `ABABA`: search (12 comparisons)

| Step | Text index i | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 1 | 0 | 0 | `A` vs `A` | ✓ | advance i and j |
| 2 | 1 | 1 | `B` vs `B` | ✓ | advance i and j |
| 3 | 2 | 2 | `A` vs `A` | ✓ | advance i and j |
| 4 | 3 | 3 | `B` vs `B` | ✓ | advance i and j |
| 5 | 4 | 4 | `C` vs `A` | ✗ | fall back via LPS[3] = 2 (re-check text[4]) |
| 6 | 4 | 2 | `C` vs `A` | ✗ | fall back via LPS[1] = 0 (re-check text[4]) |
| 7 | 4 | 0 | `C` vs `A` | ✗ | shift: i → i + 1 |
| 8 | 5 | 0 | `A` vs `A` | ✓ | advance i and j |
| 9 | 6 | 1 | `B` vs `B` | ✓ | advance i and j |
| 10 | 7 | 2 | `A` vs `A` | ✓ | advance i and j |
| 11 | 8 | 3 | `B` vs `B` | ✓ | advance i and j |
| 12 | 9 | 4 | `A` vs `A` | ✓ | **report match at 5**; fall back via LPS[4] = 3; advance i |

