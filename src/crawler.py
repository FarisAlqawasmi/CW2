"""Crawler structure for the COMP3011 search engine tool."""

from __future__ import annotations

from collections import deque
from typing import Deque
import time
from urllib.parse import urldefrag, urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


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
        """
        Crawl paginated quote listing pages by following the "Next" link.

        This avoids crawling all internal links (authors/tags/login, etc.) and
        instead follows the site's pagination path:
        https://quotes.toscrape.com/ -> /page/2/ -> /page/3/ -> ...
        """
        last_request_time: float | None = None

        current_url: str | None = self.normalize_url(self.start_url)
        while current_url is not None:
            if self.max_pages is not None and len(self.crawled_pages) >= self.max_pages:
                break

            if current_url in self.visited:
                break
            self.visited.add(current_url)

            if last_request_time is not None:
                elapsed = time.monotonic() - last_request_time
                remaining = self.politeness_delay - elapsed
                if remaining > 0:
                    time.sleep(remaining)

            html = self.fetch_page(current_url)
            last_request_time = time.monotonic()
            if html is None:
                break

            title, text = self.extract_text(html)
            links = self.extract_links(html, current_url)

            doc_id = len(self.crawled_pages)
            self.crawled_pages[doc_id] = {
                "url": current_url,
                "title": title,
                "text": text,
                "links": links,
            }

            next_url = self.extract_next_page(html, current_url)
            if next_url is None or next_url in self.visited:
                break

            current_url = next_url

        return dict(self.crawled_pages)

    def fetch_page(self, url: str) -> str | None:
        """Fetch a page and return its HTML, or None on failure."""
        try:
            response = requests.get(url, timeout=self.timeout)
        except requests.RequestException:
            return None

        if not response.ok:
            return None

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            return None

        return response.text

    def extract_links(self, html: str, base_url: str) -> list[str]:
        """Extract normalized internal links from HTML."""
        soup = BeautifulSoup(html, "html.parser")

        links: list[str] = []
        seen: set[str] = set()

        for a_tag in soup.find_all("a", href=True):
            href = str(a_tag.get("href", "")).strip()
            if not href:
                continue

            lowered = href.lower()
            if lowered.startswith(("javascript:", "mailto:", "tel:")):
                continue

            resolved = urljoin(base_url, href)
            normalized = self.normalize_url(resolved)

            if not self.is_internal_url(normalized):
                continue

            if normalized in seen:
                continue

            seen.add(normalized)
            links.append(normalized)

        return links

    def extract_next_page(self, html: str, base_url: str) -> str | None:
        """
        Extract the pagination "Next" page URL from HTML.

        Args:
            html: Raw page HTML.
            base_url: URL of the current page (used to resolve relative links).

        Returns:
            Normalized absolute URL for the next page, or None if no next link exists.
        """
        soup = BeautifulSoup(html, "html.parser")

        next_link = soup.select_one("li.next a[href]")
        if next_link is None:
            return None

        href = str(next_link.get("href", "")).strip()
        if not href:
            return None

        resolved = urljoin(base_url, href)
        normalized = self.normalize_url(resolved)
        if not self.is_internal_url(normalized):
            return None

        return normalized

    def extract_text(self, html: str) -> tuple[str, str]:
        """Extract the page title and visible text from HTML."""
        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.get_text(separator=" ", strip=True) if title_tag else ""
        title = " ".join(title.split())

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())
        return (title, text)
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize a URL for consistent crawling behaviour.

        This removes fragments and converts relative URLs into
        absolute URLs based on the crawler start URL.
        """
        absolute = urljoin(self.start_url, url)
        absolute, _ = urldefrag(absolute)

        parts = urlsplit(absolute)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))

    def is_internal_url(self, url: str) -> bool:
        """
        Check whether a URL belongs to the target website.
        """
        candidate = urlsplit(self.normalize_url(url)).netloc.lower()
        target = urlsplit(self.normalize_url(self.start_url)).netloc.lower()
        return bool(candidate) and candidate == target 