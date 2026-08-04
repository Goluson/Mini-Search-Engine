# Mini Search Engine

A small search engine built entirely in pure Python (standard library only —
no frameworks, no external packages). Supports ranked (TF-IDF) search and
boolean (AND/OR/NOT) search over a folder of text documents.

## Setup

Requires Python 3.9+ (uses built-in type hints like `list[str]`). No `pip
install` needed — everything here is Python standard library.

```bash
# 1. Build the index from the sample corpus
python3 search_engine.py index corpus

# 2. Run a ranked search
python3 search_engine.py query "python tutorial"

# 3. Run a boolean search
python3 search_engine.py query "python NOT snake"
```

Re-run `index` any time you add/change documents in the `corpus/` folder —
it rebuilds `index.json` from scratch each time.

## How It Works

1. **Tokenizer** (`tokenizer.py`) — splits text into lowercase word tokens.
2. **Indexer** (`indexer.py`) — builds an inverted index: `{word: {doc_id:
   count}}`. This is what makes search fast — instead of scanning every
   document's full text on every query (O(n) per search), looking up a
   word is a single O(1) dictionary access.
3. **Ranking** (`ranking.py`) — scores documents using TF-IDF (term
   frequency × inverse document frequency), then returns the top-K results
   using a heap (`heapq.nlargest`) rather than sorting the entire result
   set — O(n log k) instead of O(n log n).
4. **Boolean search** (`boolean_search.py`) — supports `AND` / `OR` / `NOT`
   between terms using set intersection/union/difference.

## Example Queries to Try

```bash
python3 search_engine.py query "python"              # ranked: language doc ranks above snake doc
python3 search_engine.py query "pasta cooking"        # ranked
python3 search_engine.py query "python AND language"  # boolean AND
python3 search_engine.py query "python OR football"   # boolean OR
python3 search_engine.py query "python NOT snake"      # boolean NOT — disambiguates the two "python" docs
```

## Design Decisions & Known Limitations

- **Boolean queries are evaluated strictly left-to-right**, with no
  operator precedence and no parentheses support. `"a AND b OR c"` always
  means `"(a AND b) OR c"` — a real search engine would use a proper
  expression parser for this.
- **TF-IDF, not a more advanced ranking algorithm** (like BM25). TF-IDF is
  simpler to explain and reason about, at the cost of being less
  sophisticated than what production search engines actually use.
- **Index is rebuilt fully each time**, not incrementally updated. Fine at
  this scale (a handful of documents); a real system would support adding
  a single new document without reprocessing everything.
- **No stemming/lemmatization** — "running" and "run" are treated as
  completely different tokens. Adding this would improve recall at the
  cost of some precision and complexity.

## Running Tests

```bash
python3 -m unittest test_search_engine.py -v
```

16 tests covering the tokenizer, index building, IDF calculation,
serialization, ranked search, and all three boolean operators.

## Project Structure

```
search_engine/
├── corpus/                    # sample documents to search over
│   ├── doc1_python_language.txt
│   ├── doc2_cooking_pasta.txt
│   ├── doc3_space_exploration.txt
│   ├── doc4_football_sports.txt
│   └── doc5_python_snake.txt
├── tokenizer.py                # text -> tokens
├── indexer.py                  # inverted index + IDF
├── ranking.py                  # TF-IDF scoring + heap-based top-K
├── boolean_search.py            # AND / OR / NOT
├── search_engine.py             # CLI entry point
└── test_search_engine.py        # automated test suite (16 tests)
```
