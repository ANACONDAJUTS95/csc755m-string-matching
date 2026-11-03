"""Correctness tests for the three algorithms and the input generator.

Only this file may use str.find as a reference: the algorithms themselves are
hand-written and never call str.find, `in`, or re for matching.
"""

import random
import sys

import pytest

import config
from src import ALGORITHM_MODULES, aho_corasick, kmp, naive

ALL_MODULES = list(ALGORITHM_MODULES.values())


def reference_matches(text, queries):
    """Ground truth: every (start, query_index), overlaps included, via str.find."""
    found = []
    for qi, q in enumerate(queries):
        pos = text.find(q)
        while pos != -1:
            found.append((pos, qi))
            pos = text.find(q, pos + 1)  # +1 so overlapping matches are found
    return sorted(found)


def all_six_versions(text, queries):
    """Matches from the 3 clean + 3 counted versions, keyed by a readable name."""
    results = {}
    for module in ALL_MODULES:
        results[f"{module.NAME}/clean"] = module.find_all(text, queries)
        results[f"{module.NAME}/counted"] = module.find_all_counted(text, queries)["matches"]
    return results


# ---------------------------------------------------------------------------
# 1. 2,000 random cases against the str.find reference
# ---------------------------------------------------------------------------
ALPHABETS = ["a", "ab", "abc", "abcd", "acgt", "abcdefghijklmnopqrstuvwxyz", "aA .,’"]


def random_case(rng):
    alphabet = rng.choice(ALPHABETS)
    n = rng.randint(0, 80)
    text = "".join(rng.choice(alphabet) for _ in range(n))
    queries = []
    for _ in range(rng.randint(1, 5)):
        m = rng.randint(1, 8)
        if text and m <= n and rng.random() < 0.6:
            start = rng.randint(0, n - m)
            queries.append(text[start : start + m])  # guaranteed hit
        else:
            queries.append("".join(rng.choice(alphabet) for _ in range(m)))  # maybe no hit
    return text, queries


def test_2000_random_cases_match_reference():
    rng = random.Random(12345)
    for case in range(2000):
        text, queries = random_case(rng)
        expected = reference_matches(text, queries)
        for name, got in all_six_versions(text, queries).items():
            assert got == expected, f"case {case}: {name} wrong for text={text!r} queries={queries!r}"


@pytest.mark.parametrize(
    "text, queries",
    [
        ("aaaa", ["aa"]),  # overlapping matches: 0, 1, 2
        ("aaaaa", ["a", "aa", "aaa"]),
        ("abababab", ["abab", "bab"]),
        ("abcdef", ["xyz"]),  # empty result
        ("", ["a"]),  # empty text
        ("ab", ["abc"]),  # query longer than text
        ("ushers", ["he", "she", "his", "hers"]),
        ("abcabc", ["abc", "abc"]),  # duplicate queries are reported for each index
    ],
)
def test_edge_cases_match_reference(text, queries):
    expected = reference_matches(text, queries)
    for name, got in all_six_versions(text, queries).items():
        assert got == expected, name


# ---------------------------------------------------------------------------
# 2. KMP LPS tables
# ---------------------------------------------------------------------------
def test_kmp_lps_ababa():
    assert kmp.build_lps("ABABA") == [0, 0, 1, 2, 3]
    assert kmp.build_lps_counted("ABABA")[0] == [0, 0, 1, 2, 3]


def test_kmp_lps_aaaa():
    assert kmp.build_lps("AAAA") == [0, 1, 2, 3]
    assert kmp.build_lps_counted("AAAA")[0] == [0, 1, 2, 3]


# ---------------------------------------------------------------------------
# 3. Aho & Corasick (1975) example
# ---------------------------------------------------------------------------
def test_aho_corasick_ushers():
    keywords = ["he", "she", "his", "hers"]
    # she@1 (index 1), he@2 (index 0), hers@2 (index 3)
    expected = [(1, 1), (2, 0), (2, 3)]
    assert aho_corasick.find_all("ushers", keywords) == expected
    assert aho_corasick.find_all_counted("ushers", keywords)["matches"] == expected


def test_aho_corasick_search_attempts_equal_n_plus_failure_steps():
    """Each text character costs 1 attempt, plus 1 extra attempt per failure step."""
    rng = random.Random(7)
    for _ in range(300):
        text, queries = random_case(rng)
        r = aho_corasick.find_all_counted(text, queries)
        assert r["search_comparisons"] == len(text) + r["search_failure_steps"]


# ---------------------------------------------------------------------------
# 4. Positive control
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("n, m", [(10, 5), (57, 7), (100, 10), (999, 6), (5000, 9)])
def test_positive_control_counts(n, m):
    text = "a" * n
    query = "a" * (m - 1) + "b"
    nv = naive.find_all_counted(text, [query])
    assert nv["search_comparisons"] == (n - m + 1) * m
    assert nv["prep_comparisons"] == 0
    assert nv["matches"] == []
    k = kmp.find_all_counted(text, [query])
    assert k["search_comparisons"] <= 2 * n
    assert k["matches"] == []
    assert aho_corasick.find_all_counted(text, [query])["matches"] == []


def test_kmp_search_never_exceeds_2n():
    rng = random.Random(99)
    for _ in range(500):
        text, queries = random_case(rng)
        for q in queries:
            assert kmp.find_all_counted(text, [q])["search_comparisons"] <= 2 * len(text)


