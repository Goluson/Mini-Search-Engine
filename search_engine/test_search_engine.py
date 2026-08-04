"""
test_search_engine.py

Basic automated tests for the tokenizer, indexer, ranking, and boolean
search modules. Run with:

    python3 -m unittest test_search_engine.py -v
"""

import unittest
from tokenizer import tokenize
from indexer import Indexer
from ranking import tfidf_search
from boolean_search import boolean_search, is_boolean_query


def build_test_index() -> Indexer:
    idx = Indexer()
    idx.add_document(0, "doc0.txt", "python is a great programming language")
    idx.add_document(1, "doc1.txt", "the python snake is found in africa")
    idx.add_document(2, "doc2.txt", "football is a popular sport worldwide")
    return idx


class TestTokenizer(unittest.TestCase):
    def test_basic_tokenizing(self):
        self.assertEqual(tokenize("Python is FUN!"), ["python", "is", "fun"])

    def test_apostrophes_preserved(self):
        self.assertEqual(tokenize("isn't it"), ["isn't", "it"])

    def test_empty_string(self):
        self.assertEqual(tokenize(""), [])

    def test_none_safe(self):
        self.assertEqual(tokenize(None), [])


class TestIndexer(unittest.TestCase):
    def test_index_contains_expected_terms(self):
        idx = build_test_index()
        self.assertIn("python", idx.index)
        self.assertIn(0, idx.index["python"])
        self.assertIn(1, idx.index["python"])

    def test_doc_count(self):
        idx = build_test_index()
        self.assertEqual(idx.doc_count, 3)

    def test_idf_rare_word_higher_than_common_word(self):
        idx = build_test_index()
        # "python" appears in 2/3 docs, "football" in 1/3 -> football is rarer -> higher idf
        self.assertGreater(idx.idf("football"), idx.idf("python"))

    def test_idf_unknown_term_is_zero(self):
        idx = build_test_index()
        self.assertEqual(idx.idf("nonexistentword"), 0.0)

    def test_serialization_round_trip(self):
        idx = build_test_index()
        data = idx.to_dict()
        restored = Indexer.from_dict(data)
        self.assertEqual(restored.doc_count, idx.doc_count)
        self.assertEqual(restored.index["python"], idx.index["python"])


class TestRanking(unittest.TestCase):
    def test_ranked_search_returns_relevant_doc_first(self):
        idx = build_test_index()
        results = tfidf_search(idx, "programming language", top_k=5)
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0][0], "doc0.txt")

    def test_no_match_returns_empty(self):
        idx = build_test_index()
        results = tfidf_search(idx, "nonexistentword", top_k=5)
        self.assertEqual(results, [])

    def test_top_k_limits_results(self):
        idx = build_test_index()
        results = tfidf_search(idx, "python football programming", top_k=1)
        self.assertLessEqual(len(results), 1)


class TestBooleanSearch(unittest.TestCase):
    def test_and_operator(self):
        idx = build_test_index()
        result = boolean_search(idx, "python AND snake")
        self.assertEqual(result, {1})

    def test_or_operator(self):
        idx = build_test_index()
        result = boolean_search(idx, "snake OR football")
        self.assertEqual(result, {1, 2})

    def test_not_operator(self):
        idx = build_test_index()
        result = boolean_search(idx, "python NOT snake")
        self.assertEqual(result, {0})

    def test_is_boolean_query_detection(self):
        self.assertTrue(is_boolean_query("python AND tutorial"))
        self.assertFalse(is_boolean_query("python tutorial"))


if __name__ == "__main__":
    unittest.main()
