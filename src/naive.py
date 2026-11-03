"""Naive (brute-force) exact string matching.

The idea: try every alignment i of the pattern against the text and compare
characters left to right until one differs or the whole pattern matches.
Worst case O(n * m) comparisons per pattern; no preprocessing at all.

Every module in src/ exposes the same interface so the benchmark can treat the
three algorithms identically:

    preprocess(queries)             -> state           (clean, timed)
    search(text, state)             -> matches         (clean, timed)
    preprocess_counted(queries)     -> (state, prep_comparisons)
    search_counted(text, state)     -> (matches, search_comparisons, failure_steps)

`matches` is always a sorted list of (start_index, query_index) tuples,
overlapping matches included. Queries must be non-empty strings.

The clean and counted versions contain the *same* loop logic; the counted one
only adds `comparisons += 1` in front of each character comparison. Keeping the
counters out of the clean version means the timing pass measures the algorithm,
not the bookkeeping.
"""

NAME = "naive"
HAS_PREPROCESSING = False  # memory is recorded as 0 for Naive


# ---------------------------------------------------------------------------
# Clean versions (used for timing)
# ---------------------------------------------------------------------------
def preprocess(queries):
    """Naive builds nothing. Return the queries so the interface matches the others."""
    return queries


def search(text, state):
    """Return every (start, query_index) where a query occurs in text."""
    queries = state
    matches = []
    n = len(text)
    for qi, pattern in enumerate(queries):
        m = len(pattern)
        for i in range(n - m + 1):  # every possible alignment
            j = 0
            while j < m:
                if text[i + j] != pattern[j]:
                    break  # mismatch: give up on this alignment
                j += 1
            if j == m:
                matches.append((i, qi))
    matches.sort()
    return matches


# ---------------------------------------------------------------------------
# Counted versions (used for counting comparisons; same logic as above)
# ---------------------------------------------------------------------------
def preprocess_counted(queries):
    """Naive has no preprocessing, so prep comparisons are 0 by definition."""
    return queries, 0


def search_counted(text, state):
    """Same as search(), but counts every text[i + j] == pattern[j] check."""
    queries = state
    matches = []
    comparisons = 0
    n = len(text)
    for qi, pattern in enumerate(queries):
        m = len(pattern)
        for i in range(n - m + 1):
            j = 0
            while j < m:
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1
            if j == m:
                matches.append((i, qi))
    matches.sort()
    return matches, comparisons, None  # Naive has no failure steps


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
