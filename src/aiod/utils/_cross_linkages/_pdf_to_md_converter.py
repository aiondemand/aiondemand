"""Utility for converting PDF to Markdown."""

from pathlib import Path

from skbase.utils.dependencies import _check_soft_dependencies, _safe_import


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
    _check_soft_dependencies("markitdown", severity="error")

    MarkItDown = _safe_import("markitdown.MarkItDown", pkg_name="markitdown")

    converter = MarkItDown()
    result = converter.convert(str(pdf_path))

    text = str(result)

    return text
