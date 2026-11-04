"""Statistics on the primary machine's results (H0-1 ... H0-12).

Reads results/primary/raw_runs.csv and writes
    results/primary/stats_report.md     hypothesis tests, descriptive section, figures
    results/primary/figures/*.png       bar charts (mean ± SD)
    results/primary/paper_values.md     checklist of numbers for the paper

Test procedure (alpha = 0.05), run per algorithm and per text-length level:
  * Shapiro-Wilk on every group.
  * 2 groups: Welch's t-test if every group is normal, else Mann-Whitney U (two-sided).
  * 4 groups: one-way ANOVA if every group is normal, else Kruskal-Wallis.
  * Effect sizes: Cohen's d / Cliff's delta / eta squared / epsilon squared.
  * Holm's correction across all 81 tests as one family.

Dependent variables: time and comparisons are divided by the text length n (ns per text
character, comparisons per text character); memory is memory_bytes. The first, unnormalized
analysis (raw time and raw comparisons, its own Holm family of 81) is reported in an appendix.

Usage:
    python analyze.py           # full results
    python analyze.py --pilot   # pilot results (results/primary/pilot/), no 81-test assertion
"""

import argparse
import json
import sys
import warnings

import matplotlib

matplotlib.use("Agg")  # write PNG files; no window needed
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

import config  # noqa: E402
from src.inputs_io import read_manifest_hash, read_raw_runs, results_dir  # noqa: E402
from src.measure import utc_now  # noqa: E402
from src.report import describe, fmt_int, fmt_num, fmt_p, md_escape, md_table, range_label  # noqa: E402
from src.summaries import FACTOR_VIEWS, positive_control_table, subset  # noqa: E402

# Okabe-Ito colour-blind-safe palette, plus hatches so the bars also work in greyscale.
COLORS = ["#0072B2", "#E69F00", "#009E73", "#CC79A7"]
HATCHES = ["", "//", "..", "xx"]

ALL = list(config.ALGORITHMS)
KMP_AC = ["kmp", "aho_corasick"]
AC = ["aho_corasick"]

# Dependent variables: key -> (column, name, scale, decimals, unit)
# Primary analysis: time and comparisons per text character (columns added by add_per_char_columns).
DVS = {
    "time": ("time_per_char", "total time ÷ text length", 1e9, 2, "ns per text character"),
    "comparisons": ("comparisons_per_char", "comparisons (prep + search) ÷ text length", 1, 3,
                    "comparisons per text character"),
    "memory": ("memory_bytes", "memory use (structure bytes)", 1, 0, "bytes"),
}
# Appendix: the first, unnormalized analysis.
RAW_DVS = {
    "time": ("total_time", "total time", 1e6, 2, "µs"),
    "comparisons": ("total_comparisons", "comparisons (prep + search)", 1, 1, "comparisons"),
    "memory": ("memory_bytes", "memory use (structure bytes)", 1, 0, "bytes"),
}

NORMALIZATION_NOTE = (
    "Time and comparisons are divided by text length n before testing because exact lengths vary up to "
    "tenfold within each level and are drawn independently for each condition. This normalization was "
    "adopted after inspecting the first, unnormalized analysis, which is reported in the appendix."
)


def add_per_char_columns(df):
    """Add time_per_char (seconds per text character) and comparisons_per_char."""
    df = df.copy()
    n = df["text_length"].astype(float)
    df["time_per_char"] = df["total_time"] / n
    df["comparisons_per_char"] = df["total_comparisons"] / n
    return df

VIEW = {v["key"]: v for v in FACTOR_VIEWS}

# The 12 null hypotheses. The wording here is generic; use your paper's wording.
HYPOTHESES = [
    ("H0-1", "text_type", "time", ALL),
    ("H0-2", "text_type", "comparisons", ALL),
    ("H0-3", "text_type", "memory", KMP_AC),
    ("H0-4", "num_queries", "time", AC),
    ("H0-5", "num_queries", "comparisons", AC),
    ("H0-6", "num_queries", "memory", AC),
    ("H0-7", "query_style", "time", ALL),
    ("H0-8", "query_style", "comparisons", ALL),
    ("H0-9", "query_style", "memory", KMP_AC),
    ("H0-10", "alphabet_size", "time", ALL),
    ("H0-11", "alphabet_size", "comparisons", ALL),
    ("H0-12", "alphabet_size", "memory", KMP_AC),
]
STATEMENTS = {
    "H0-1": "There is no significant difference in completion time between random text and narrative text, for each algorithm.",
    "H0-2": "There is no significant difference in character comparisons between random text and narrative text, for each algorithm.",
    "H0-3": "There is no significant difference in memory use between random text and narrative text, for each algorithm.",
    "H0-4": "There is no significant difference in completion time between different numbers of query strings for the Aho-Corasick algorithm.",
    "H0-5": "There is no significant difference in character comparisons between different numbers of query strings for the Aho-Corasick algorithm.",
    "H0-6": "There is no significant difference in memory use between different numbers of query strings for the Aho-Corasick algorithm.",
    "H0-7": "There is no significant difference in completion time between query strings of distinct characters and query strings containing repeating substrings, for each algorithm.",
    "H0-8": "There is no significant difference in character comparisons between query strings of distinct characters and query strings containing repeating substrings, for each algorithm.",
    "H0-9": "There is no significant difference in memory use between query strings of distinct characters and query strings containing repeating substrings, for each algorithm.",
    "H0-10": "There is no significant difference in completion time between random texts over alphabets of 2, 4, 26, and |Σ| characters (|Σ| = the full Alice character set), for each algorithm.",
    "H0-11": "There is no significant difference in character comparisons between random texts over alphabets of 2, 4, 26, and |Σ| characters, for each algorithm.",
    "H0-12": "There is no significant difference in memory use between random texts over alphabets of 2, 4, 26, and |Σ| characters, for each algorithm.",
}

