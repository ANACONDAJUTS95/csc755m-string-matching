# Aho-Corasick trace

| Item | Value |
| --- | --- |
| Text | `ushers` |
| Text length n | 6 |
| Queries | 0: `he`<br>1: `she`<br>2: `his`<br>3: `hers` |
| Preprocessing comparisons | 19 |
| Search comparisons | 7 |
| Matches (start, query) | (1, 1), (2, 0), (2, 3) |
| Agrees with `src/` counted version | ✓ yes |

Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.

## Automaton (10 states, 19 preprocessing comparisons)

| State (path) | Goto (children) | Failure link | Output |
| --- | --- | --- | --- |
| 0 (root) | `h`→1, `s`→3 | — | — |
| 1 (`h`) | `e`→2, `i`→6 | 0 (root) | — |
| 2 (`he`) | `r`→8 | 0 (root) | `he` |
| 3 (`s`) | `h`→4 | 0 (root) | — |
| 4 (`sh`) | `e`→5 | 1 (`h`) | — |
| 5 (`she`) | — | 2 (`he`) | `she`, `he` |
| 6 (`hi`) | `s`→7 | 0 (root) | — |
| 7 (`his`) | — | 3 (`s`) | `his` |
| 8 (`her`) | `s`→9 | 0 (root) | — |
| 9 (`hers`) | — | 3 (`s`) | `hers` |


## Search (7 attempted transitions, 1 failure-link steps)

| Step | Text index | Character | Current state | Transition tried | Result | Failure link followed | Outputs reported |
| ---: | ---: | :---: | --- | --- | --- | --- | --- |
| 1 | 0 | `u` | 0 (root) | goto(0, `u`) | fail → stay at root | — | — |
| 2 | 1 | `s` | 0 (root) | goto(0, `s`) | → 3 (`s`) | — | — |
| 3 | 2 | `h` | 3 (`s`) | goto(3, `h`) | → 4 (`sh`) | — | — |
| 4 | 3 | `e` | 4 (`sh`) | goto(4, `e`) | → 5 (`she`) | — | **`she` at 1**, **`he` at 2** |
| 5 | 4 | `r` | 5 (`she`) | goto(5, `r`) | fail | 5 → 2 (`he`) | — |
| 6 | 4 | `r` | 2 (`he`) | goto(2, `r`) | → 8 (`her`) | — | — |
| 7 | 5 | `s` | 8 (`her`) | goto(8, `s`) | → 9 (`hers`) | — | **`hers` at 2** |

