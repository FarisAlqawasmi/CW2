"""Command-line interface for the COMP3011 search engine tool."""

from __future__ import annotations

import sys


PROMPT = "search> "


def show_help() -> None:
    """Display available commands and short descriptions."""
    print(
        "Commands:\n"
        "  build          - crawl and build the index (not implemented yet)\n"
        "  load           - load a saved index from disk (not implemented yet)\n"
        "  print <word>   - show postings for a word (not implemented yet)\n"
        "  find <query>   - run a search query (not implemented yet)\n"
        "  help           - show this message\n"
        "  exit           - quit the program"
    )


def handle_build() -> None:
    """Handle the build command placeholder."""
    print("Build command recognised. Crawler not implemented yet.")


def handle_load() -> None:
    """Handle the load command placeholder."""
    print("Load command not implemented yet.")


def handle_print_word(args: list[str]) -> None:
    """
    Handle the print command placeholder.

    Args:
        args: Tokens after the command name.
    """
    if not args:
        print("Usage: print <word>")
        print("  <word> - term to look up in the index once implemented.")
        return

    word = " ".join(args)
    print(f'Print command recognised. Index not implemented yet. Requested word: "{word}"')


def handle_find_query(args: list[str]) -> None:
    """
    Handle the find command placeholder.

    Args:
        args: Tokens after the command name.
    """
    if not args:
        print("Usage: find <query>")
        print("  <query> - search terms once implemented.")
        return

    query = " ".join(args)
    print(f'Find command recognised. Search not implemented yet. Query: "{query}"')


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