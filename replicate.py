"""Compare the primary and replication machines.

Times are expected to differ between machines; comparison counts and match
counts are NOT (they depend only on the inputs and the code), so any
difference there is a bug.

Writes results/replication_report.md with:
  1. input hashes and row counts
  2. comparison / match counts per (input_id, algorithm): must be identical
  3. Table 5.8-style winners per condition group (fastest median total time)
  4. ratio of median times between machines
  5. a warning if the Python versions differ

Usage:
    python replicate.py
    python replicate.py --pilot    # compare the two pilot runs instead
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

import config
from run_benchmark import number_of_conditions
from src.inputs_io import read_manifest_hash, read_raw_runs, results_dir
from src.measure import utc_now
from src.report import fmt_num, md_escape, md_table
from src.summaries import condition_label, group_key, sort_key

COUNT_COLUMNS = ["prep_comparisons", "search_comparisons", "search_failure_steps", "num_matches"]


def load_side(directory):
    directory = Path(directory)
    csv_path = directory / "raw_runs.csv"
    if not csv_path.exists():
        sys.exit(f"{csv_path} not found.")
    env, hashes = None, set()
    if (directory / "environment.json").exists():
        env = json.loads((directory / "environment.json").read_text(encoding="utf-8"))
    if (directory / "sessions.jsonl").exists():
        for line in (directory / "sessions.jsonl").read_text(encoding="utf-8").splitlines():
            if line:
                hashes.add(json.loads(line)["input_hash"])
    return read_raw_runs(csv_path), env, hashes


def by_job(df):
    """(input_id, algorithm) -> row dict."""
    return {(int(r["input_id"]), r["algorithm"]): r for r in df.to_dict("records")}


def same_value(a, b):
    a_missing = a is None or (isinstance(a, float) and np.isnan(a))
    b_missing = b is None or (isinstance(b, float) and np.isnan(b))
    if a_missing or b_missing:
        return a_missing and b_missing
    return float(a) == float(b)


def condition_groups(df):
    """condition group (all factors except algorithm) -> algorithm -> list of total times."""
    groups = {}
    for r in df.to_dict("records"):
        groups.setdefault(group_key(r, include_algorithm=False), {}).setdefault(r["algorithm"], []).append(
            r["total_time"])
    return groups


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pilot", action="store_true", help="compare results/<machine>/pilot/")
    parser.add_argument("--primary", help="override the primary results folder")
    parser.add_argument("--replication", help="override the replication results folder")
    parser.add_argument("--out", help="override the output file")
    args = parser.parse_args()

    p_dir = Path(args.primary) if args.primary else results_dir("primary", args.pilot)
    r_dir = Path(args.replication) if args.replication else results_dir("replication", args.pilot)
    out = Path(args.out) if args.out else config.RESULTS_DIR / (
        "replication_report_pilot.md" if args.pilot else "replication_report.md")

    p_df, p_env, p_hashes = load_side(p_dir)
    r_df, r_env, r_hashes = load_side(r_dir)
    manifest_hash = read_manifest_hash()
    parts = [
        "# Replication report" + (" (PILOT)" if args.pilot else ""),
        "",
        f"Generated {utc_now():%Y-%m-%d %H:%M:%S} UTC by `replicate.py`.",
        "",
    ]

    # 5. Python version warning (shown first so it cannot be missed)
    p_py = p_env["python_version"] if p_env else "unknown"
    r_py = r_env["python_version"] if r_env else "unknown"
    if p_py != r_py:
        parts += [f"> ⚠️ **Python versions differ:** primary {p_py}, replication {r_py}. Timings and "
                  "memory may not be comparable; comparison counts should still be identical.", ""]

    # 1. Hashes and row counts
    expected_rows = number_of_conditions() * (config.PILOT_RUNS if args.pilot else config.NUM_RUNS)
    hash_ok = p_hashes == {manifest_hash} and r_hashes == {manifest_hash}
    rows_ok = len(p_df) == len(r_df) == expected_rows
    p_jobs, r_jobs = by_job(p_df), by_job(r_df)
    jobs_ok = set(p_jobs) == set(r_jobs)
    parts += [
        "## 1. Inputs and row counts",
        "",
        md_table(["Check", "Primary", "Replication", "Result"], [
            ["Input hash used", "<br>".join(f"`{h}`" for h in sorted(p_hashes)) or "—",
             "<br>".join(f"`{h}`" for h in sorted(r_hashes)) or "—", "✅ match" if hash_ok else "❌ MISMATCH"],
            ["Row count", f"{len(p_df):,}", f"{len(r_df):,}",
             f"{'✅' if rows_ok else '❌'} expected {expected_rows:,}"],
            ["Same set of (input_id, algorithm) jobs", "", "", "✅ yes" if jobs_ok else "❌ NO"],
            ["Python", p_py, r_py, "✅ same" if p_py == r_py else "⚠️ differs"],
            ["OS", md_escape(p_env["os"]) if p_env else "—", md_escape(r_env["os"]) if r_env else "—", ""],
            ["CPU", md_escape(p_env["cpu_model"]) if p_env else "—",
             md_escape(r_env["cpu_model"]) if r_env else "—", ""],
        ]),
        f"Manifest hash: `{manifest_hash}`",
        "",
    ]

    # 2. Counts identical per job
    mismatches = []
    memory_diffs = 0
    shared = sorted(set(p_jobs) & set(r_jobs))
    for job in shared:
        a, b = p_jobs[job], r_jobs[job]
        for col in COUNT_COLUMNS:
            if not same_value(a[col], b[col]):
                mismatches.append([job[0], config.ALGORITHM_LABELS[job[1]], col, a[col], b[col]])
        memory_diffs += not same_value(a["memory_bytes"], b["memory_bytes"])
    parts += [
        "## 2. Comparison and match counts per (input_id, algorithm)",
        "",
        f"Columns compared: {', '.join(f'`{c}`' for c in COUNT_COLUMNS)} over {len(shared):,} jobs.",
        "",
        f"**{'✅ All identical.' if not mismatches else f'❌ {len(mismatches)} MISMATCH(ES): this is a bug.'}**",
        "",
    ]
    if mismatches:
        parts += [md_table(["input_id", "Algorithm", "Column", "Primary", "Replication"], mismatches[:200]), ""]
    parts += [f"For information: `memory_bytes` differs in {memory_diffs:,} of {len(shared):,} jobs "
              "(expected 0 with the same Python version, since object sizes are deterministic).", ""]

    # 3. Table 5.8 winners and 4. ratios
    p_groups, r_groups = condition_groups(p_df), condition_groups(r_df)
    # Comparisons identical per condition group
    mismatch_jobs = {(m[0], m[1]) for m in mismatches}
    group_of_input = {int(r["input_id"]): group_key(r, include_algorithm=False) for r in p_df.to_dict("records")}
    bad_groups = {group_of_input[i] for i, _ in mismatch_jobs if i in group_of_input}

    winner_rows, ratio_rows = [], []
    same_count = 0
    all_ratios = {a: [] for a in config.ALGORITHMS}
    for key in sorted(set(p_groups) & set(r_groups), key=sort_key):
        p_med = {a: float(np.median(v)) for a, v in p_groups[key].items()}
        r_med = {a: float(np.median(v)) for a, v in r_groups[key].items()}
        p_win = min(p_med, key=p_med.get)
        r_win = min(r_med, key=r_med.get)
        same = p_win == r_win
        same_count += same
        winner_rows.append([condition_label(key), config.ALGORITHM_LABELS[p_win], config.ALGORITHM_LABELS[r_win],
                            "✅ yes" if same else "❌ no", "❌ no" if key in bad_groups else "✅ yes"])
        ratios = []
        for a in config.ALGORITHMS:
            ratio = r_med[a] / p_med[a] if a in p_med and a in r_med and p_med[a] else float("nan")
            all_ratios[a].append(ratio)
            ratios.append(fmt_num(ratio, 2))
        ratio_rows.append([condition_label(key), *ratios])
    n_groups = len(winner_rows)
    parts += [
        "## 3. Winners per condition (Table 5.8)",
        "",
        "Winner = the fastest algorithm by median total time in that condition group. "
        f"Same winner on both machines in **{same_count} of {n_groups}** condition groups.",
        "",
        md_table(["Condition", "Winner (primary)", "Winner (replication)", "Same direction?",
                  "Comparisons identical?"], winner_rows, ["l", "l", "l", "c", "c"]),
        "## 4. Ratio of median total times (replication ÷ primary)",
        "",
        "Above 1 means the replication machine was slower.",
        "",
        md_table(["Algorithm", "Median ratio over condition groups", "Min", "Max"], [
            [config.ALGORITHM_LABELS[a], fmt_num(float(np.nanmedian(v)), 2), fmt_num(float(np.nanmin(v)), 2),
             fmt_num(float(np.nanmax(v)), 2)] for a, v in all_ratios.items() if v], ["l", "r", "r", "r"]),
        md_table(["Condition", *[config.ALGORITHM_LABELS[a] for a in config.ALGORITHMS]], ratio_rows,
                 ["l", "r", "r", "r"]),
    ]

    out.write_text("\n".join(parts), encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(config.ROOT) if out.is_relative_to(config.ROOT) else out}")
    print(f"Count mismatches: {len(mismatches)}; same winner in {same_count}/{n_groups} condition groups.")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
