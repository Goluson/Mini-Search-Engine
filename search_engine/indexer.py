"""
indexer.py

Builds and stores the inverted index: a mapping from each word to the
documents it appears in, plus how many times it appears there.

    {
      "python": {0: 3, 4: 2},   # appears 3 times in doc 0, 2 times in doc 4
      "pasta":  {1: 5},
      ...
    }

This is the core data structure behind every real search engine. Without
it, answering "which documents contain 'python'?" would mean scanning
every document's full text on every single search — O(n) work per query.
With the index, it's a single O(1) dictionary lookup.
"""

import os
import math
from collections import defaultdict
from tokenizer import tokenize


class Indexer:
    def __init__(self):
        self.index: dict[str, dict[int, int]] = defaultdict(dict)  # term -> {doc_id: term_freq}
        self.doc_names: dict[int, str] = {}   # doc_id -> filename
        self.doc_lengths: dict[int, int] = {}  # doc_id -> total token count (for TF normalization)
        self.doc_count: int = 0

    def add_document(self, doc_id: int, filename: str, text: str) -> None:
        """Tokenize one document and fold it into the index."""
        tokens = tokenize(text)
        self.doc_names[doc_id] = filename
        self.doc_lengths[doc_id] = len(tokens) or 1  # avoid divide-by-zero later

        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1

        for term, freq in term_freq.items():
            self.index[term][doc_id] = freq

        self.doc_count += 1

    def build_from_folder(self, folder_path: str) -> None:
        """Index every .txt file in a folder, in sorted (deterministic) order."""
        doc_id = 0
        for fname in sorted(os.listdir(folder_path)):
            if not fname.endswith(".txt"):
                continue
            path = os.path.join(folder_path, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            self.add_document(doc_id, fname, text)
            doc_id += 1

    def idf(self, term: str) -> float:
        """
        Inverse document frequency: rare words score higher than common ones.
        Smoothed with +1 in numerator/denominator to avoid division by zero
        and to keep even a word that's in every document from scoring exactly 0.
        """
        doc_freq = len(self.index.get(term, {}))
        if doc_freq == 0:
            return 0.0
        return math.log((self.doc_count + 1) / (doc_freq + 1)) + 1

    # ---- Persistence: save/load the index as JSON so you don't have to
    # ---- re-index every time you search ----

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "doc_names": self.doc_names,
            "doc_lengths": self.doc_lengths,
            "doc_count": self.doc_count,
        }

    @staticmethod
    def from_dict(data: dict) -> "Indexer":
        idx = Indexer()
        # JSON turns all dict keys into strings, so doc_ids need converting back to int.
        idx.index = defaultdict(
            dict,
            {
                term: {int(doc_id): freq for doc_id, freq in postings.items()}
                for term, postings in data["index"].items()
            },
        )
        idx.doc_names = {int(k): v for k, v in data["doc_names"].items()}
        idx.doc_lengths = {int(k): v for k, v in data["doc_lengths"].items()}
        idx.doc_count = data["doc_count"]
        return idx
