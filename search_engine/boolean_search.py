"""
boolean_search.py

Supports simple boolean queries between terms: AND, OR, NOT.

    "python AND tutorial"     -> docs containing both words
    "python OR snake"         -> docs containing either word
    "python NOT snake"        -> docs with "python" but not "snake"

Known limitation (intentional, kept simple on purpose): operators are
evaluated strictly LEFT TO RIGHT with no precedence rules and no support
for parentheses. "a AND b OR c" is evaluated as "(a AND b) OR c", always,
regardless of what real-world boolean logic precedence would suggest.
A production search engine would use a proper expression parser here.
"""

from tokenizer import tokenize
from indexer import Indexer

OPERATORS = {"AND", "OR", "NOT"}


def _docs_for_term(indexer: Indexer, term: str) -> set[int]:
    tokens = tokenize(term)
    if not tokens:
        return set()
    return set(indexer.index.get(tokens[0], {}).keys())


def boolean_search(indexer: Indexer, query: str) -> set[int]:
    raw_tokens = query.strip().split()
    if not raw_tokens:
        return set()

    # First token is always treated as a plain term, not an operator.
    result = _docs_for_term(indexer, raw_tokens[0])

    i = 1
    while i < len(raw_tokens):
        op = raw_tokens[i].upper()

        # If we don't recognize this as an operator, skip it rather than
        # crash — keeps the CLI resilient to slightly malformed queries.
        if op not in OPERATORS or i + 1 >= len(raw_tokens):
            i += 1
            continue

        next_term_docs = _docs_for_term(indexer, raw_tokens[i + 1])

        if op == "AND":
            result &= next_term_docs
        elif op == "OR":
            result |= next_term_docs
        elif op == "NOT":
            result -= next_term_docs

        i += 2

    return result


def is_boolean_query(query: str) -> bool:
    """Detect whether a query string contains any boolean operators."""
    return any(token.upper() in OPERATORS for token in query.split())