FACTOR_PHRASE = {
    "text_type": "text type (random vs. narrative)",
    "num_queries": "the number of queries (1 vs. 5)",
    "query_style": "query pattern (distinct vs. repeating)",
    "alphabet_size": "alphabet size (2, 4, 26, full Σ)",
}
EXPECTED_GROUP_SIZE = {"text_type": 180, "num_queries": 180, "query_style": 30, "alphabet_size": 30}

FIGURE_NUMBERS = {"text_type": "5.2", "num_queries": "5.3", "query_style": "5.4", "alphabet_size": "5.5"}
FIGURE_LETTERS = {"time": "a", "comparisons": "b", "memory": "c"}


# ---------------------------------------------------------------------------
# Effect sizes
# ---------------------------------------------------------------------------
def cohens_d(a, b):
    """Mean difference divided by the pooled SD."""
    na, nb = len(a), len(b)
    pooled = np.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2))
    return float((np.mean(a) - np.mean(b)) / pooled)


def cliffs_delta(a, b):
    """P(a > b) - P(a < b) over all pairs. Range -1 .. 1."""
    a = np.asarray(a)[:, None]
    b = np.asarray(b)[None, :]
    return float((np.sum(a > b) - np.sum(a < b)) / (a.size * b.size))


def eta_squared(groups):
    """Between-group sum of squares / total sum of squares."""
    allv = np.concatenate(groups)
    grand = allv.mean()
    ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ss_total = ((allv - grand) ** 2).sum()
    return float(ss_between / ss_total)


def label_d(d):  # Cohen (1988) conventions
    d = abs(d)
    return "negligible" if d < 0.2 else "small" if d < 0.5 else "medium" if d < 0.8 else "large"


def label_delta(delta):  # thresholds given in the study design
    delta = abs(delta)
    return "negligible" if delta < 0.11 else "small" if delta < 0.28 else "medium" if delta < 0.43 else "large"


def label_eta_eps(v):  # small 0.01, medium 0.06, large 0.14
    return "negligible" if v < 0.01 else "small" if v < 0.06 else "medium" if v < 0.14 else "large"


# ---------------------------------------------------------------------------
# One test
# ---------------------------------------------------------------------------
def run_test(groups, labels):
    """Choose and run the test for a list of groups. Returns a result dict (p=None if N/A)."""
    res = {"p": None, "na_reason": None, "notes": [], "normality": [], "test": "—",
           "statistic": "—", "effect": "—", "effect_value": None}
    groups = [np.asarray(g, dtype=float) for g in groups]

    if any(len(g) < 3 for g in groups):
        res["na_reason"] = "not applicable: a group has fewer than 3 values"
        res["test"] = "not applicable"
        return res
    allv = np.concatenate(groups)
    if np.all(allv == allv[0]):
        res["na_reason"] = "not applicable: no variance"
        res["test"] = "not applicable: no variance"
        res["notes"].append("every value in every group is identical")
        return res

    all_normal = True
    for g, lab in zip(groups, labels):
        if np.all(g == g[0]):
            res["normality"].append(f"{lab}: zero variance, Shapiro-Wilk skipped")
            res["notes"].append(f"{lab} has zero variance → non-parametric test")
            all_normal = False
            continue
        w, p = stats.shapiro(g)
        normal = p >= config.ALPHA
        all_normal &= normal
        res["normality"].append(f"{lab}: W = {w:.3f}, p = {fmt_p(p)} {'✓ normal' if normal else '✗ not normal'}")

    if len(groups) == 2:
        a, b = groups
        if all_normal:
            t = stats.ttest_ind(a, b, equal_var=False)
            d = cohens_d(a, b)
            res.update(test="Welch's t-test", statistic=f"t = {t.statistic:.3f} (df = {t.df:.1f})",
                       p=float(t.pvalue), effect_value=d,
                       effect=f"d = {d:+.3f} ({label_d(d)})")
        else:
            u = stats.mannwhitneyu(a, b, alternative="two-sided")
            delta = cliffs_delta(a, b)
            res.update(test="Mann-Whitney U", statistic=f"U = {u.statistic:,.1f}",
                       p=float(u.pvalue), effect_value=delta,
                       effect=f"δ = {delta:+.3f} ({label_delta(delta)})")
        sign = res["effect_value"]
        if sign:
            hi, lo = (labels[0], labels[1]) if sign > 0 else (labels[1], labels[0])
            res["effect"] += f"; {hi} > {lo}"
    else:
        n_total = len(allv)
        k = len(groups)
        if all_normal:
            f = stats.f_oneway(*groups)
            eta = eta_squared(groups)
            res.update(test="One-way ANOVA", statistic=f"F({k - 1}, {n_total - k}) = {f.statistic:.3f}",
                       p=float(f.pvalue), effect_value=eta, effect=f"η² = {eta:.3f} ({label_eta_eps(eta)})")
        else:
            h = stats.kruskal(*groups)
            eps = float(h.statistic / (n_total - 1))
            res.update(test="Kruskal-Wallis", statistic=f"H = {h.statistic:.3f} (df = {k - 1})",
                       p=float(h.pvalue), effect_value=eps, effect=f"ε² = {eps:.3f} ({label_eta_eps(eps)})")
    return res


