"""Markdown converter using Microsoft MarkItDown."""

from pathlib import Path

from markitdown import MarkItDown

from aiod.cross_linkages.paper_ingestion.converter._base import DocumentConverter


class MarkitDownConverter(DocumentConverter):
    """Convert PDF documents to Markdown using MarkItDown."""

    def __init__(self):
        self._converter = MarkItDown()
        super().__init__()

    def convert(self, input_path: Path, output_dir: Path) -> Path:
        """Convert PDF to Markdown.

        Parameters
        ----------
        input_path : Path
            Path to PDF file.
        output_dir : Path
            Output directory for Markdown file.

        Returns
        -------
        Path
            Path to generated Markdown file.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{input_path.stem}.md"

        result = self._converter.convert(str(input_path))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)

        return output_path
