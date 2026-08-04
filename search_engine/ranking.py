"""
ranking.py

Scores documents by relevance to a query using TF-IDF (Term Frequency -
Inverse Document Frequency), then returns the top-K highest scoring
documents using a heap instead of sorting the entire result set.

TF-IDF, in plain words:
  - TF (term frequency): how often a word appears in THIS document.
    A document mentioning "python" 5 times is probably more about Python
    than one mentioning it once.
  - IDF (inverse document frequency): how RARE a word is across ALL
    documents. Common words like "the" appear everywhere and carry little
    meaning; rare words like "carbonara" are much more distinctive.
  - Multiplying them together rewards words that are both frequent in a
    specific document AND rare across the whole corpus — exactly the
    words that make that document distinctive.
"""

import heapq
from collections import defaultdict
from tokenizer import tokenize
from indexer import Indexer


def tfidf_search(indexer: Indexer, query: str, top_k: int = 5) -> list[tuple[str, float]]:
    query_terms = tokenize(query)
    scores: dict[int, float] = defaultdict(float)

    for term in query_terms:
        postings = indexer.index.get(term, {})
        idf = indexer.idf(term)

        for doc_id, term_freq in postings.items():
            # Normalize by document length so a long document doesn't win
            # purely by containing more words overall.
            normalized_tf = term_freq / indexer.doc_lengths[doc_id]
            scores[doc_id] += normalized_tf * idf

    # heapq.nlargest is O(n log k) — much better than sorting all n results
    # (O(n log n)) when you only need the top few, which is the realistic
    # case for a search engine returning e.g. the top 5 or 10 results.
    top_docs = heapq.nlargest(top_k, scores.items(), key=lambda pair: pair[1])

    return [
        (indexer.doc_names[doc_id], score)
        for doc_id, score in top_docs
        if score > 0
    ]