def holm(pvalues, family_size):
    """Holm step-down adjusted p-values.

    Tests without a p-value (not applicable) stay in the family: they are ranked
    last, which is the same as giving them p = 1, and they are never rejected.
    """
    order = sorted((i for i, p in enumerate(pvalues) if p is not None), key=lambda i: pvalues[i])
    adjusted = [None] * len(pvalues)
    running_max = 0.0
    for rank, i in enumerate(order):
        value = min(1.0, (family_size - rank) * pvalues[i])
        running_max = max(running_max, value)
        adjusted[i] = running_max
    return adjusted


# ---------------------------------------------------------------------------
# All 81 tests
# ---------------------------------------------------------------------------
def run_all_tests(df, pilot, dvs=DVS):
    tests = []
    for hyp_id, factor, dv, algorithms in HYPOTHESES:
        view = VIEW[factor]
        column, _, scale, decimals, unit = dvs[dv]
        exp_df = subset(df, experiment=view["experiment"])
        for algo in algorithms:
            for tr in config.TEXT_LENGTH_RANGES:
                cell = subset(exp_df, algorithm=algo, text_length_range=tr)
                groups = [subset(cell, **{factor: lv})[column].to_numpy(dtype=float) for lv in view["levels"]]
                if not pilot:
                    expected = EXPECTED_GROUP_SIZE[factor]
                    sizes = [len(g) for g in groups]
                    if any(s != expected for s in sizes):
                        sys.exit(f"{hyp_id} {algo} {tr}: group sizes {sizes}, expected {expected} each. "
                                 "Is raw_runs.csv complete?")
                res = run_test(groups, view["labels"])
                res.update(hyp=hyp_id, factor=factor, dv=dv, algorithm=algo, text_range=tr,
                           group_stats=[(lab, describe(g)) for lab, g in zip(view["labels"], groups)],
                           scale=scale, decimals=decimals, unit=unit)
                tests.append(res)

    if not pilot:
        assert len(tests) == config.EXPECTED_TESTS, f"expected {config.EXPECTED_TESTS} tests, got {len(tests)}"
    adjusted = holm([t["p"] for t in tests], len(tests))
    for t, adj in zip(tests, adjusted):
        t["p_holm"] = adj
        if t["p"] is None:
            t["decision"] = "Not applicable"
        else:
            t["decision"] = "Reject H0" if adj < config.ALPHA else "Fail to reject H0"
    return tests


# ---------------------------------------------------------------------------
# Report pieces
# ---------------------------------------------------------------------------
def group_stats_cell(t):
    s, dec = t["scale"], t["decimals"]
    return "<br>".join(
        f"{md_escape(lab)}: {fmt_num(d['mean'] * s, dec)} ± {fmt_num(d['sd'] * s, dec)} "
        f"(Mdn {fmt_num(d['median'] * s, dec)}, n = {d['n']})"
        for lab, d in t["group_stats"]
    )


def decision_cell(t):
    if t["decision"] == "Reject H0":
        return "**Reject H0**"
    return t["decision"]


def decisions_summary(tests):
    rows = []
    for i, t in enumerate(tests, 1):
        rows.append([i, t["hyp"], config.ALGORITHM_LABELS[t["algorithm"]], range_label(t["text_range"]),
                     t["test"], fmt_p(t["p_holm"]), decision_cell(t)])
    counts = []
    for hyp_id, *_ in HYPOTHESES:
        ts = [t for t in tests if t["hyp"] == hyp_id]
        counts.append([hyp_id, len(ts), sum(t["decision"] == "Reject H0" for t in ts),
                       sum(t["decision"] == "Fail to reject H0" for t in ts),
                       sum(t["decision"] == "Not applicable" for t in ts)])
    counts.append(["**Total**", len(tests), sum(c[2] for c in counts), sum(c[3] for c in counts),
                   sum(c[4] for c in counts)])
    return (
        md_table(["Hypothesis", "Tests", "Reject", "Fail to reject", "Not applicable"], counts,
                 ["l", "r", "r", "r", "r"])
        + "\n"
        + md_table(["#", "Hypothesis", "Algorithm", "Text length", "Test", "Holm-adjusted p", "Decision"],
                   rows, ["r", "l", "l", "l", "l", "r", "l"])
    )


