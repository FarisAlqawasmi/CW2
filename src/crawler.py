"""Crawler structure for the COMP3011 search engine tool."""

from __future__ import annotations

from collections import deque
from typing import Deque


class SearchCrawler:
    """Represent the crawler used to explore the target website."""

    def __init__(
        self,
        start_url: str,
        politeness_delay: float = 6.0,
        timeout: int = 10,
        max_pages: int | None = None,
    ) -> None:
        """
        Initialise the crawler configuration and internal containers.

        Args:
            start_url: The initial URL used to seed the crawl.
            politeness_delay: Minimum delay in seconds between requests.
            timeout: Timeout in seconds for HTTP requests.
            max_pages: Optional limit on the number of pages to crawl.
        """
        self.start_url: str = start_url
        self.politeness_delay: float = politeness_delay
        self.timeout: int = timeout
        self.max_pages: int | None = max_pages

        self.frontier: Deque[str] = deque([start_url])
        self.visited: set[str] = set()
        self.crawled_pages: dict[int, dict[str, object]] = {}

    def crawl(self) -> dict[int, dict[str, object]]:
        """
        Run the crawl process.

        Returns:
            A mapping of document IDs to page data.

        Note:
            This is a skeleton implementation for now and currently returns the
            existing crawled_pages dictionary without performing any crawl.
        """
        return dict(self.crawled_pages)