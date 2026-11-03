"""Reading and hashing the shared files (inputs, manifest, raw results).

Kept in one module so every script verifies hashes and parses the CSV the
same way.
"""

import hashlib
import json
import re
from pathlib import Path

import config

MANIFEST_HASH_PATTERN = re.compile(r"SHA-256 of inputs\.jsonl:\*\*\s*`([0-9a-f]{64})`")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    """SHA-256 of a file's exact bytes (read in chunks so big files are fine)."""
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_manifest_hash(manifest_path=config.MANIFEST_FILE):
    """Pull the recorded inputs.jsonl hash out of inputs/manifest.md."""
    text = Path(manifest_path).read_text(encoding="utf-8")
    found = MANIFEST_HASH_PATTERN.search(text)
    if not found:
        raise ValueError(f"Could not find the inputs.jsonl SHA-256 line in {manifest_path}")
    return found.group(1)


def verify_inputs_hash(inputs_path=config.INPUTS_FILE, manifest_path=config.MANIFEST_FILE):
    """Return (ok, actual_hash, expected_hash)."""
    expected = read_manifest_hash(manifest_path)
    actual = sha256_file(inputs_path)
    return actual == expected, actual, expected


def load_inputs(inputs_path=config.INPUTS_FILE):
    """Read inputs.jsonl into a list of dicts (one per input instance)."""
    records = []
    with Path(inputs_path).open("r", encoding="utf-8", newline="") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def results_dir(machine, pilot=False):
    out = config.RESULTS_DIR / machine
    return out / "pilot" if pilot else out


def read_raw_runs(csv_path):
    """Load raw_runs.csv as a pandas DataFrame with sensible types.

    Categorical columns stay strings (alphabet_size mixes '2' and 'full');
    blank cells become NaN. Adds a `total_comparisons` column (prep + search),
    which is the 'comparisons' dependent variable used in the paper.
    """
    import pandas as pd

    text_cols = [
        "experiment", "algorithm", "text_type", "alphabet_size", "text_length_range",
        "query_length_range", "query_lengths", "query_style", "machine",
    ]
    df = pd.read_csv(csv_path, dtype={c: "string" for c in text_cols}, keep_default_na=True)
    for c in text_cols:
        df[c] = df[c].astype(object).where(df[c].notna(), None)
    df["total_comparisons"] = df["prep_comparisons"] + df["search_comparisons"]
    return df
