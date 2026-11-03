"""Descriptive summary tables shared by run_benchmark.py, analyze.py and replicate.py.

The wide tables follow the paper's layout: rows are algorithm x text length,
columns are the levels of the factor being studied.
"""

import config
from src.report import fmt_int, fmt_num, md_table, range_label, stat_cell

# Each "view" is one way of slicing an experiment by a single factor.
FACTOR_VIEWS = [
    {
        "key": "text_type",
        "title": "Core grid: random vs. narrative text",
        "pooling": "pooled over the 3 query lengths and both query counts",
        "experiment": "core",
        "factor": "text_type",
        "levels": ["random", "narrative"],
        "labels": ["Random", "Narrative"],
    },
    {
        "key": "num_queries",
        "title": "Core grid: 1 vs. 5 queries",
        "pooling": "pooled over both text types and the 3 query lengths",
        "experiment": "core",
        "factor": "num_queries",
        "levels": [1, 5],
        "labels": ["1 query", "5 queries"],
    },
    {
        "key": "query_style",
        "title": "Query-pattern experiment: distinct vs. repeating",
        "pooling": "narrative text, one query of length 5–10",
        "experiment": "query_pattern",
        "factor": "query_style",
        "levels": ["distinct", "repeating"],
        "labels": ["Distinct", "Repeating"],
    },
    {
        "key": "alphabet_size",
        "title": "Alphabet-size experiment",
        "pooling": "random text, one query of length 5–10",
        "experiment": "alphabet",
        "factor": "alphabet_size",
        "levels": ["2", "4", "26", "full"],
        "labels": ["|Σ| = 2", "|Σ| = 4", "|Σ| = 26", "Full Alice Σ"],
    },
]

# (column, title, scale, decimals, unit)
METRICS = [
    ("total_time", "Total time (prep + search)", 1e6, 2, "µs per call"),
    ("prep_time", "Preprocessing time", 1e6, 3, "µs per call"),
    ("search_time", "Search time", 1e6, 2, "µs per call"),
    ("total_comparisons", "Comparisons (prep + search)", 1, 1, "count"),
    ("memory_bytes", "Memory, structure only (memory_bytes, tested)", 1, 0, "bytes"),
    ("memory_retained_raw_bytes", "Memory, raw retained size (descriptive only)", 1, 0, "bytes"),
    ("memory_peak_bytes", "Peak memory during preprocessing (descriptive only)", 1, 0, "bytes"),
]

CELL_NOTE = (
    "Each cell: mean ± SD, then median (Mdn) and interquartile range (IQR = Q3 − Q1)."
)


def subset(df, **equals):
    """Rows where every given column equals the given value."""
    mask = None
    for col, val in equals.items():
        m = df[col] == val
        mask = m if mask is None else (mask & m)
    return df[mask] if mask is not None else df


def wide_table(df, view, metric):
    column, title, scale, decimals, unit = metric
    exp_df = subset(df, experiment=view["experiment"])
    rows = []
    ns = set()
    for algo in config.ALGORITHMS:
        for tr in config.TEXT_LENGTH_RANGES:
            cells = []
            for level in view["levels"]:
                vals = subset(exp_df, algorithm=algo, text_length_range=tr, **{view["factor"]: level})[column]
                ns.add(len(vals))
                cells.append(stat_cell(vals.to_numpy(dtype=float), scale, decimals))
            rows.append([config.ALGORITHM_LABELS[algo], range_label(tr), *cells])
    headers = ["Algorithm", "Text length", *view["labels"]]
    n_note = ", ".join(str(n) for n in sorted(ns))
    return (
        f"**{title}** ({unit})\n\n"
        + md_table(headers, rows, ["l", "l"] + ["r"] * len(view["levels"]))
        + f"\n*Units: {unit}. {CELL_NOTE} N per cell: {n_note}.*\n"
    )


