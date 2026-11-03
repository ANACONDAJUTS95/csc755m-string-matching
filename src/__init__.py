"""Algorithms and shared helpers for the CSC755M string-matching benchmark."""

from . import aho_corasick, kmp, naive

# Name used in config.ALGORITHMS / the CSV -> module implementing it.
ALGORITHM_MODULES = {
    "naive": naive,
    "kmp": kmp,
    "aho_corasick": aho_corasick,
}
