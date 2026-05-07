"""
Indexer structure for the COMP3011 search engine tool.

This file provides an initial scaffold for an inverted index. Real tokenisation,
ranking, and persistence will be implemented in later stages.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


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

    def save_to_file(self, path: str) -> None:
        """
        Save the current index and documents to a JSON file.

        Args:
            path: Output file path.
        """
        payload = {
            "documents": self.documents,
            "inverted_index": self.inverted_index,
        }
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_from_file(self, path: str) -> None:
        """
        Load index and documents from a JSON file.

        Note:
            JSON forces dictionary keys to be strings. This method converts
            document ids back to integers in both ``documents`` and each term's
            ``postings`` dictionary.

        Args:
            path: Input file path.
        """
        raw = json.loads(Path(path).read_text(encoding="utf-8"))

        documents_raw = raw.get("documents", {})
        inverted_raw = raw.get("inverted_index", {})

        documents: dict[int, dict[str, object]] = {}
        if isinstance(documents_raw, dict):
            for doc_id_str, meta in documents_raw.items():
                try:
                    doc_id = int(doc_id_str)
                except (TypeError, ValueError):
                    continue
                if isinstance(meta, dict):
                    documents[doc_id] = meta

        inverted_index: dict[str, dict[str, object]] = {}
        if isinstance(inverted_raw, dict):
            for term, entry in inverted_raw.items():
                if not isinstance(term, str) or not isinstance(entry, dict):
                    continue

                postings_raw = entry.get("postings", {})
                postings: dict[int, dict[str, object]] = {}
                if isinstance(postings_raw, dict):
                    for doc_id_str, posting in postings_raw.items():
                        try:
                            doc_id = int(doc_id_str)
                        except (TypeError, ValueError):
                            continue
                        if isinstance(posting, dict):
                            postings[doc_id] = posting

                df = entry.get("df", 0)
                inverted_index[term] = {
                    "df": df if isinstance(df, int) else 0,
                    "postings": postings,
                }

        self.documents = documents
        self.inverted_index = inverted_index