def positive_control_table(df):
    """Naive vs. KMP vs. Aho-Corasick on text 'a'*n with query 'a'*(m-1)+'b'."""
    pc = subset(df, experiment="positive_control")
    rows = []
    for tr in config.TEXT_LENGTH_RANGES:
        level = subset(pc, text_length_range=tr)
        if level.empty:
            continue
        n = int(level["text_length"].iloc[0])
        m = int(str(level["query_lengths"].iloc[0]))
        row = [range_label(tr), f"{n:,}", m, f"{(n - m + 1) * m:,}"]
        for algo in config.ALGORITHMS:
            a = subset(level, algorithm=algo)
            comps = a["total_comparisons"].median()
            row += [fmt_int(comps), fmt_num(comps / n, 2), fmt_num(a["total_time"].median() * 1e6, 2)]
        rows.append(row)
    headers = ["Text length", "n", "m", "Expected Naive (n−m+1)·m"]
    for algo in config.ALGORITHMS:
        label = config.ALGORITHM_LABELS[algo]
        headers += [f"{label} comparisons", f"{label} comparisons / char", f"{label} median time (µs)"]
    return (
        md_table(headers, rows, ["l", "r", "r", "r"] + ["r"] * 9)
        + "\n*Comparisons = prep + search (identical in every run, so the median equals every value). "
        "Comparisons / char = comparisons ÷ n. Time = median total time in µs per call over the runs.*\n"
    )


# ---------------------------------------------------------------------------
# Conditions (all factor levels including algorithm)
# ---------------------------------------------------------------------------
CONDITION_FIELDS = [
    "experiment", "text_type", "alphabet_size", "text_length_range",
    "query_length_range", "query_style", "num_queries",
]

_ORDER = {
    "experiment": list(config.EXPERIMENTS),
    "text_type": ["random", "narrative", ""],
    "alphabet_size": ["", *config.ALPHABETS],
    "text_length_range": list(config.TEXT_LENGTH_RANGES),
    "query_length_range": list(config.QUERY_LENGTH_RANGES),
    "query_style": ["", *config.QUERY_STYLES],
    "algorithm": list(config.ALGORITHMS),
}


def _norm(value):
    """Blank/NaN -> '', everything else -> str (so the int 1 and the string '1' compare equal)."""
    if value is None or (isinstance(value, float) and value != value):
        return ""
    return str(value)


def group_key(row, include_algorithm=True):
    """Hashable key for a condition (or condition group, if include_algorithm=False)."""
    key = tuple(_norm(row[f]) for f in CONDITION_FIELDS)
    return key + ((row["algorithm"],) if include_algorithm else ())


def sort_key(key):
    """Sort condition keys in the paper's order."""
    fields = CONDITION_FIELDS + (["algorithm"] if len(key) > len(CONDITION_FIELDS) else [])
    out = []
    for f, v in zip(fields, key):
        order = _ORDER.get(f)
        if order is not None:
            out.append(order.index(v) if v in order else len(order))
        else:
            out.append(int(v) if str(v).isdigit() else 0)
    return tuple(out)


def condition_label(key):
    """Short readable description of a condition group key (without algorithm)."""
    d = dict(zip(CONDITION_FIELDS, key))
    parts = [d["experiment"]]
    if d["experiment"] == "core":
        parts += [d["text_type"], f"q {range_label(d['query_length_range'])}", f"k={d['num_queries']}"]
    elif d["experiment"] == "query_pattern":
        parts += [d["query_style"]]
    elif d["experiment"] == "alphabet":
        parts += [f"|Σ|={d['alphabet_size']}"]
    parts.append(f"n {range_label(d['text_length_range'])}")
    return ", ".join(parts)


def per_condition_table(df):
    """One row per condition (171 in the full design) with all five metrics."""
    groups = {}
    for idx, row in enumerate(df[CONDITION_FIELDS + ["algorithm"]].to_dict("records")):
        groups.setdefault(group_key(row), []).append(idx)
    rows = []
    for key in sorted(groups, key=sort_key):
        sub = df.iloc[groups[key]]
        cells = [stat_cell(sub[c].to_numpy(dtype=float), s, d) for c, _, s, d, _ in METRICS]
        rows.append([condition_label(key[:-1]), config.ALGORITHM_LABELS[key[-1]], len(sub), *cells])
    headers = ["Condition", "Algorithm", "N"] + [f"{t} ({u})" for _, t, _, _, u in METRICS]
    return md_table(headers, rows, ["l", "l", "r"] + ["r"] * len(METRICS)) + f"\n*{CELL_NOTE}*\n"
