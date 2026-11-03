"""Aho-Corasick multi-pattern exact string matching (Aho & Corasick, 1975).

The idea: put all queries into one trie (the "goto" function), then give every
node a failure link to the node for its longest proper suffix that is also in
the trie. Scanning the text once, we follow goto edges when we can and failure
links when we cannot, so every query is found in a single pass.

Representation (parallel lists indexed by node number, root = 0):
    goto[node]    dict: character -> child node
    fail[node]    int:  failure link
    out[node]     list: query indices that end at this node (own + inherited
                  through the failure link, as in the 1975 paper)
    lengths[qi]   length of query qi, to turn an end position into a start

Failure links are built breadth-first, so a node's failure target (which is
always shallower) is finished before the node itself.

See naive.py for the shared module interface.
"""

from collections import deque

NAME = "aho_corasick"
HAS_PREPROCESSING = True


# ---------------------------------------------------------------------------
# Clean versions (used for timing)
# ---------------------------------------------------------------------------
def preprocess(queries):
    """Build one automaton for all queries."""
    goto = [{}]
    fail = [0]
    out = [[]]

    # 1. Insert every keyword into the trie.
    for qi, word in enumerate(queries):
        node = 0
        for ch in word:
            nxt = goto[node].get(ch)
            if nxt is None:
                nxt = len(goto)
                goto.append({})
                fail.append(0)
                out.append([])
                goto[node][ch] = nxt
            node = nxt
        out[node].append(qi)

    # 2. Failure links, breadth-first. Depth-1 nodes fail to the root (already 0).
    queue = deque(goto[0].values())
    while queue:
        r = queue.popleft()
        for ch, s in goto[r].items():
            queue.append(s)
            state = fail[r]
            while True:
                f = goto[state].get(ch)
                if f is not None:
                    break
                if state == 0:
                    f = 0
                    break
                state = fail[state]
            fail[s] = f
            if out[f]:
                out[s] = out[s] + out[f]  # inherit the outputs of the failure target

    lengths = [len(word) for word in queries]
    return goto, fail, out, lengths


def search(text, state):
    """Scan text once; return every (start, query_index) occurrence."""
    goto, fail, out, lengths = state
    matches = []
    node = 0
    for i, ch in enumerate(text):
        while True:
            nxt = goto[node].get(ch)  # attempted goto transition
            if nxt is not None:
                node = nxt
                break
            if node == 0:
                break  # the root loops to itself on any missing character
            node = fail[node]  # follow the failure link and try again
        for qi in out[node]:
            matches.append((i - lengths[qi] + 1, qi))
    matches.sort()
    return matches


# ---------------------------------------------------------------------------
# Counted versions (same logic, plus counters)
# ---------------------------------------------------------------------------
def preprocess_counted(queries):
    """Same as preprocess(), counting child lookups and failure-link steps."""
    comparisons = 0
    goto = [{}]
    fail = [0]
    out = [[]]

    for qi, word in enumerate(queries):
        node = 0
        for ch in word:
            comparisons += 1  # child lookup while inserting
            nxt = goto[node].get(ch)
            if nxt is None:
                nxt = len(goto)
                goto.append({})
                fail.append(0)
                out.append([])
                goto[node][ch] = nxt
            node = nxt
        out[node].append(qi)

    queue = deque(goto[0].values())
    while queue:
        r = queue.popleft()
        for ch, s in goto[r].items():
            queue.append(s)
            state = fail[r]
            while True:
                comparisons += 1  # child lookup while building failure links
                f = goto[state].get(ch)
                if f is not None:
                    break
                if state == 0:
                    f = 0
                    break
                comparisons += 1  # failure-link step while building failure links
                state = fail[state]
            fail[s] = f
            if out[f]:
                out[s] = out[s] + out[f]

    lengths = [len(word) for word in queries]
    return (goto, fail, out, lengths), comparisons


def search_counted(text, state):
    """Same as search(); counts attempted goto transitions and, separately, failure steps."""
    goto, fail, out, lengths = state
    matches = []
    comparisons = 0
    failure_steps = 0
    node = 0
    for i, ch in enumerate(text):
        while True:
            comparisons += 1  # attempted goto transition (successful or not)
            nxt = goto[node].get(ch)
            if nxt is not None:
                node = nxt
                break
            if node == 0:
                break
            failure_steps += 1  # following the failure link itself
            node = fail[node]
        for qi in out[node]:
            matches.append((i - lengths[qi] + 1, qi))
    matches.sort()
    return matches, comparisons, failure_steps


def trie_keys(state):
    """Every character key stored in the trie (used by the memory pass, not timed)."""
    goto = state[0]
    return [key for children in goto for key in children]


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
