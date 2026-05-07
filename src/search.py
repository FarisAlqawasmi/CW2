"""
Search engine structure for the COMP3011 search engine tool.

This module provides a minimal scaffold. Ranking and CLI integration are added
in later stages.
"""

from __future__ import annotations

import re


class SearchEngine:
    """
    Run queries against an inverted index and document store.

    Attributes:
        inverted_index: Term -> metadata (e.g. df, postings) from the indexer.
        documents: doc_id -> document metadata (e.g. url, title, word_count).
    """

    def __init__(
        self,
        inverted_index: dict[str, dict[str, object]],
        documents: dict[int, dict[str, object]],
    ) -> None:
        """
        Initialise the search engine with index and document data.

        Args:
            inverted_index: The inverted index built by ``InvertedIndexer``.
            documents: Per-document metadata keyed by document id.
        """
        self.inverted_index: dict[str, dict[str, object]] = inverted_index
        self.documents: dict[int, dict[str, object]] = documents

    def tokenize_query(self, query: str) -> list[str]:
        """
        Tokenize a raw query string into lowercase alphanumeric terms.

        This mirrors the indexer's current tokenisation approach (basic regex,
        no stopword removal or stemming).
        """
        return re.findall(r"[a-z0-9]+", query.lower())

    def lookup_term(self, term: str) -> dict[int, dict[str, object]]:
        """
        Look up postings for a single term.

        Args:
            term: Raw query term.

        Returns:
            Mapping from doc_id to posting data for that term.
        """
        normalized = term.lower()
        entry = self.inverted_index.get(normalized)
        if not isinstance(entry, dict):
            return {}

        postings = entry.get("postings")
        if not isinstance(postings, dict):
            return {}

        result: dict[int, dict[str, object]] = {}
        for doc_id, posting in postings.items():
            if isinstance(doc_id, int) and isinstance(posting, dict):
                result[doc_id] = posting
        return result

    def search(self, query: str) -> list[dict[str, object]]:
        """
        Run a conjunctive (AND) search for the given query.

        Args:
            query: User search string.

        Returns:
            Result list sorted by descending score (sum of term frequencies).
        """
        terms = self.tokenize_query(query)
        if not terms:
            return []

        postings_per_term: list[dict[int, dict[str, object]]] = [
            self.lookup_term(term) for term in terms
        ]
        if any(not postings for postings in postings_per_term):
            return []

        common_doc_ids = set(postings_per_term[0].keys())
        for postings in postings_per_term[1:]:
            common_doc_ids &= set(postings.keys())
            if not common_doc_ids:
                return []

        results: list[dict[str, object]] = []
        for doc_id in common_doc_ids:
            score = 0
            for postings in postings_per_term:
                tf = postings.get(doc_id, {}).get("tf")
                if isinstance(tf, int):
                    score += tf

            doc_meta = self.documents.get(doc_id, {})
            url = doc_meta.get("url", "")
            title = doc_meta.get("title", "")

            results.append(
                {
                    "doc_id": doc_id,
                    "url": url if isinstance(url, str) else "",
                    "title": title if isinstance(title, str) else "",
                    "score": score,
                }
            )

        results.sort(key=lambda r: int(r.get("score", 0)), reverse=True)
        return results
