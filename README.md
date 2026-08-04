# Mini-Search-Engine
Built a search engine from scratch in pure Python, implementing an inverted index for O(1) term lookup across a document corpus Implemented TF-IDF ranking to score and return the top-K most relevant documents per query using a min-heap, avoiding a full O(n log n) sort Designed a boolean query engine supporting AND / OR / NOT operators.
#Project Overview
tokenizer.py: Handles breaking down the raw text from your documents into individual, searchable words (tokens).
