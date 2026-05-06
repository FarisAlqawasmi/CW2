"""Crawler structure for the COMP3011 search engine tool."""

from __future__ import annotations

from collections import deque
from typing import Deque
from urllib.parse import urldefrag, urljoin, urlsplit, urlunsplit


class SearchCrawler:
    """Represent the crawler used to explore the target website."""

    def __init__(
        self,
        start_url: str,
        politeness_delay: float = 6.0,
        timeout: int = 10,
        max_pages: int | None = None,
    ) -> None:
        """Initialise crawler configuration and internal containers."""
        self.start_url: str = start_url
        self.politeness_delay: float = politeness_delay
        self.timeout: int = timeout
        self.max_pages: int | None = max_pages

        self.frontier: Deque[str] = deque([start_url])
        self.visited: set[str] = set()
        self.crawled_pages: dict[int, dict[str, object]] = {}

    def crawl(self) -> dict[int, dict[str, object]]:
        """Run the crawl process (placeholder)."""
        return dict(self.crawled_pages)

    def fetch_page(self, url: str) -> str | None:
        """Fetch a page and return HTML (placeholder)."""
        _ = url
        return None

    def extract_links(self, html: str, base_url: str) -> list[str]:
        """Extract links from HTML (placeholder)."""
        _ = (html, base_url)
        return []

    def extract_text(self, html: str) -> tuple[str, str]:
        """Extract title and text from HTML (placeholder)."""
        _ = html
        return ("", "")

    def normalize_url(self, url: str) -> str:
        """Normalize a URL (placeholder implementation)."""
        absolute = urljoin(self.start_url, url)
        absolute, _ = urldefrag(absolute)

        parts = urlsplit(absolute)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))

    def is_internal_url(self, url: str) -> bool:
        """Check if a URL belongs to the target domain."""
        candidate = urlsplit(self.normalize_url(url)).netloc.lower()
        target = urlsplit(self.normalize_url(self.start_url)).netloc.lower()
        return bool(candidate) and candidate == target