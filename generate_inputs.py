"""Build every benchmark input once, save it, and record its SHA-256.

One *input instance* = one text + its queries. It is shared by all three
algorithms (the pairing rule), so there are 5,130 / 3 = 1,710 instances:

    core grid         2 text types x 3 text ranges x 3 query ranges x 2 query counts x 30 runs = 1,080
    query pattern     2 styles x 3 text ranges x 30 runs                                        =   180
    alphabet size     4 alphabets x 3 text ranges x 30 runs                                     =   360
    positive control  3 text ranges x 30 runs (the same input reused for all 30)                =    90

Everything is drawn from ONE random.Random(GENERATION_SEED) instance in a fixed
loop order, so the same seed always produces byte-identical inputs.jsonl.

Usage:
    python generate_inputs.py          # refuses to overwrite existing inputs
    python generate_inputs.py --force  # regenerate (only if you really mean it)
"""

import argparse
import json
import platform
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

import config
from src.inputs_io import sha256_bytes, sha256_file
from src.report import fmt_num, md_table, range_label


def is_ascii_letter(ch):
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z")


class InputBuilder:
    """Holds the single random generator and the bookkeeping for the manifest."""

    def __init__(self, clean_text, seed):
        self.clean_text = clean_text
        self.rng = random.Random(seed)  # dedicated instance, never the global `random`
        self.sigma = sorted(set(clean_text), key=ord)  # sorted -> deterministic order
        self.letters = [c for c in self.sigma if is_ascii_letter(c)]
        self.records = []
        self.redraws = Counter()  # (experiment, text range, query range) -> redraw count

    # -- length drawing ----------------------------------------------------
    def draw_lengths(self, experiment, text_range, query_range, num_queries):
        """Draw n and every query length; if any query is longer than the text, redraw all.

        Lengths are uniform integers, inclusive at both ends.
        """
        n_lo, n_hi = config.TEXT_LENGTH_RANGES[text_range]
        m_lo, m_hi = config.QUERY_LENGTH_RANGES[query_range]
        while True:
            n = self.rng.randint(n_lo, n_hi)
            ms = [self.rng.randint(m_lo, m_hi) for _ in range(num_queries)]
            if max(ms) <= n:
                return n, ms
            self.redraws[(experiment, text_range, query_range)] += 1

    # -- text and query makers --------------------------------------------
    def random_text(self, n, alphabet):
        """Each character drawn uniformly at random from `alphabet`."""
        return "".join([self.rng.choice(alphabet) for _ in range(n)])

    def narrative_text(self, n):
        """A contiguous slice of Alice starting at a uniformly random position."""
        start = self.rng.randint(0, len(self.clean_text) - n)
        return self.clean_text[start : start + n], start

    def substring_query(self, text, m):
        """A random substring of the text, so the query occurs at least once."""
        start = self.rng.randint(0, len(text) - m)
        return text[start : start + m]

    def distinct_query(self, m):
        """m letters, all different (e.g. 'ABCDE')."""
        return "".join(self.rng.sample(self.letters, m))

    def repeating_query(self, m):
        """A 1-3 letter unit (letters may repeat), repeated then truncated to m."""
        unit_len = self.rng.randint(*config.REPEAT_UNIT_LENGTH)
        unit = "".join([self.rng.choice(self.letters) for _ in range(unit_len)])
        return (unit * (m // unit_len + 1))[:m]

    # -- records -------------------------------------------------------------
    def add(self, experiment, run_id, text, queries, *, text_type=None, alphabet_size=None,
            text_length_range, query_length_range, query_style=None, narrative_start=None):
        record = {
            "input_id": len(self.records) + 1,
            "experiment": experiment,
            "text_type": text_type,
            "alphabet_size": alphabet_size,
            "text_length_range": text_length_range,
            "query_length_range": query_length_range,
            "query_style": query_style,
            "num_queries": len(queries),
            "run_id": run_id,
            "text_length": len(text),
            "query_lengths": [len(q) for q in queries],
            "has_duplicate_queries": len(set(queries)) < len(queries),
            "narrative_start": narrative_start,
            "text": text,
            "queries": queries,
        }
        self.records.append(record)

    # -- the four experiments ------------------------------------------------
    def build_core(self):
        for text_type in config.TEXT_TYPES:
            for text_range in config.TEXT_LENGTH_RANGES:
                for query_range in config.QUERY_LENGTH_RANGES:
                    for k in config.NUM_QUERIES_LEVELS:
                        for run_id in range(1, config.NUM_RUNS + 1):
                            n, ms = self.draw_lengths("core", text_range, query_range, k)
                            start = None
                            if text_type == "random":
                                text = self.random_text(n, self.sigma)
                            else:
                                text, start = self.narrative_text(n)
                            queries = [self.substring_query(text, m) for m in ms]
                            self.add("core", run_id, text, queries, text_type=text_type,
                                     text_length_range=text_range, query_length_range=query_range,
                                     narrative_start=start)

    def build_query_pattern(self):
        query_range = config.FIXED_QUERY_RANGE
        for style in config.QUERY_STYLES:
            for text_range in config.TEXT_LENGTH_RANGES:
                for run_id in range(1, config.NUM_RUNS + 1):
                    n, (m,) = self.draw_lengths("query_pattern", text_range, query_range, 1)
                    text, start = self.narrative_text(n)
                    # The query is generated independently of the text.
                    query = self.distinct_query(m) if style == "distinct" else self.repeating_query(m)
                    self.add("query_pattern", run_id, text, [query], text_type="narrative",
                             text_length_range=text_range, query_length_range=query_range,
                             query_style=style, narrative_start=start)

    def build_alphabet(self):
        query_range = config.FIXED_QUERY_RANGE
        for size, chars in config.ALPHABETS.items():
            alphabet = self.sigma if chars is None else list(chars)
            for text_range in config.TEXT_LENGTH_RANGES:
                for run_id in range(1, config.NUM_RUNS + 1):
                    n, (m,) = self.draw_lengths("alphabet", text_range, query_range, 1)
                    text = self.random_text(n, alphabet)
                    query = self.substring_query(text, m)
                    self.add("alphabet", run_id, text, [query], text_type="random",
                             alphabet_size=size, text_length_range=text_range,
                             query_length_range=query_range)

    def build_positive_control(self):
        query_range = config.FIXED_QUERY_RANGE
        for text_range in config.TEXT_LENGTH_RANGES:
            # Drawn ONCE per text-length level, then reused for all 30 runs.
            n, (m,) = self.draw_lengths("positive_control", text_range, query_range, 1)
            text = config.CONTROL_TEXT_CHAR * n
            query = config.CONTROL_TEXT_CHAR * (m - 1) + config.CONTROL_LAST_QUERY_CHAR
            for run_id in range(1, config.NUM_RUNS + 1):
                self.add("positive_control", run_id, text, [query],
                         text_length_range=text_range, query_length_range=query_range)

    def build_all(self):
        self.build_core()
        self.build_query_pattern()
        self.build_alphabet()
        self.build_positive_control()
        return self.records


def build_inputs(clean_text, seed=config.GENERATION_SEED):
    """Return (records, builder). Pure function of (clean_text, seed)."""
    builder = InputBuilder(clean_text, seed)
    return builder.build_all(), builder


def serialize(records):
    """One compact JSON object per line, LF line endings, ASCII only (\\u escapes).

    ASCII-only output means the bytes (and therefore the hash) cannot be changed
    by an editor or OS that guesses a different text encoding.
    """
    lines = [json.dumps(r, ensure_ascii=True, separators=(",", ":")) for r in records]
    return ("\n".join(lines) + "\n").encode("ascii")


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
def length_sanity_rows(records):
    """Min / mean / max of text and query lengths, per experiment and range."""
    text_lengths = defaultdict(list)
    query_lengths = defaultdict(list)
    for r in records:
        text_lengths[(r["experiment"], r["text_length_range"])].append(r["text_length"])
        query_lengths[(r["experiment"], r["query_length_range"])].extend(r["query_lengths"])

    def rows(groups, ranges):
        out = []
        for exp in config.EXPERIMENTS:
            for rng_key, (lo, hi) in ranges.items():
                vals = groups.get((exp, rng_key))
                if not vals:
                    continue
                ok = "yes" if lo <= min(vals) and max(vals) <= hi else "**NO**"
                out.append([exp, range_label(rng_key), len(vals), min(vals),
                            fmt_num(sum(vals) / len(vals), 1), max(vals), ok])
        return out

    return rows(text_lengths, config.TEXT_LENGTH_RANGES), rows(query_lengths, config.QUERY_LENGTH_RANGES)


def write_manifest(records, builder, inputs_hash, alice_meta):
    counts = Counter(r["experiment"] for r in records)
    dupes = sum(1 for r in records if r["num_queries"] > 1 and r["has_duplicate_queries"])
    multi = sum(1 for r in records if r["num_queries"] > 1)
    text_rows, query_rows = length_sanity_rows(records)
    redraw_rows = [
        [exp, range_label(tr), range_label(qr), count]
        for (exp, tr, qr), count in sorted(builder.redraws.items())
    ] or [["(none)", "", "", 0]]

    count_rows = [[exp, f"{counts.get(exp, 0):,}", f"{counts.get(exp, 0) * len(config.ALGORITHMS):,}"]
                  for exp in config.EXPERIMENTS]
    count_rows.append(["**Total**", f"**{len(records):,}**", f"**{len(records) * len(config.ALGORITHMS):,}**"])

    lines = [
        "# Input manifest",
        "",
        "Generated by `generate_inputs.py`. Do not edit `inputs.jsonl` by hand: "
        "`run_benchmark.py` checks its hash against the line below and refuses to run if it differs.",
        "",
        f"**SHA-256 of inputs.jsonl:** `{inputs_hash}`",
        "",
        md_table(
            ["Item", "Value"],
            [
                ["Generated (UTC)", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")],
                ["GENERATION_SEED", f"`{config.GENERATION_SEED}`"],
                ["ORDER_SEED (job order, used by run_benchmark.py)", f"`{config.ORDER_SEED}`"],
                ["Python version", platform.python_version()],
                ["Runs per condition", config.NUM_RUNS],
                ["Source text", "`data/alice_clean.txt`"],
                ["alice_clean.txt SHA-256", f"`{alice_meta['clean_sha256']}`"],
                ["\\|Σ\\| (full Alice alphabet)", len(builder.sigma)],
                ["Letters available for query-pattern queries", len(builder.letters)],
            ],
        ),
        "## Input instances per experiment",
        "",
        "Each instance is shared by all three algorithms (pairing rule).",
        "",
        md_table(["Experiment", "Input instances", "Benchmark rows (× 3 algorithms)"], count_rows, ["l", "r", "r"]),
        "## Redraws (query longer than text)",
        "",
        "Rule: if any drawn query length is greater than the drawn text length, the text length "
        "and all query lengths of that instance are drawn again.",
        "",
        f"Total redraws: **{sum(builder.redraws.values())}**",
        "",
        md_table(["Experiment", "Text range", "Query range", "Redraws"], redraw_rows, ["l", "l", "l", "r"]),
        "## Duplicate queries",
        "",
        f"{dupes} of {multi} five-query instances contain at least one repeated query "
        "(allowed by the design; recorded per instance as `has_duplicate_queries`).",
        "",
        "## Sanity check: text lengths",
        "",
        md_table(["Experiment", "Range", "N", "Min", "Mean", "Max", "Within range?"], text_rows,
                 ["l", "l", "r", "r", "r", "r", "c"]),
        "## Sanity check: query lengths (every individual query)",
        "",
        md_table(["Experiment", "Range", "N", "Min", "Mean", "Max", "Within range?"], query_rows,
                 ["l", "l", "r", "r", "r", "r", "c"]),
        "The positive control draws n and m once per text-length level, so its 30 rows per level are identical.",
        "",
    ]
    config.MANIFEST_FILE.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="overwrite existing inputs")
    args = parser.parse_args()

    if config.INPUTS_FILE.exists() and not args.force:
        print(f"{config.INPUTS_FILE.relative_to(config.ROOT)} already exists; refusing to overwrite.\n"
              "Pass --force only if you really want to regenerate the inputs.", file=sys.stderr)
        return 1
    if not config.ALICE_CLEAN.exists():
        print("data/alice_clean.txt is missing. Run `python prepare_alice.py` first.", file=sys.stderr)
        return 1

    alice_meta = json.loads(config.ALICE_META_JSON.read_text(encoding="utf-8"))
    if sha256_file(config.ALICE_CLEAN) != alice_meta["clean_sha256"]:
        print("alice_clean.txt does not match the hash in alice_meta.json. Re-run prepare_alice.py.",
              file=sys.stderr)
        return 1
    clean_text = config.ALICE_CLEAN.read_text(encoding="utf-8")

    records, builder = build_inputs(clean_text, config.GENERATION_SEED)
    data = serialize(records)
    config.INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    config.INPUTS_FILE.write_bytes(data)
    inputs_hash = sha256_bytes(data)
    write_manifest(records, builder, inputs_hash, alice_meta)

    print(f"Wrote {len(records):,} input instances to {config.INPUTS_FILE.relative_to(config.ROOT)}")
    print(f"SHA-256: {inputs_hash}")
    print(f"Redraws: {sum(builder.redraws.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
