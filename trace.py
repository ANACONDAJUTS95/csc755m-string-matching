"""Write a step-by-step trace of one algorithm as a Markdown table.

One table row per character comparison, using exactly the comparison-counting
definitions of the benchmark. At the end the trace checks itself against the
counted version in src/: the number of rows must equal the counted
comparisons and the matches must be identical.

Usage:
    python trace.py --algorithm naive --text "abcabd" --queries "abd"
    python trace.py --algorithm kmp --text "ABABCABABA" --queries "ABABA"
    python trace.py --algorithm aho_corasick --text "ushers" \\
        --queries he --queries she --queries his --queries hers
Output: traces/<name>.md  (default name: <algorithm>_<text>; change it with --name)
"""

import argparse
import re
import sys

import config
from src import ALGORITHM_MODULES
from src.report import md_escape, md_table, md_text


def ch(c):
    """A single character as a code span, with the space made visible."""
    if c == " ":
        return "`␠`"
    if c == "|":
        return "`\\|`"
    if c == "`":
        return "`` ` ``"
    return f"`{c}`"


def yes_no(flag):
    return "✓" if flag else "✗"


# ---------------------------------------------------------------------------
# Naive
# ---------------------------------------------------------------------------
def trace_naive(text, queries):
    rows, matches = [], []
    step = 0
    n = len(text)
    for qi, p in enumerate(queries):
        m = len(p)
        for i in range(n - m + 1):
            j = 0
            while j < m:
                step += 1
                equal = text[i + j] == p[j]
                if not equal:
                    action = f"mismatch → shift pattern to i = {i + 1}"
                elif j + 1 == m:
                    action = f"**report match at {i}** → shift pattern to i = {i + 1}"
                else:
                    action = "advance j"
                rows.append([step, qi, i, i + j, j, f"{ch(text[i + j])} vs {ch(p[j])}", yes_no(equal), action])
                if not equal:
                    break
                j += 1
            if j == m:
                matches.append((i, qi))
    table = md_table(["Step", "Query", "Alignment i", "Text index", "Pattern index j", "Compared",
                      "Match?", "Action"], rows, ["r", "r", "r", "r", "r", "c", "c", "l"])
    return [("Search", table)], sorted(matches), 0, step


# ---------------------------------------------------------------------------
# KMP
# ---------------------------------------------------------------------------
def trace_lps(p):
    rows = []
    m = len(p)
    lps = [0] * m
    length, i, step = 0, 1, 0
    while i < m:
        step += 1
        equal = p[i] == p[length]
        if equal:
            action = f"lps[{i}] = {length + 1}; advance i"
            row = [step, i, length, f"{ch(p[i])} vs {ch(p[length])}", yes_no(True), action]
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            action = f"fall back: len = LPS[{length - 1}] = {lps[length - 1]} (i stays)"
            row = [step, i, length, f"{ch(p[i])} vs {ch(p[length])}", yes_no(False), action]
            length = lps[length - 1]
        else:
            action = f"lps[{i}] = 0; advance i"
            row = [step, i, length, f"{ch(p[i])} vs {ch(p[length])}", yes_no(False), action]
            lps[i] = 0
            i += 1
        rows.append(row)
    return lps, rows, step


def trace_kmp(text, queries):
    sections, matches = [], []
    prep_total = search_total = 0
    n = len(text)
    for qi, p in enumerate(queries):
        lps, lps_rows, lps_steps = trace_lps(p)
        prep_total += lps_steps
        lps_table = md_table(["Index", *range(len(p))], [["Character", *[ch(c) for c in p]], ["LPS", *lps]],
                             ["l"] + ["c"] * len(p))
        build = (md_table(["Step", "i", "len", "Compared p[i] vs p[len]", "Match?", "Action"], lps_rows,
                          ["r", "r", "r", "c", "c", "l"]) if lps_rows else "*(pattern of length 1: no comparisons)*\n")
        sections.append((f"Query {qi} {md_text(p)}: building the LPS table ({lps_steps} comparisons)",
                         build + "\nResulting LPS table:\n\n" + lps_table))

        rows = []
        m = len(p)
        i = j = step = 0
        while i < n:
            step += 1
            equal = text[i] == p[j]
            compared = f"{ch(text[i])} vs {ch(p[j])}"
            if equal:
                if j + 1 == m:
                    action = (f"**report match at {i + 1 - m}**; fall back via LPS[{j}] = {lps[j]}; advance i")
                else:
                    action = "advance i and j"
                rows.append([step, i, j, compared, yes_no(True), action])
                i += 1
                j += 1
                if j == m:
                    matches.append((i - m, qi))
                    j = lps[j - 1]
            elif j != 0:
                rows.append([step, i, j, compared, yes_no(False),
                             f"fall back via LPS[{j - 1}] = {lps[j - 1]} (re-check text[{i}])"])
                j = lps[j - 1]
            else:
                rows.append([step, i, j, compared, yes_no(False), "shift: i → i + 1"])
                i += 1
        search_total += step
        sections.append((f"Query {qi} {md_text(p)}: search ({step} comparisons)",
                         md_table(["Step", "Text index i", "Pattern index j", "Compared", "Match?", "Action"],
                                  rows, ["r", "r", "r", "c", "c", "l"])))
    return sections, sorted(matches), prep_total, search_total


