"""
Indexer structure for the COMP3011 search engine tool.

This file provides an initial scaffold for an inverted index. Real tokenisation,
ranking, and persistence will be implemented in later stages.
"""

from __future__ import annotations

import re


class InvertedIndexer:
    """
    Represent an inverted index over a collection of crawled documents.

    Attributes:
        inverted_index: Mapping of terms to postings/metadata (placeholder structure).
        documents: Mapping of doc_id to document metadata (placeholder structure).
    """

    def __init__(self) -> None:
        """Initialise empty index and document store."""
        self.inverted_index: dict[str, dict[str, object]] = {}
        self.documents: dict[int, dict[str, object]] = {}

    def add_document(self, doc_id: int, url: str, title: str, text: str) -> None:
        """
        Add a document to the index.

        Args:
            doc_id: Integer document identifier.
            url: Canonical URL of the document.
            title: Extracted page title.
            text: Extracted visible page text.
        """
        tokens = self.tokenize(text)

        self.documents[doc_id] = {
            "url": url,
            "title": title,
            "word_count": len(tokens),
        }

        term_positions: dict[str, list[int]] = {}
        for pos, term in enumerate(tokens):
            term_positions.setdefault(term, []).append(pos)

        for term, positions in term_positions.items():
            entry = self.inverted_index.get(term)
            if entry is None:
                entry = {"df": 0, "postings": {}}
                self.inverted_index[term] = entry

            postings = entry.get("postings")
            if not isinstance(postings, dict):
                postings = {}
                entry["postings"] = postings

            if doc_id not in postings:
                df = entry.get("df")
                entry["df"] = (df if isinstance(df, int) else 0) + 1

            postings[doc_id] = {
                "tf": len(positions),
                "positions": positions,
            }

    def tokenize(self, text: str) -> list[str]:
        """
        Convert raw text into a list of tokens.

        The current tokenizer:
        - lowercases text
        - extracts alphanumeric tokens (letters and/or digits)
        - keeps numbers
        """
        lowered = text.lower()
        return re.findall(r"[a-z0-9]+", lowered)

    def build_index(self, pages: dict[int, dict[str, object]]) -> None:
        """
        Build the index from crawled pages.

        Args:
            pages: Output from the crawler keyed by doc_id. Each page is expected
                to include keys like "url", "title", and "text".
        """
        self.inverted_index = {}
        self.documents = {}

        for doc_id, page in pages.items():
            url = page.get("url")
            title = page.get("title")
            text = page.get("text")

            if not isinstance(url, str):
                continue
            if not isinstance(title, str):
                continue
            if not isinstance(text, str):
                continue

            self.add_document(doc_id, url, title, text)
        return None

    def get_index(self) -> dict[str, dict[str, object]]:
        """
        Return the current inverted index structure.

        Returns:
            The inverted index mapping (placeholder structure).
        """
        return dict(self.inverted_index)