def hypothesis_section(hyp_id, factor, dv, algorithms, tests, dvs=DVS, heading="##", tag="",
                       figure_ref=True):
    ts = [t for t in tests if t["hyp"] == hyp_id]
    unit = dvs[dv][4]
    rows = []
    for t in ts:
        normality = "<br>".join(t["normality"]) or "—"
        effect = t["effect"]
        if t["notes"]:
            effect += "<br>*Note: " + "; ".join(t["notes"]) + "*"
        rows.append([
            config.ALGORITHM_LABELS[t["algorithm"]], range_label(t["text_range"]), group_stats_cell(t),
            normality, t["test"], t["statistic"], fmt_p(t["p"]), fmt_p(t["p_holm"]), decision_cell(t), effect,
        ])
    view = VIEW[factor]
    fig = f"Figure {FIGURE_NUMBERS[factor]}{FIGURE_LETTERS[dv]}"
    return "\n".join([
        f"{heading} {hyp_id}{tag}: {md_escape(STATEMENTS[hyp_id])}",
        "",
        f"{hyp_id}: {md_escape(STATEMENTS[hyp_id])}",
        "",
        f"*Experiment: `{view['experiment']}` ({view['pooling']}). Dependent variable: {dvs[dv][1]} "
        f"({unit}). Algorithms tested: {', '.join(config.ALGORITHM_LABELS[a] for a in algorithms)}.*",
        "",
        md_table(
            ["Algorithm", "Text length", "Group stats (mean ± SD, median)", "Normality result", "Test used",
             "Statistic", "Raw p", "Holm-adjusted p", "Decision", "Effect size (label)"],
            rows, ["l", "l", "l", "l", "l", "l", "r", "r", "l", "l"]),
        f"*Group stats in {unit}." + (f" See {fig}.*" if figure_ref else "*"),
        "",
    ])


def core_grid_tables(df, normalized, heading="###", tag=""):
    """Naive/KMP 1 vs. 5 queries and the query-length split, per text character or in raw units."""
    core = subset(df, experiment="core").copy()
    n = core["text_length"].astype(float)
    if normalized:
        core["search_comparisons_dv"] = core["search_comparisons"] / n
        core["search_time_dv"] = core["search_time"] / n
        sc_unit, st_unit, st_scale, sc_dec = "per text character", "ns per text character", 1e9, 3
        split_tables = [
            ("time_per_char", "Median total time ÷ text length (ns per text character)", 1e9, 2, "median"),
            ("comparisons_per_char", "Mean comparisons (prep + search) ÷ text length "
             "(comparisons per text character)", 1, 3, "mean"),
        ]
    else:
        core["search_comparisons_dv"] = core["search_comparisons"]
        core["search_time_dv"] = core["search_time"]
        sc_unit, st_unit, st_scale, sc_dec = "", "µs", 1e6, 1
        split_tables = [
            ("total_time", "Median total time (µs)", 1e6, 2, "median"),
            ("total_comparisons", "Mean comparisons (prep + search)", 1, 1, "mean"),
        ]
    out = []

    # A. Naive and KMP, 1 vs 5 queries
    rows = []
    for algo in ("naive", "kmp"):
        for tr in config.TEXT_LENGTH_RANGES:
            c = subset(core, algorithm=algo, text_length_range=tr)
            one, five = subset(c, num_queries=1), subset(c, num_queries=5)
            c1, c5 = one["search_comparisons_dv"].mean(), five["search_comparisons_dv"].mean()
            t1, t5 = one["search_time_dv"].median(), five["search_time_dv"].median()
            rows.append([config.ALGORITHM_LABELS[algo], range_label(tr), fmt_num(c1, sc_dec), fmt_num(c5, sc_dec),
                         fmt_num(c5 / c1 if c1 else float("nan"), 2), fmt_num(t1 * st_scale, 2),
                         fmt_num(t5 * st_scale, 2), fmt_num(t5 / t1 if t1 else float("nan"), 2)])
    sc = f"search comparisons {sc_unit}".strip()
    out += [
        f"{heading} Naive and KMP with 1 vs. 5 queries{tag}",
        "",
        "Naive and KMP search the text once per query, so their search cost should be about 5× "
        "with 5 queries. Pooled over both text types and the 3 query lengths."
        + (" Search comparisons and search time are divided by text length n." if normalized else ""),
        "",
        md_table(["Algorithm", "Text length", f"Mean {sc} (1 query)", f"Mean {sc} (5 queries)", "Ratio 5/1",
                  f"Median search time 1 query ({st_unit})", f"Median search time 5 queries ({st_unit})",
                  "Ratio 5/1"], rows, ["l", "l"] + ["r"] * 6),
    ]

    # B. Split by query length
    for column, title, scale, dec, agg in split_tables:
        rows = []
        for algo in config.ALGORITHMS:
            for tr in config.TEXT_LENGTH_RANGES:
                c = subset(core, algorithm=algo, text_length_range=tr)
                cells = [fmt_num(getattr(subset(c, query_length_range=qr)[column], agg)() * scale, dec)
                         for qr in config.QUERY_LENGTH_RANGES]
                rows.append([config.ALGORITHM_LABELS[algo], range_label(tr), *cells])
        out += [
            f"{heading} Core grid split by query length: {title}{tag}",
            "",
            "Pooled over both text types and both query counts.",
            "",
            md_table(["Algorithm", "Text length", *[f"Query {range_label(q)}" for q in config.QUERY_LENGTH_RANGES]],
                     rows, ["l", "l", "r", "r", "r"]),
        ]
    return out