# ---------------------------------------------------------------------------
# 5. Naive: hand-checked counts (no repeated partial matches)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "text, pattern, expected_comparisons, expected_matches",
    [
        # alignments 0..3: a|c b|c (c=c,d=d) d|c  -> 1 + 1 + 2 + 1 = 5
        ("abcde", "cd", 5, [(2, 0)]),
        # 4 alignments, each fails on the first character -> 4
        ("abcdef", "xyz", 4, []),
        # 9 alignments; 8 fail on the first char, i=6 matches 'wor' fully -> 8 + 3 = 11
        ("hello world", "wor", 11, [(6, 0)]),
    ],
)
def test_naive_hand_checked(text, pattern, expected_comparisons, expected_matches):
    r = naive.find_all_counted(text, [pattern])
    assert r["search_comparisons"] == expected_comparisons
    assert r["prep_comparisons"] == 0
    assert r["matches"] == expected_matches


# ---------------------------------------------------------------------------
# 6. Clean and counted versions agree
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("module", ALL_MODULES, ids=lambda m: m.NAME)
def test_clean_and_counted_agree(module):
    rng = random.Random(2024)
    for _ in range(300):
        text, queries = random_case(rng)
        assert module.find_all(text, queries) == module.find_all_counted(text, queries)["matches"]


# ---------------------------------------------------------------------------
# 7. Input generation is deterministic
# ---------------------------------------------------------------------------
def test_generate_inputs_is_deterministic():
    if not config.ALICE_CLEAN.exists():
        pytest.skip("data/alice_clean.txt missing; run prepare_alice.py first")
    from generate_inputs import build_inputs, serialize
    from src.inputs_io import sha256_bytes

    clean = config.ALICE_CLEAN.read_text(encoding="utf-8")
    records_a, _ = build_inputs(clean, config.GENERATION_SEED)
    records_b, _ = build_inputs(clean, config.GENERATION_SEED)
    assert sha256_bytes(serialize(records_a)) == sha256_bytes(serialize(records_b))

    # The design's instance counts.
    assert len(records_a) == 1710
    counts = {}
    for r in records_a:
        counts[r["experiment"]] = counts.get(r["experiment"], 0) + 1
    assert counts == {"core": 1080, "query_pattern": 180, "alphabet": 360, "positive_control": 90}

    # Every substring-style query really occurs; lengths stay in range.
    for r in records_a:
        lo, hi = config.TEXT_LENGTH_RANGES[r["text_length_range"]]
        assert lo <= r["text_length"] <= hi
        qlo, qhi = config.QUERY_LENGTH_RANGES[r["query_length_range"]]
        assert all(qlo <= m <= qhi for m in r["query_lengths"])
        if r["experiment"] in ("core", "alphabet"):
            assert all(q in r["text"] for q in r["queries"])  # `in` is fine in tests

    # A different seed gives different inputs.
    records_c, _ = build_inputs(clean, config.GENERATION_SEED + 1)
    assert sha256_bytes(serialize(records_c)) != sha256_bytes(serialize(records_a))


# ---------------------------------------------------------------------------
# 8. Memory pass
# ---------------------------------------------------------------------------
def test_memory_naive_is_zero_and_harness_overhead_removed():
    from src.measure import _traced_build, measure_memory

    assert measure_memory(naive, ["abc"]) == (0, 0, 0)
    # An empty build measures 0 once the harness overhead is subtracted.
    oh = _traced_build(lambda: None)
    empty = _traced_build(lambda: None)
    assert (empty[0] - oh[0], empty[1] - oh[1]) == (0, 0)


MEMORY_CASES = [
    ["abcab"],
    ["x"],
    ["ab", "abcd", "x"],
    ["aaaa", "abab", "abcd", "bcda", "q"],
    ["he", "she", "his", "hers"],
    ["’tis", "“Oh", "Oh”"],  # Alice's curly quotes in the original
]


@pytest.mark.parametrize("module", [kmp, aho_corasick], ids=lambda m: m.NAME)
@pytest.mark.parametrize("queries", MEMORY_CASES)
def test_memory_bytes_ignores_non_latin1_characters(module, queries):
    """Same lengths + same character structure -> same memory_bytes, for KMP and Aho-Corasick."""
    from run_benchmark import LATIN1_POOL, NON_LATIN1_POOL, relabel
    from src.measure import measure_memory

    original = measure_memory(module, queries)[0]
    latin1 = measure_memory(module, relabel(queries, LATIN1_POOL))[0]
    non_latin1 = measure_memory(module, relabel(queries, NON_LATIN1_POOL))[0]
    assert original == latin1 == non_latin1


@pytest.mark.parametrize("queries", MEMORY_CASES)
def test_memory_columns_relationship(queries):
    """KMP: structure == raw. Aho-Corasick: raw - structure == 60 B per non-Latin-1 trie edge (BMP chars)."""
    from run_benchmark import NON_LATIN1_POOL, relabel
    from src.measure import measure_memory

    structure, raw, _ = measure_memory(kmp, queries)
    assert structure == raw

    renamed = relabel(queries, NON_LATIN1_POOL)
    structure, raw, _ = measure_memory(aho_corasick, renamed)
    edges = len(aho_corasick.trie_keys(aho_corasick.preprocess(renamed)))
    assert raw - structure == edges * sys.getsizeof("А")
