"""CLI entry point for the publication-code linkage extractor.

Usage::

    python -m aiod.linkage_cli <paper-identifier> --model <litellm-model> [options]

Examples::

    # From a DOI
    python -m aiod.linkage_cli "10.48550/arXiv.2307.09288" --model openai/gpt-4o

    # From a Zenodo link
    python -m aiod.linkage_cli "https://zenodo.org/records/12345" --model anthropic/claude-3.5-sonnet

    # From a local PDF
    python -m aiod.linkage_cli paper.pdf --model ollama/llama3

    # JSON output
    python -m aiod.linkage_cli paper.pdf --model openai/gpt-4o --output json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from aiod.linkage_extractor import (
    CodeLinkage,
    LiteLLMBackend,
    extract_linkages_from_paper,
)


def _format_table(linkages: list[CodeLinkage]) -> str:
    """Format linkages as a human-readable ASCII table."""
    if not linkages:
        return "No linkages found."

    # Column definitions: (header, accessor, min_width)
    columns = [
        ("Artefact ID", lambda l: l.artefact_id, 20),
        ("Type", lambda l: l.artefact_type.value, 18),
        ("Relation", lambda l: l.relation.value, 28),
        ("Confidence", lambda l: f"{l.confidence:.2f}" if l.confidence is not None else "-", 10),
        ("Comment", lambda l: l.comment or "", 30),
    ]

    # Determine column widths
    widths = []
    for header, accessor, min_w in columns:
        col_max = max(len(accessor(l)) for l in linkages)
        widths.append(max(len(header), col_max, min_w))

    # Build header
    header_line = " | ".join(
        h.ljust(w) for (h, _, _), w in zip(columns, widths)
    )
    separator = "-+-".join("-" * w for w in widths)

    # Build rows
    rows = []
    for linkage in linkages:
        row = " | ".join(
            accessor(linkage).ljust(w)
            for (_, accessor, _), w in zip(columns, widths)
        )
        rows.append(row)

    return "\n".join([header_line, separator, *rows])


def _format_json(linkages: list[CodeLinkage]) -> str:
    """Format linkages as a JSON string."""
    data = []
    for l in linkages:
        d = asdict(l)
        d["artefact_type"] = l.artefact_type.value
        d["relation"] = l.relation.value
        data.append(d)
    return json.dumps(data, indent=2)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the linkage CLI."""
    parser = argparse.ArgumentParser(
        prog="aiod.linkage_cli",
        description=(
            "Extract code artefact linkages (GitHub repos, PyPI packages) "
            "from a scientific paper using an LLM."
        ),
    )
    parser.add_argument(
        "paper",
        help=(
            "Paper identifier: file path, DOI (e.g. 10.xxx/yyy), "
            "Zenodo URL, or arbitrary URL."
        ),
    )
    parser.add_argument(
        "--model",
        required=True,
        help=(
            "LLM model identifier for litellm "
            "(e.g. 'openai/gpt-4o', 'anthropic/claude-3.5-sonnet')."
        ),
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key for the LLM provider (or set via env vars).",
    )
    parser.add_argument(
        "--api-base",
        default=None,
        help="Base URL for self-hosted LLM endpoints.",
    )
    parser.add_argument(
        "--output",
        choices=["json", "table"],
        default="table",
        help="Output format (default: table).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the linkage extraction CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    backend = LiteLLMBackend(
        model=args.model,
        api_key=args.api_key,
        api_base=args.api_base,
    )

    try:
        linkages = extract_linkages_from_paper(args.paper, backend=backend)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output == "json":
        print(_format_json(linkages))
    else:
        print(_format_table(linkages))


if __name__ == "__main__":
    main()