def descriptive_section(df, sigma_size):
    out = ["## Descriptive-only results", ""]

    # A + B. Core grid tables, per text character
    out += core_grid_tables(df, normalized=True)

    # C. Naive comparisons per text position vs sigma / (sigma - 1)
    alpha = subset(df, experiment="alphabet", algorithm="naive")
    rows = []
    for size in config.ALPHABETS:
        sigma = sigma_size if size == "full" else len(config.ALPHABETS[size])
        predicted = sigma / (sigma - 1)
        for tr in config.TEXT_LENGTH_RANGES:
            c = subset(alpha, alphabet_size=size, text_length_range=tr)
            if c.empty:
                continue
            m = c["query_lengths"].astype(int)
            per_pos = c["search_comparisons"] / (c["text_length"] - m + 1)
            rows.append([size if size != "full" else f"full ({sigma})", range_label(tr), sigma,
                         fmt_num(predicted, 4), fmt_num(per_pos.mean(), 4), fmt_num(per_pos.std(ddof=1), 4),
                         fmt_num(per_pos.mean() / predicted, 3)])
    out += [
        "### Naive comparisons per text position vs. the σ/(σ − 1) prediction",
        "",
        "Alphabet-size experiment (random text, one query of length 5–10). Observed = search comparisons "
        "÷ (n − m + 1) alignments. For a uniformly random text and pattern the expected number of "
        "comparisons per alignment is about σ/(σ − 1) (exactly (1 − σ^−m)·σ/(σ − 1)); the guaranteed "
        "occurrence of the query adds a little on short texts.",
        "",
        md_table(["Alphabet", "Text length", "σ", "Predicted σ/(σ−1)", "Observed mean", "Observed SD",
                  "Observed / predicted"], rows, ["l", "l", "r", "r", "r", "r", "r"]),
    ]

    # D. Positive control, plus Naive memory
    naive_mem = df.loc[df["algorithm"] == "naive", "memory_bytes"]
    out += [
        "### Positive control",
        "",
        positive_control_table(df),
        "### Naive memory",
        "",
        f"Naive builds no preprocessing structure; its memory is recorded as 0 in "
        f"{int((naive_mem == 0).sum()):,} of {len(naive_mem):,} rows. H0-3, H0-9 and H0-12 are therefore "
        "tested only for KMP and Aho-Corasick.",
        "",
    ]

    # E. The three memory measures (descriptive) and the size of the CPython effect
    from run_benchmark import cpython_effect_section

    rows = []
    for algo in ("kmp", "aho_corasick"):
        for exp in config.EXPERIMENTS:
            c = subset(df, experiment=exp, algorithm=algo)
            if c.empty:
                continue
            rows.append([config.ALGORITHM_LABELS[algo], exp, fmt_num(c["memory_bytes"].mean(), 1),
                         fmt_num(c["memory_retained_raw_bytes"].mean(), 1),
                         fmt_num(c["memory_peak_bytes"].mean(), 1)])
    out += [
        "### Memory: structure, raw retained and peak",
        "",
        config.MEMORY_DEFINITIONS,
        "",
        md_table(["Algorithm", "Experiment", "Mean memory_bytes (tested)", "Mean memory_retained_raw_bytes",
                  "Mean memory_peak_bytes"], rows, ["l", "l", "r", "r", "r"]),
        "### Memory: size of the CPython character-object effect",
        "",
        cpython_effect_section(df),
    ]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def bar_figure(df, view, dv, path):
    column, name, scale, _, unit = DVS[dv]
    levels, labels = view["levels"], view["labels"]
    exp_df = subset(df, experiment=view["experiment"])
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
    x = np.arange(len(config.ALGORITHMS))
    width = 0.8 / len(levels)
    for ax, tr in zip(axes, config.TEXT_LENGTH_RANGES):
        for li, (lv, lab) in enumerate(zip(levels, labels)):
            means, sds = [], []
            for algo in config.ALGORITHMS:
                vals = subset(exp_df, algorithm=algo, text_length_range=tr, **{view["factor"]: lv})[column]
                vals = vals.to_numpy(dtype=float) * scale
                means.append(vals.mean() if len(vals) else np.nan)
                sds.append(vals.std(ddof=1) if len(vals) > 1 else 0.0)
            ax.bar(x + (li - (len(levels) - 1) / 2) * width, means, width, yerr=sds, capsize=3,
                   color=COLORS[li], hatch=HATCHES[li], edgecolor="black", linewidth=0.5,
                   error_kw={"elinewidth": 0.8}, label=lab)
        ax.set_xticks(x, [config.ALGORITHM_LABELS[a] for a in config.ALGORITHMS])
        ax.set_title(f"Text length {range_label(tr)}")
        ax.set_ylabel(f"{name[0].upper() + name[1:]}\n({unit})")
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", linewidth=0.3, alpha=0.6)
        ax.set_axisbelow(True)
    handles, leg_labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, leg_labels, loc="outside lower center", ncol=len(levels), frameon=False)
    fig.suptitle(f"{view['title']}: {name}, {unit} (mean ± SD)")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def make_figures(df, fig_dir):
    fig_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for view in FACTOR_VIEWS:
        for dv in DVS:
            fig_id = f"{FIGURE_NUMBERS[view['key']]}{FIGURE_LETTERS[dv]}"
            filename = f"fig{fig_id.replace('.', '_')}_{view['key']}_{dv}.png"
            bar_figure(df, view, dv, fig_dir / filename)
            made.append((fig_id, view, dv, filename))
    return made


