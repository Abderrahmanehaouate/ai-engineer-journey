"""Command line entry point: ``journey status``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .parse import load_program
from .report import render, summarize

#: The package lives in e03-claude-code-101/, so the repo root is two levels up.
DEFAULT_REPO = Path(__file__).resolve().parent.parent.parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="journey",
        description="Report ai-engineer-journey program progress from its markdown.",
    )
    subcommands = parser.add_subparsers(dest="command")
    status = subcommands.add_parser("status", help="print program status")
    status.add_argument(
        "--repo",
        type=Path,
        default=DEFAULT_REPO,
        help="repo root to read (defaults to the enclosing journey repo)",
    )
    status.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero when the root README has drifted from the checkboxes",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    try:
        tasks = load_program(args.repo)
    except FileNotFoundError as exc:
        print(f"journey: {exc}", file=sys.stderr)
        return 2

    print(render(tasks))
    if args.strict and summarize(tasks).drifted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