# ---------------------------------------------------------------------------
# Aho-Corasick
# ---------------------------------------------------------------------------
def trace_aho_corasick(text, queries):
    module = ALGORITHM_MODULES["aho_corasick"]
    (goto, fail, out, lengths), prep = module.preprocess_counted(queries)

    # Path string of every node, for readable state names.
    path = {0: ""}
    order = [0]
    for node in order:
        for c, child in goto[node].items():
            path[child] = path[node] + c
            order.append(child)

    def state(s):
        return "0 (root)" if s == 0 else f"{s} ({md_text(path[s])})"

    def outputs(s):
        return ", ".join(md_text(queries[q]) for q in out[s]) or "—"

    trie_rows = [[state(s), ", ".join(f"{ch(c)}→{t}" for c, t in goto[s].items()) or "—",
                  state(fail[s]) if s else "—", outputs(s)] for s in sorted(path)]
    trie = md_table(["State (path)", "Goto (children)", "Failure link", "Output"], trie_rows)

    rows, matches = [], []
    node = step = failure_steps = 0
    for i, c in enumerate(text):
        while True:
            step += 1
            nxt = goto[node].get(c)
            tried = f"goto({node}, {ch(c)})"
            if nxt is not None:
                found = [(i - lengths[q] + 1, q) for q in out[nxt]]
                matches.extend(found)
                reported = ", ".join(f"**{md_text(queries[q])} at {start}**" for start, q in found) or "—"
                rows.append([step, i, ch(c), state(node), tried, f"→ {state(nxt)}", "—", reported])
                node = nxt
                break
            if node == 0:
                rows.append([step, i, ch(c), state(0), tried, "fail → stay at root", "—", "—"])
                break
            failure_steps += 1
            rows.append([step, i, ch(c), state(node), tried, "fail", f"{node} → {state(fail[node])}", "—"])
            node = fail[node]
    search = md_table(["Step", "Text index", "Character", "Current state", "Transition tried", "Result",
                       "Failure link followed", "Outputs reported"], rows,
                      ["r", "r", "c", "l", "l", "l", "l", "l"])
    sections = [
        (f"Automaton ({len(goto)} states, {prep} preprocessing comparisons)", trie),
        (f"Search ({step} attempted transitions, {failure_steps} failure-link steps)", search),
    ]
    return sections, sorted(matches), prep, step


TRACERS = {"naive": trace_naive, "kmp": trace_kmp, "aho_corasick": trace_aho_corasick}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--algorithm", required=True, choices=config.ALGORITHMS)
    parser.add_argument("--text", required=True)
    parser.add_argument("--queries", required=True, action="append",
                        help="a query; repeat --queries for several")
    parser.add_argument("--name", help="output file name without .md")
    args = parser.parse_args()

    if any(q == "" for q in args.queries):
        sys.exit("Queries must be non-empty.")

    sections, matches, prep, search = TRACERS[args.algorithm](args.text, args.queries)

    # Self-check against the benchmark's counted version.
    counted = ALGORITHM_MODULES[args.algorithm].find_all_counted(args.text, args.queries)
    consistent = (counted["matches"] == matches and counted["prep_comparisons"] == prep
                  and counted["search_comparisons"] == search)
    if not consistent:
        sys.exit("Trace disagrees with the counted version in src/ — this is a bug in trace.py.")

    label = config.ALGORITHM_LABELS[args.algorithm]
    lines = [
        f"# {label} trace",
        "",
        md_table(["Item", "Value"], [
            ["Text", md_text(args.text)],
            ["Text length n", len(args.text)],
            ["Queries", "<br>".join(f"{qi}: {md_text(q)}" for qi, q in enumerate(args.queries))],
            ["Preprocessing comparisons", prep],
            ["Search comparisons", search],
            ["Matches (start, query)", md_escape(", ".join(f"({s}, {q})" for s, q in matches) or "none")],
            ["Agrees with `src/` counted version", "✓ yes"],
        ]),
        "Characters are shown as code; `␠` is a space. ✓ = characters equal, ✗ = different.",
        "",
    ]
    for heading, body in sections:
        lines += [f"## {heading}", "", body, ""]

    name = args.name or f"{args.algorithm}_{re.sub(r'[^A-Za-z0-9_-]+', '_', args.text)[:30]}"
    config.TRACES_DIR.mkdir(parents=True, exist_ok=True)
    path = config.TRACES_DIR / f"{name}.md"
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Wrote {path.relative_to(config.ROOT)} ({prep} prep + {search} search comparisons, "
          f"{len(matches)} match(es))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