# ---------------------------------------------------------------------------
# Paper values
# ---------------------------------------------------------------------------
def env_rows(env):
    if not env:
        return [["(not available)", ""]]
    return [
        ["OS", md_escape(env["os"])],
        ["CPU", md_escape(env["cpu_model"])],
        ["Cores (physical / logical)", f"{env['physical_cores']} / {env['logical_cores']}"],
        ["RAM", f"{env['ram_bytes'] / 2**30:.1f} GiB"],
        ["Python", f"{env['python_implementation']} {env['python_version']} ({md_escape(env['python_build'])})"],
        ["Packages", ", ".join(f"{k} {v}" for k, v in env["packages"].items())],
        ["Timer resolution", f"{env['perf_counter']['resolution_s'] * 1e9:.0f} ns"],
    ]


# Laptop model for the Model row (not detectable reliably from Python).
MACHINE_MODELS = {"primary": "TODO", "replication": "Dell Inspiron 7501"}


def ram_text(e):
    """Installed RAM rounded to GB, with usable GiB in parentheses, e.g. '32 GB (31.1 GiB usable)'."""
    usable = f"{e['ram_bytes'] / 2**30:.1f} GiB usable"
    if e.get("ram_installed_gb") is None:
        return usable
    estimated = "" if e.get("ram_installed_source", "").startswith("Get") else ", installed size estimated"
    return f"{e['ram_installed_gb']} GB ({usable}{estimated})"


def machine_table(env, rep_env):
    """Machine specs side by side: Role, Model, CPU, Cores, RAM, OS, Python version, Pinned core."""
    def col(e, key, role):
        if key == "role":
            return role.capitalize()
        if key == "model":
            return MACHINE_MODELS[role]
        if not e:
            return "(not yet run)"
        return {
            "cpu": md_escape(e["cpu_model"]),
            "cores": f"{e['physical_cores']} physical / {e['logical_cores']} logical",
            "ram": ram_text(e),
            "os": md_escape(e["os"]),
            "python": f"{e['python_implementation']} {e['python_version']}",
            "pinned": (f"Logical core {config.PIN_CORE}: "
                       + ((e.get("core_type") or {}).get("summary", "—").replace("**", "")
                          .replace(f"Logical core {config.PIN_CORE} is a ", "").rstrip("."))),
        }[key]
    rows = [["Role", "role"], ["Model", "model"], ["CPU", "cpu"], ["Cores", "cores"], ["RAM", "ram"],
            ["OS", "os"], ["Python version", "python"], ["Pinned core", "pinned"]]
    return md_table(["", "Primary machine", "Replication machine"],
                    [[f"**{label}**", col(env, key, "primary"), col(rep_env, key, "replication")]
                     for label, key in rows])


