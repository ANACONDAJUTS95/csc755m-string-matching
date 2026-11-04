# Trace summary: Case 1 (positive control) and Case 2 (repeating vs. distinct query)

Comparison counts follow the definitions in `README.md` ("Comparison-counting definitions"):

- **Naive:** prep = 0. Every check `text[i + j] == pattern[j]` counts 1.
- **KMP:** prep is every character comparison made while building the LPS table. Search is every check
  `text[i] == pattern[j]`, including the re-checks after a fallback via the LPS table.
- **Total** = prep + search. **Comparisons per text character** = total ÷ n, the same quantity `analyze.py`
  uses.

**Verification.** I also ran each case through `find_all_counted` in `src/naive.py` or `src/kmp.py` on the
same inputs. For all six traces, the prep comparisons, search comparisons and matches equal the counted
versions (trace.py's built-in self-check also passed on every run).

## 1. All traces

| Case | Algorithm | Text | Query | n | m | Alignments (n − m + 1) | Prep comparisons | Search comparisons | Total | Comparisons per text character | Matches found |
| :---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 1 | Naive | `aaaaaaaaaa` | `aaab` | 10 | 4 | 7 | 0 | 28 | 28 | 2.800 | 0 |
| 1 | KMP | `aaaaaaaaaa` | `aaab` | 10 | 4 | 7 | 5 | 17 | 22 | 2.200 | 0 |
| 2 | Naive | `the cat sat on the mat` | `abab` | 22 | 4 | 19 | 0 | 21 | 21 | 0.955 | 0 |
| 2 | Naive | `the cat sat on the mat` | `abcd` | 22 | 4 | 19 | 0 | 21 | 21 | 0.955 | 0 |
| 2 | KMP | `the cat sat on the mat` | `abab` | 22 | 4 | 19 | 3 | 25 | 28 | 1.273 | 0 |
| 2 | KMP | `the cat sat on the mat` | `abcd` | 22 | 4 | 19 | 3 | 25 | 28 | 1.273 | 0 |

Trace files: `case1_naive.md`, `case1_kmp.md`, `case2_naive_abab.md`, `case2_naive_abcd.md`,
`case2_kmp_abab.md`, `case2_kmp_abcd.md`.

LPS tables:

| Query | LPS | Prep comparisons |
| --- | --- | ---: |
| `aaab` | [0, 1, 2, 0] | 5 |
| `abab` | [0, 0, 1, 2] | 3 |
| `abcd` | [0, 0, 0, 0] | 3 |

## 2. Case 1 checks (text `aaaaaaaaaa`, n = 10; query `aaab`, m = 4)

| Check | Expected | Observed | Holds? |
| --- | --- | --- | :---: |
| Naive search = (n − m + 1) · m | (10 − 4 + 1) · 4 = 7 · 4 = **28** | 28 | ✓ |
| KMP search ≤ 2n | ≤ 2 · 10 = **20** | 17 | ✓ |

Naive reaches the worst case exactly. In every one of the 7 alignments, `aaa` matches and the 4th comparison
(`a` vs `b`) fails. KMP compares each of the 10 text characters once (10 comparisons). It also re-checks
`text[3]` … `text[9]` once each after a fallback via LPS[2] = 2 (7 comparisons), for 17 in total. Even with its
5 LPS-building comparisons, KMP's total (22) is below Naive's (28).

## 3. Case 2: how far Naive gets in each alignment (text `the cat sat on the mat`, n = 22)

| Query | Alignments | Failed on 1st character | Reached 2nd character | Reached 3rd character | Longest partial match | Search comparisons |
| --- | ---: | ---: | ---: | ---: | :---: | ---: |
| `abab` | 19 | 17 | 2 (at i = 5, 9) | 0 | 1 character (`a`) | 17 · 1 + 2 · 2 = 21 |
| `abcd` | 19 | 17 | 2 (at i = 5, 9) | 0 | 1 character (`a`) | 17 · 1 + 2 · 2 = 21 |

Only the `a` in "c**a**t" (i = 5) and "s**a**t" (i = 9) start an alignment that gets past the first character,
and both fail at once on `t` vs `b`. The `a` in "m**a**t" (index 20) lies past the last alignment (i = 18).
Both queries start with `ab`, and the text never contains `ab`. So the repeating structure of `abab` is never
reached, and the two queries give identical Naive counts.

## 4. KMP trace excerpts (fallbacks via the LPS table)

### Case 1: KMP, text `aaaaaaaaaa`, query `aaab` (LPS = [0, 1, 2, 0]); steps 1–12 of 17

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

After the first mismatch, LPS[2] = 2 keeps the already-matched `aa`. KMP resumes at j = 2 and never moves i
backwards. Steps 13–17 repeat the same two-row pattern up to text[9].

### Case 2: KMP, text `the cat sat on the mat`, query `abab` (LPS = [0, 0, 1, 2]); steps 6–8, 11–13, 23–25 of 25

| Step | Text index i | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 6 | 5 | 0 | `a` vs `a` | ✓ | advance i and j |
| 7 | 6 | 1 | `t` vs `b` | ✗ | fall back via LPS[0] = 0 (re-check text[6]) |
| 8 | 6 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 11 | 9 | 0 | `a` vs `a` | ✓ | advance i and j |
| 12 | 10 | 1 | `t` vs `b` | ✗ | fall back via LPS[0] = 0 (re-check text[10]) |
| 13 | 10 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 23 | 20 | 0 | `a` vs `a` | ✓ | advance i and j |
| 24 | 21 | 1 | `t` vs `b` | ✗ | fall back via LPS[0] = 0 (re-check text[21]) |
| 25 | 21 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |

The omitted steps are first-character mismatches (`shift: i → i + 1`). Every fallback goes through LPS[0] = 0,
so the repeated `ab` in `abab` (LPS[3] = 2) is never used. Each re-check (steps 8, 13, 25) is a comparison that
Naive does not make, which is why KMP's search count (25) is higher than Naive's (21).

### Case 2: KMP, text `the cat sat on the mat`, query `abcd` (LPS = [0, 0, 0, 0]); steps 6–8, 11–13, 23–25 of 25

| Step | Text index i | Pattern index j | Compared | Match? | Action |
| ---: | ---: | ---: | :---: | :---: | --- |
| 6 | 5 | 0 | `a` vs `a` | ✓ | advance i and j |
| 7 | 6 | 1 | `t` vs `b` | ✗ | fall back via LPS[0] = 0 (re-check text[6]) |
| 8 | 6 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 11 | 9 | 0 | `a` vs `a` | ✓ | advance i and j |
| 12 | 10 | 1 | `t` vs `b` | ✗ | fall back via LPS[0] = 0 (re-check text[10]) |
| 13 | 10 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |
| 23 | 20 | 0 | `a` vs `a` | ✓ | advance i and j |
| 24 | 21 | 1 | `t` vs `b` | ✗ | fall back via LPS[0] = 0 (re-check text[21]) |
| 25 | 21 | 0 | `t` vs `a` | ✗ | shift: i → i + 1 |

This excerpt matches the `abab` excerpt row for row. On this text, the queries differ only in their LPS
tables, and only LPS[0] (0 for both) is ever used. So the repeating vs. distinct distinction has no effect on
KMP's search here. It also has no effect on prep: both tables take 3 comparisons to build.
