"""Small helpers for writing Markdown reports.

All human-readable output of the project is Markdown, so the formatting rules
(units, number of decimals, escaping) live here and are shared by every script.
"""

import math
import unicodedata

import numpy as np

MICRO = "µs"


def range_label(range_key):
    """'10-100' -> '10–100' (en dash, as in the paper)."""
    return str(range_key).replace("-", "–")


def md_escape(value):
    """Escape characters that would break a Markdown table cell."""
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def md_table(headers, rows, align=None):
    """Return a GitHub-flavoured Markdown table.

    align: optional list of 'l', 'r' or 'c' per column (default: left).
    Cells are used as given (call md_escape yourself for untrusted text),
    so callers can put `code`, **bold** or <br> inside cells.
    """
    align = align or ["l"] * len(headers)
    marks = {"l": "---", "r": "---:", "c": ":---:"}
    lines = [
        "| " + " | ".join(str(h) for h in headers) + " |",
        "| " + " | ".join(marks[a] for a in align) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines) + "\n"


def md_char(ch):
    """Show one character so that spaces, quotes and pipes stay visible in a table."""
    if ch == " ":
        return "␠ (space)"
    if ch == "|":
        return "`\\|`"
    if ch == "`":
        return "`` ` ``"
    if unicodedata.category(ch).startswith(("C", "Z")):  # control / other whitespace
        return f"U+{ord(ch):04X}"
    return f"`{ch}`"


def md_text(text):
    """Show an arbitrary string inside a table cell, keeping spaces visible."""
    return "`" + md_escape(text).replace("`", "'").replace(" ", "␠") + "`" if text else "(empty)"


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------
def is_missing(x):
    return x is None or (isinstance(x, float) and math.isnan(x))


def fmt_num(x, decimals=2):
    """Thousands separator, fixed decimals, '—' for missing."""
    if is_missing(x):
        return "—"
    return f"{x:,.{decimals}f}"


def fmt_int(x):
    if is_missing(x):
        return "—"
    return f"{int(round(x)):,}"


def fmt_us(seconds, decimals=2):
    """Seconds -> microseconds string."""
    if is_missing(seconds):
        return "—"
    return f"{seconds * 1e6:,.{decimals}f}"


def fmt_p(p):
    """p-values: scientific notation when tiny, otherwise 4 decimals."""
    if is_missing(p):
        return "—"
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def describe(values):
    """Mean, sample SD, median, quartiles and IQR of a 1-D sequence."""
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    n = arr.size
    if n == 0:
        nan = float("nan")
        return {"n": 0, "mean": nan, "sd": nan, "median": nan, "q1": nan, "q3": nan, "iqr": nan}
    q1, med, q3 = np.percentile(arr, [25, 50, 75])
    return {
        "n": int(n),
        "mean": float(arr.mean()),
        "sd": float(arr.std(ddof=1)) if n > 1 else float("nan"),
        "median": float(med),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
    }


def stat_cell(values, scale=1.0, decimals=2):
    """'mean ± SD<br>Mdn x, IQR y' for one table cell. `scale` converts units (1e6 for µs)."""
    d = describe(values)
    if d["n"] == 0:
        return "—"
    s = {k: (v * scale if isinstance(v, float) else v) for k, v in d.items()}
    return (
        f"{fmt_num(s['mean'], decimals)} ± {fmt_num(s['sd'], decimals)}"
        f"<br>Mdn {fmt_num(s['median'], decimals)}, IQR {fmt_num(s['iqr'], decimals)}"
    )
