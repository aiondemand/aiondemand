"""Utility for converting PDF to Markdown."""

from pathlib import Path

from skbase.utils.dependencies import _safe_import

MarkItDown = _safe_import("markitdown.MarkItDown", pkg_name="markitdown")


def pdf_to_markdown(pdf_path: Path) -> str:
    """Convert a PDF file to Markdown.

    Parameters
    ----------
    pdf_path : Path
        Path to PDF file.

    Returns
    -------
    str
        Markdown content extracted from PDF.
    """
    converter = MarkItDown()
    result = converter.convert(str(pdf_path))

    text = result.text_content

    if not isinstance(text, str):
        raise TypeError(f"Expected string output, got {type(text)}")

    return text
