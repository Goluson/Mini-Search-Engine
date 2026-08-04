"""
search_engine.py

Command-line interface for the mini search engine.

Usage:
    python search_engine.py index corpus
    python search_engine.py query "python tutorial"
    python search_engine.py query "python AND tutorial"
    python search_engine.py query "python NOT snake"
"""

import sys
import json
from indexer import Indexer
from ranking import tfidf_search
from boolean_search import boolean_search, is_boolean_query

INDEX_FILE = "index.json"


def cmd_index(folder: str) -> None:
    idx = Indexer()
    idx.build_from_folder(folder)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(idx.to_dict(), f)

    print(f"Indexed {idx.doc_count} documents from '{folder}/' -> {INDEX_FILE}")
    for doc_id, name in idx.doc_names.items():
        print(f"  [{doc_id}] {name}")


def _load_index() -> Indexer:
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"No index found. Run 'python search_engine.py index <folder>' first.")
        sys.exit(1)
    return Indexer.from_dict(data)


def cmd_query(query_str: str) -> None:
    idx = _load_index()

    if is_boolean_query(query_str):
        doc_ids = boolean_search(idx, query_str)
        print(f"Boolean search: \"{query_str}\"")
        if not doc_ids:
            print("  No matching documents.")
        for doc_id in sorted(doc_ids):
            print(f"  - {idx.doc_names[doc_id]}")
    else:
        results = tfidf_search(idx, query_str, top_k=5)
        print(f"Ranked search: \"{query_str}\"")
        if not results:
            print("  No matching documents.")
        for name, score in results:
            print(f"  {score:.4f}  {name}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "index":
        if len(sys.argv) < 3:
            print("Usage: python search_engine.py index <folder>")
            return
        cmd_index(sys.argv[2])

    elif command == "query":
        if len(sys.argv) < 3:
            print('Usage: python search_engine.py query "search terms"')
            return
        cmd_query(sys.argv[2])

    else:
        print(f"Unknown command: '{command}'")
        print(__doc__)


if __name__ == "__main__":
    main()
