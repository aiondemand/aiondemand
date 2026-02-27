"""CLI entry point for the crosslinker extraction pipeline.

Usage
-----
::

    # Demo mode (hardcoded abstract):
    aiod-crosslink

    # Extract from a local PDF:
    aiod-crosslink --pdf paper.pdf

    # Extract from a DOI (auto-downloads PDF):
    aiod-crosslink --doi 10.5281/zenodo.4106480

    # Extract from a Zenodo or arxiv URL:
    aiod-crosslink --url https://zenodo.org/records/4106480
    aiod-crosslink --url https://arxiv.org/abs/1810.04805

    # Save output to file:
    aiod-crosslink --pdf paper.pdf --output result.json

See Also
--------
aiod.crosslinker : Core extraction logic.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import pathlib
import sys

from pydantic import ValidationError

from aiod.crosslinker import (
    _DEFAULT_MODEL,
    ExtractionResult,
    extract_from_doi,
    extract_from_pdf,
    extract_from_text,
    extract_from_url,
)

_SAMPLE_ABSTRACT: str = (
    "We present SciMapper, a novel framework for mapping scientific "
    "literature to software artefacts.  Our official implementation is "
    "available at https://github.com/scimapper/scimapper.  We benchmark "
    "against the approach of M\u00fcller et al., whose unofficial re-"
    "implementation can be found at "
    "https://github.com/jdoe/muller-reimpl.  "
    "The pipeline is built on PyTorch "
    "(https://github.com/pytorch/pytorch) "
    "and HuggingFace Transformers, installable via ``pip install "
    "transformers``.  We additionally use scikit-learn for evaluation "
    "metrics and Pandas for data wrangling.  Our training dataset is "
    "archived on Zenodo at https://zenodo.org/record/1234567.  We also "
    "cite the GROBID library (https://github.com/kermitt2/grobid) for "
    "reference parsing, although it is not used directly in our "
    "experiments.  All experiments were tracked with Weights & Biases."
)


def _build_cli() -> argparse.ArgumentParser:
    """Construct the argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="aiod-crosslink",
        description=("Extract code-to-publication linkages from a scientific paper."),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--pdf",
        type=str,
        default=None,
        help="Path to a local PDF file.",
    )
    group.add_argument(
        "--text",
        type=str,
        default=None,
        help="Path to a plain-text file.",
    )
    group.add_argument(
        "--doi",
        type=str,
        default=None,
        help=("DOI to resolve and download (e.g. 10.5281/zenodo.4106480)."),
    )
    group.add_argument(
        "--url",
        type=str,
        default=None,
        help="Zenodo or arxiv URL to download and extract from.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help=("Path to save JSON result (default: print to stdout)."),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=(
            "LiteLLM model identifier, overrides the "
            "LLM_MODEL env var "
            f"(default: {_DEFAULT_MODEL})."
        ),
    )
    return parser


async def _async_main() -> None:
    """Run the extraction pipeline from CLI arguments."""
    parser = _build_cli()
    args = parser.parse_args()

    model: str = args.model if args.model is not None else _DEFAULT_MODEL

    try:
        if args.pdf is not None:
            pdf_path = pathlib.Path(args.pdf)
            if not pdf_path.is_file():
                msg = f"PDF file not found: {pdf_path}"
                raise FileNotFoundError(msg)
            sys.stderr.write(f"[source] PDF: {pdf_path}\n")
            result: ExtractionResult = await extract_from_pdf(
                str(pdf_path), model=model
            )

        elif args.text is not None:
            text_path = pathlib.Path(args.text)
            if not text_path.is_file():
                msg = f"Text file not found: {text_path}"
                raise FileNotFoundError(msg)
            sys.stderr.write(f"[source] Text file: {text_path}\n")
            text = text_path.read_text(encoding="utf-8")
            result = await extract_from_text(text, model=model)

        elif args.doi is not None:
            sys.stderr.write(f"[source] DOI: {args.doi}\n")
            result = await extract_from_doi(args.doi, model=model)

        elif args.url is not None:
            sys.stderr.write(f"[source] URL: {args.url}\n")
            result = await extract_from_url(args.url, model=model)

        else:
            sys.stderr.write("[source] Built-in demo abstract\n")
            result = await extract_from_text(_SAMPLE_ABSTRACT, model=model)

    except (FileNotFoundError, RuntimeError) as exc:
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)

    sys.stderr.write(f"[model] {model}\n")

    try:
        output_json: str = json.dumps(result.model_dump(), indent=2)
    except (ValueError, ValidationError) as exc:
        sys.stderr.write(f"\nExtraction failed: {exc}\n")
        sys.exit(1)

    if args.output is not None:
        out_path = pathlib.Path(args.output)
        out_path.write_text(output_json + "\n", encoding="utf-8")
        sys.stderr.write(f"[saved] {out_path}\n")
    else:
        sys.stdout.write(output_json + "\n")


def main() -> None:
    """Run the CLI extraction pipeline synchronously."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