def write_paper_values(out_dir, df, tests, raw_tests, pilot):
    alice = json.loads(config.ALICE_META_JSON.read_text(encoding="utf-8"))
    env = None
    if (out_dir / "environment.json").exists():
        env = json.loads((out_dir / "environment.json").read_text(encoding="utf-8"))
    sessions = []
    if (out_dir / "sessions.jsonl").exists():
        sessions = [json.loads(s) for s in (out_dir / "sessions.jsonl").read_text(encoding="utf-8").splitlines() if s]
    rep_dir = results_dir("replication", pilot)
    rep_env = None
    if (rep_dir / "environment.json").exists():
        rep_env = json.loads((rep_dir / "environment.json").read_text(encoding="utf-8"))
    rep_rows = None
    if (rep_dir / "raw_runs.csv").exists():
        rep_rows = len(read_raw_runs(rep_dir / "raw_runs.csv"))

    priority = "—"
    pin = "—"
    if sessions:
        p = sessions[-1]["process"]
        priority = f"{'yes' if p['priority_ok'] else 'NO'} ({md_escape(p['priority_message'])})"
        pin = f"core {p['pinned_core']} ({'OK' if p['pin_ok'] else 'FAILED'})"
    duration = sum(s.get("duration_s", 0) for s in sessions)

    per_algo = [[config.ALGORITHM_LABELS[a], f"{int((df['algorithm'] == a).sum()):,}"] for a in config.ALGORITHMS]
    per_exp = [[e, f"{int((df['experiment'] == e).sum()):,}"] for e in config.EXPERIMENTS]
    rejected = sum(t["decision"] == "Reject H0" for t in tests)
    na = sum(t["decision"] == "Not applicable" for t in tests)
    raw_rejected = sum(t["decision"] == "Reject H0" for t in raw_tests)
    raw_na = sum(t["decision"] == "Not applicable" for t in raw_tests)

    lines = [
        "# Paper values checklist" + (" (PILOT DATA, do not paste)" if pilot else ""),
        "",
        f"Generated {utc_now():%Y-%m-%d %H:%M:%S} UTC by `analyze.py`. Tick each item off as you paste it.",
        "",
        f"> {NORMALIZATION_NOTE}",
        "",
        "## Seeds",
        "",
        f"- [ ] `GENERATION_SEED` = **{config.GENERATION_SEED}** (input generation)",
        f"- [ ] `ORDER_SEED` = **{config.ORDER_SEED}** (run-order shuffle)",
        "",
        "## Repeat counts R (repeat-and-divide)",
        "",
        md_table(["Text length", "R"], [[range_label(k), f"{v:,}"] for k, v in config.REPEATS.items()], ["l", "r"]),
        "## Text source",
        "",
        f"- [ ] \\|Σ\\| = **{alice['sigma_size']}**",
        f"- [ ] Alice download date: **{alice['download_date_utc']}**",
        f"- [ ] Clean text length: **{alice['clean_char_count']:,}** characters "
        f"(raw: {alice['raw_char_count']:,})",
        f"- [ ] alice_clean.txt SHA-256: `{alice['clean_sha256']}`",
        f"- [ ] alice_raw.txt SHA-256: `{alice['raw_sha256']}`",
        "",
        "## Inputs",
        "",
        f"- [ ] inputs.jsonl SHA-256: `{read_manifest_hash()}`",
        "- [ ] Input instances: **1,710** (each shared by the 3 algorithms)",
        "",
        "## Machine specifications",
        "",
        machine_table(env, rep_env),
        "## Software and machine details (primary)",
        "",
        md_table(["Item", "Value"], env_rows(env) + [["Pinned core", pin], ["Priority raised", priority],
                                                     ["Total benchmark duration", f"{duration / 60:.1f} min"]]),
        "## Software and machine (replication)",
        "",
        md_table(["Item", "Value"], env_rows(rep_env)),
        "## Row counts",
        "",
        f"- [ ] Primary rows: **{len(df):,}** (expected {5130 if not pilot else 513:,})",
        f"- [ ] Replication rows: **{rep_rows:,}**" if rep_rows is not None else "- [ ] Replication rows: (not yet run)",
        "",
        md_table(["Algorithm", "Primary rows"], per_algo, ["l", "r"]),
        md_table(["Experiment", "Primary rows"], per_exp, ["l", "r"]),
        "## Statistics",
        "",
        f"- [ ] Tests: **{len(tests)}** (Holm family size {len(tests)}, α = {config.ALPHA})",
        "- [ ] Dependent variables: time = total time ÷ text length (ns per text character); "
        "comparisons = (prep + search comparisons) ÷ text length (comparisons per text character); "
        "memory = `memory_bytes` (bytes)",
        f"- [ ] Rejected after Holm: **{rejected}**; not applicable: **{na}**",
        f"- [ ] Appendix (unnormalized time and comparisons, separate Holm family of {len(raw_tests)}): "
        f"rejected **{raw_rejected}**; not applicable: **{raw_na}**",
        "- [ ] Effect-size labels: Cohen's d small 0.2 / medium 0.5 / large 0.8 (Cohen, 1988); "
        "η² small 0.01 / medium 0.06 / large 0.14 (Cohen, 1988); Cliff's δ negligible < 0.11 / small < 0.28 / "
        "medium < 0.43 / large otherwise; ε² = H/(N − 1) small 0.01 / medium 0.06 / large 0.14",
        "",
        "## Memory definitions",
        "",
        config.MEMORY_DEFINITIONS,
        "",
        "## Comparison-counting definitions",
        "",
        config.COMPARISON_DEFINITIONS,
        "",
    ]
    (out_dir / "paper_values.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pilot", action="store_true", help="analyse results/primary/pilot/ instead")
    args = parser.parse_args()

    out_dir = results_dir("primary", args.pilot)
    csv_path = out_dir / "raw_runs.csv"
    if not csv_path.exists():
        sys.exit(f"{csv_path} not found. Run run_benchmark.py first.")
    df = add_per_char_columns(read_raw_runs(csv_path))
    sigma_size = json.loads(config.ALICE_META_JSON.read_text(encoding="utf-8"))["sigma_size"]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)  # e.g. Shapiro on tiny pilot groups
        tests = run_all_tests(df, args.pilot)
        raw_tests = run_all_tests(df, args.pilot, RAW_DVS)
    figures = make_figures(df, out_dir / "figures")

    title = "# Statistics report (primary machine)" + (" — PILOT DATA" if args.pilot else "")
    parts = [title, "", f"> {NORMALIZATION_NOTE}", ""]
    if args.pilot:
        parts += ["> ⚠️ **Pilot data (3 runs per condition).** These numbers only prove the pipeline works; "
                  "they are not results.", ""]
    rejected = sum(t["decision"] == "Reject H0" for t in tests)
    raw_rejected = sum(t["decision"] == "Reject H0" for t in raw_tests)
    parts += [
        f"Generated {utc_now():%Y-%m-%d %H:%M:%S} UTC by `analyze.py` from `raw_runs.csv` ({len(df):,} rows).",
        "",
        "## Method",
        "",
        f"- α = {config.ALPHA}. Every test is run per algorithm and per text-length level.",
        "- Shapiro-Wilk on every group (skipped for a zero-variance group, which then forces the "
        "non-parametric test).",
        "- Two groups: Welch's t-test if every group is normal, otherwise Mann-Whitney U (two-sided). "
        "Four groups: one-way ANOVA if every group is normal, otherwise Kruskal-Wallis.",
        "- Effect sizes: Cohen's d (pooled SD; small 0.2, medium 0.5, large 0.8; Cohen, 1988), "
        "Cliff's δ (< 0.11 negligible, < 0.28 small, < 0.43 medium, else large), η² (small 0.01, "
        "medium 0.06, large 0.14; Cohen, 1988) and ε² = H/(N − 1) (small 0.01, medium 0.06, large 0.14). "
        "Values below the small threshold are labelled negligible. The sign of d and δ is "
        "first group minus second group.",
        f"- Holm's correction across all {len(tests)} tests as one family. Tests that are not applicable "
        "(no variance at all) stay in the family, are ranked last (as if p = 1) and are never rejected.",
        "- Time = total time (prep + search) per call ÷ text length n, in ns per text character; "
        "comparisons = (prep + search comparisons) ÷ n, in comparisons per text character; "
        "memory = `memory_bytes` in bytes, not normalized (structure only; it does not depend on the text; "
        "exact definitions per algorithm in the descriptive section). `memory_retained_raw_bytes` and "
        "`memory_peak_bytes` are descriptive only.",
        "- Descriptive-only section: the core-grid time and comparison tables are also per text character "
        "(raw-unit versions in the appendix). The σ/(σ − 1) table is per alignment, the positive control "
        "uses fixed inputs and shows its own per-character columns, and the memory tables are in bytes.",
        "",
        "## Decisions summary",
        "",
        f"**{rejected} of {len(tests)} null hypotheses rejected after Holm's correction.**",
        "",
        decisions_summary(tests),
    ]
    for hyp_id, factor, dv, algorithms in HYPOTHESES:
        parts.append(hypothesis_section(hyp_id, factor, dv, algorithms, tests))
    parts.append(descriptive_section(df, sigma_size))

    parts += ["## Figures", "", "Bars show the mean; error bars show ± 1 SD. Colours are colour-blind safe "
              "(Okabe-Ito) and hatched for greyscale printing.", ""]
    for fig_id, view, dv, filename in figures:
        parts += [f"### Figure {fig_id}. {view['title']}: {DVS[dv][1]} ({DVS[dv][4]})", "",
                  f"![Figure {fig_id}](figures/{filename})", ""]

    parts += [
        "## Appendix: unnormalized results",
        "",
        "The first analysis, before normalization: time = total time per call (µs) and comparisons = "
        "prep + search comparisons, not divided by text length; memory = `memory_bytes` (bytes), as in the "
        "main analysis. Same groups, pooling, test selection and effect sizes, with its own Holm correction "
        f"across all {len(raw_tests)} tests. The memory tests have the same raw p-values as in the main "
        "analysis, but their Holm-adjusted p-values can differ because the other tests in the family differ.",
        "",
        "### Decisions summary (unnormalized)",
        "",
        f"**{raw_rejected} of {len(raw_tests)} null hypotheses rejected after Holm's correction.**",
        "",
        decisions_summary(raw_tests),
    ]
    for hyp_id, factor, dv, algorithms in HYPOTHESES:
        parts.append(hypothesis_section(hyp_id, factor, dv, algorithms, raw_tests, dvs=RAW_DVS,
                                        heading="###", tag=" (unnormalized)", figure_ref=False))
    parts += ["### Descriptive core-grid tables (unnormalized)", "",
              "Raw-unit versions of the core-grid descriptive tables (not divided by text length).", ""]
    parts += core_grid_tables(df, normalized=False, heading="####", tag=" (unnormalized)")

    (out_dir / "stats_report.md").write_text("\n".join(parts), encoding="utf-8", newline="\n")
    write_paper_values(out_dir, df, tests, raw_tests, args.pilot)
    print(f"{len(tests)} tests, {rejected} rejected after Holm (normalized). "
          f"Appendix (unnormalized): {raw_rejected} rejected.")
    print(f"Wrote {(out_dir / 'stats_report.md').relative_to(config.ROOT)}, "
          f"{(out_dir / 'paper_values.md').relative_to(config.ROOT)} and {len(figures)} figures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
