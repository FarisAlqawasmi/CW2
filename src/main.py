"""Command-line interface for the COMP3011 search engine tool."""

from __future__ import annotations

import sys
from pathlib import Path

from crawler import SearchCrawler
from indexer import InvertedIndexer
from search import SearchEngine


PROMPT = "search> "

TARGET_WEBSITE: str = "https://quotes.toscrape.com/"
INDEX_FILE = Path("data/index.json")

current_indexer: InvertedIndexer | None = None


def show_help() -> None:
    """Display available commands and short descriptions."""
    print(
        "Commands:\n"
        "  build          - crawl pages and build the inverted index\n"
        "  load           - load a saved index from disk (not implemented yet)\n"
        "  print <word>   - show postings for a word (not implemented yet)\n"
        "  find <query>   - run a search query (not implemented yet)\n"
        "  help           - show this message\n"
        "  exit           - quit the program"
    )


def handle_build() -> None:
    """Crawl the target website and build the inverted index."""
    global current_indexer
    crawler = SearchCrawler(start_url=TARGET_WEBSITE, max_pages=3)
    crawled_pages = crawler.crawl()

    indexer = InvertedIndexer()
    indexer.build_index(crawled_pages)
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    indexer.save_to_file(str(INDEX_FILE))
    current_indexer = indexer

    print(f"Pages crawled: {len(crawled_pages)}")
    print(f"Documents indexed: {len(indexer.documents)}")
    print(f"Unique terms: {len(indexer.get_index())}")
    print(f"Index saved to: {INDEX_FILE}")


def handle_load() -> None:
    """Load the inverted index from disk."""
    global current_indexer
    if not INDEX_FILE.exists():
        print(f"No saved index found at: {INDEX_FILE}")
        print("Run 'build' first to crawl pages and create the index.")
        return

    indexer = InvertedIndexer()
    indexer.load_from_file(str(INDEX_FILE))
    current_indexer = indexer

    print(f"Documents loaded: {len(indexer.documents)}")
    print(f"Unique terms loaded: {len(indexer.get_index())}")


def handle_print_word(args: list[str]) -> None:
    """
    Handle the print command.

    Args:
        args: Tokens after the command name.
    """
    if not args:
        print("Usage: print <word>")
        print("  <word> - term to look up in the index once implemented.")
        return

    if current_indexer is None:
        print("No index is currently loaded. Run 'build' first.")
        return

    word = " ".join(args).lower()
    index = current_indexer.get_index()
    entry = index.get(word)

    if not isinstance(entry, dict):
        print(f'The word "{word}" is not in the index.')
        return

    df = entry.get("df")
    postings = entry.get("postings")
    if not isinstance(df, int) or not isinstance(postings, dict):
        print(f'The word "{word}" is not in the index.')
        return

    print(f'Word: "{word}"')
    print(f"Document frequency (df): {df}")

    for doc_id in sorted(postings):
        posting = postings.get(doc_id)
        if not isinstance(doc_id, int) or not isinstance(posting, dict):
            continue

        tf = posting.get("tf", 0)
        positions = posting.get("positions", [])

        url = ""
        doc_meta = current_indexer.documents.get(doc_id, {})
        if isinstance(doc_meta, dict):
            meta_url = doc_meta.get("url", "")
            if isinstance(meta_url, str):
                url = meta_url

        print(f"- doc_id: {doc_id}")
        print(f"  tf: {tf}")
        print(f"  positions: {positions}")
        if url:
            print(f"  url: {url}")


def handle_find_query(args: list[str]) -> None:
    """
    Handle the find command.

    Args:
        args: Tokens after the command name.
    """
    if not args:
        print("Usage: find <query>")
        print("  <query> - search terms.")
        return

    query = " ".join(args)
    if current_indexer is None:
        print("No index is currently loaded. Run 'build' first.")
        return

    engine = SearchEngine(current_indexer.get_index(), current_indexer.documents)
    results = engine.search(query)

    if not results:
        print("No matching pages found.")
        return

    for result in results:
        score = result.get("score", 0)
        title = result.get("title", "")
        url = result.get("url", "")
        print(f"[{score}] {title} - {url}")


def handle_unknown(command: str) -> None:
    """Report an unrecognised command and suggest help."""
    print(f'Unknown command: "{command}". Type "help" for a list of commands.')


def process_line(line: str) -> bool:
    """
    Parse and execute one line of input.

    Args:
        line: Raw input entered by the user.

    Returns:
        True if the shell should continue running, otherwise False.
    """
    parts = line.strip().split()
    if not parts:
        return True

    command = parts[0].lower()
    args = parts[1:]

    if command == "exit":
        print("Goodbye.")
        return False
    if command == "help":
        show_help()
        return True
    if command == "build":
        handle_build()
        return True
    if command == "load":
        handle_load()
        return True
    if command == "print":
        handle_print_word(args)
        return True
    if command == "find":
        handle_find_query(args)
        return True

    handle_unknown(command)
    return True


def run_shell() -> None:
    """Run the interactive command loop until the user exits."""
    print("Search engine tool - type 'help' for commands, 'exit' to quit.")
    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            print()
            print("Goodbye.")
            break

        if not process_line(line):
            break


def main() -> None:
    """Run the command-line interface."""
    run_shell()
    sys.exit(0)


if __name__ == "__main__":
    main()