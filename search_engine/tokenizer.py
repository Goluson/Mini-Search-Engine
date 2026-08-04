"""
tokenizer.py

Turns raw text into a clean list of lowercase word tokens.
This is the foundation every other module builds on — get this wrong
and everything downstream (index, ranking, search) breaks quietly.
"""

import re

# Basic regex: keep letters, digits, and apostrophes (so "it's" stays one token),
# split on everything else (punctuation, whitespace, newlines).
_TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9']+")


def tokenize(text: str) -> list[str]:
    """
    Convert a string into a list of lowercase tokens.

    Example:
        tokenize("Python is FUN! Isn't it?")
        -> ["python", "is", "fun", "isn't", "it"]
    """
    if not text:
        return []
    return _TOKEN_PATTERN.findall(text.lower())
