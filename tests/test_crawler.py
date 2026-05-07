from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Allow tests to import modules from src/ when the project isn't packaged.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crawler import SearchCrawler  # noqa: E402


@pytest.fixture()
def crawler() -> SearchCrawler:
    return SearchCrawler(start_url="https://quotes.toscrape.com/", max_pages=1)


def test_normalize_url_removes_fragments_and_resolves_relative_urls(crawler: SearchCrawler) -> None:
    assert (
        crawler.normalize_url("https://quotes.toscrape.com/page/1/#top")
        == "https://quotes.toscrape.com/page/1/"
    )
    assert (
        crawler.normalize_url("/tag/love/#fragment")
        == "https://quotes.toscrape.com/tag/love/"
    )


def test_is_internal_url_true_for_internal_false_for_external(crawler: SearchCrawler) -> None:
    assert crawler.is_internal_url("https://quotes.toscrape.com/author/Albert-Einstein/") is True
    assert crawler.is_internal_url("/tag/life/") is True

    assert crawler.is_internal_url("https://example.com/") is False
    assert crawler.is_internal_url("https://quotes.toscrape.com.evil.com/") is False


def test_extract_links_internal_only_resolves_relative_and_dedupes(crawler: SearchCrawler) -> None:
    html = """
    <html>
      <body>
        <a href="/page/1/">Page 1</a>
        <a href="https://quotes.toscrape.com/page/1/#frag">Page 1 duplicate</a>
        <a href="/page/2/">Page 2</a>
        <a href="https://example.com/external">External</a>
        <a href="mailto:test@example.com">Mail</a>
      </body>
    </html>
    """
    links = crawler.extract_links(html, base_url="https://quotes.toscrape.com/")

    assert links == [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]


def test_extract_text_extracts_title_strips_script_style_noscript_and_normalizes_whitespace(
    crawler: SearchCrawler,
) -> None:
    html = """
    <html>
      <head>
        <title>
          Test   Title
        </title>
        <style>body { color: red; }</style>
        <script>var secret = 123;</script>
      </head>
      <body>
        <noscript>no script text</noscript>
        <h1> Hello </h1>
        <p>World   !</p>
      </body>
    </html>
    """
    title, text = crawler.extract_text(html)

    assert title == "Test Title"
    assert "secret" not in text
    assert "no script text" not in text
    assert "color" not in text
    assert text == "Test Title Hello World !"
