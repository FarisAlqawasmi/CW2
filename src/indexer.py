"""
Indexer structure for the COMP3011 search engine tool.

This file provides an initial scaffold for an inverted index. Real tokenisation,
ranking, and persistence will be implemented in later stages.
"""

from __future__ import annotations


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
        Add a document to the index (placeholder).

        Args:
            doc_id: Integer document identifier.
            url: Canonical URL of the document.
            title: Extracted page title.
            text: Extracted visible page text.
        """
        _ = (doc_id, url, title, text)
        return None

    def build_index(self, pages: dict[int, dict[str, object]]) -> None:
        """
        Build the index from crawled pages (placeholder).

        Args:
            pages: Output from the crawler keyed by doc_id. Each page is expected
                to include keys like "url", "title", and "text".
        """
        _ = pages
        return None

    def get_index(self) -> dict[str, dict[str, object]]:
        """
        Return the current inverted index structure.

        Returns:
            The inverted index mapping (placeholder structure).
        """
        return dict(self.inverted_index)
