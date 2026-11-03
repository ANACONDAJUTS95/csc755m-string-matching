"""Knuth-Morris-Pratt (KMP) exact string matching.

The idea: when a mismatch happens after j matched characters, we already know
what those j text characters were (they equal pattern[0:j]). The LPS table
("longest proper prefix that is also a suffix") tells us how much of the
pattern is still lined up, so the text index never moves backwards.
Search is O(n) per pattern (at most 2n comparisons); preprocessing is O(m).

With several queries, KMP builds one LPS table per query and searches the
text once per query; times and comparisons are therefore sums over queries.

See naive.py for the shared module interface.
"""

NAME = "kmp"
HAS_PREPROCESSING = True


# ---------------------------------------------------------------------------
# Clean versions (used for timing)
# ---------------------------------------------------------------------------
def build_lps(pattern):
    """lps[i] = length of the longest proper prefix of pattern[:i+1] that is also its suffix."""
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the current matched prefix
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]  # fall back to a shorter border; do not advance i
        else:
            lps[i] = 0
            i += 1
    return lps


def preprocess(queries):
    """Build every LPS table. The state keeps the original queries list (no copy)."""
    return queries, [build_lps(pattern) for pattern in queries]


def search(text, state):
    """Return every (start, query_index) where a query occurs in text."""
    queries, tables = state
    matches = []
    n = len(text)
    for qi in range(len(queries)):
        pattern = queries[qi]
        lps = tables[qi]
        m = len(pattern)
        i = 0  # text index (never moves backwards)
        j = 0  # pattern index
        while i < n:
            if text[i] == pattern[j]:
                i += 1
                j += 1
                if j == m:
                    matches.append((i - m, qi))
                    j = lps[j - 1]  # keep going to find overlapping matches
            elif j != 0:
                j = lps[j - 1]  # fall back via the LPS table, re-check the same text[i]
            else:
                i += 1
    matches.sort()
    return matches


# ---------------------------------------------------------------------------
# Counted versions (same logic, plus counters)
# ---------------------------------------------------------------------------
def build_lps_counted(pattern):
    """Same as build_lps(), but counts every pattern[i] == pattern[length] check."""
    m = len(pattern)
    lps = [0] * m
    comparisons = 0
    length = 0
    i = 1
    while i < m:
        comparisons += 1
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps, comparisons


def preprocess_counted(queries):
    tables = []
    comparisons = 0
    for pattern in queries:
        lps, c = build_lps_counted(pattern)
        tables.append(lps)
        comparisons += c
    return (queries, tables), comparisons


def search_counted(text, state):
    """Same as search(), but counts every text[i] == pattern[j] check (re-checks included)."""
    queries, tables = state
    matches = []
    comparisons = 0
    n = len(text)
    for qi in range(len(queries)):
        pattern = queries[qi]
        lps = tables[qi]
        m = len(pattern)
        i = 0
        j = 0
        while i < n:
            comparisons += 1
            if text[i] == pattern[j]:
                i += 1
                j += 1
                if j == m:
                    matches.append((i - m, qi))
                    j = lps[j - 1]
            elif j != 0:
                j = lps[j - 1]
            else:
                i += 1
    matches.sort()
    return matches, comparisons, None  # KMP has no failure-link steps


# ---------------------------------------------------------------------------
# Convenience wrappers (tests, trace.py)
# ---------------------------------------------------------------------------
def find_all(text, queries):
    return search(text, preprocess(queries))


def find_all_counted(text, queries):
    state, prep = preprocess_counted(queries)
    matches, search_comparisons, failure_steps = search_counted(text, state)
    return {
        "matches": matches,
        "prep_comparisons": prep,
        "search_comparisons": search_comparisons,
        "search_failure_steps": failure_steps,
    }
