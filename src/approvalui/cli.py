"""Command-line interface for ApprovalUI."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from approvalui._core import ApprovalUIError, render


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="approvalui",
        description="Generate a clickable HTML approval page from a JSON spec.",
    )
    parser.add_argument("input", help="Path to the JSON spec")
    parser.add_argument("output", help="Path to write the HTML file")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ApprovalUI CLI.

    Returns:
        0 on success, 1 on error.
    """
    args = _parse_args(argv)

    try:
        spec = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {args.input}: {exc}", file=sys.stderr)
        return 1

    try:
        html_output = render(spec)
    except ApprovalUIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        Path(args.output).write_text(html_output, encoding="utf-8")
    except OSError as exc:
        print(f"Error: could not write {args.output}: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {args.output}")
    return 0
