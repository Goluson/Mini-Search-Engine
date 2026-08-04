# Mini-Search-Engine
Built a search engine from scratch in pure Python, implementing an inverted index for O(1) term lookup across a document corpus Implemented TF-IDF ranking to score and return the top-K most relevant documents per query using a min-heap, avoiding a full O(n log n) sort Designed a boolean query engine supporting AND / OR / NOT operators.
# Project Overview
tokenizer.py: Handles breaking down the raw text from your documents into individual, searchable words (tokens).


indexer.py: Likely builds an "inverted index," which is a database mapping each word to the specific documents where it appears.

boolean_search.py: Allows for strict query matching using operators like AND, OR, and NOT (e.g., searching for "space AND exploration").

ranking.py: Implements a scoring algorithm (such as TF-IDF) to return the most relevant documents first, rather than just returning a random list of matches.
