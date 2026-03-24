"""Zenodo document loader."""

import re
from pathlib import Path

import httpx
from skbase.utils.dependencies import _safe_import

from aiod.cross_linkages._loaders._base import BaseLoader
from aiod.utils._cross_linkages import pdf_to_markdown

Document = _safe_import("langchain_core.documents.Document", pkg_name="langchain")


class ZenodoLoader(BaseLoader):
    """Loader for Zenodo papers.

    Parameters
    ----------
    download_dir : Path
        Directory to download PDF files to.
        Defaults to "data/pdfs".

    Returns
    -------
    List[Document]
        List containing Langchain Document wrapping the paper content and metadata.
    """

    _tags = {
        "python_dependencies": [
            "langchain",
            "markitdown",
        ],
    }

    BASE_API = "https://zenodo.org/api/records"

    def __init__(self, download_dir: Path = Path("data/pdfs")):
        self.download_dir = download_dir
        super().__init__()

    def _extract_record_id(self, url: str) -> str:
        """Extract record ID from Zenodo URL."""
        match = re.search(r"zenodo\.org/(?:record|records)/(\d+)", url)
        if not match:
            raise ValueError(f"Invalid Zenodo URL: {url}")
        return match.group(1)

    def _get_pdf_url(self, record_id: str) -> str:
        """Fetch PDF URL from Zenodo API."""
        with httpx.Client() as client:
            response = client.get(f"{self.BASE_API}/{record_id}")
            response.raise_for_status()
            data = response.json()

        for file in data.get("files", []):
            if file["key"].endswith(".pdf"):
                return file["links"]["self"]

        raise ValueError(f"No PDF found for record {record_id}")

    def _download_pdf(
        self,
        pdf_url: str,
        output_path: Path,
        retries: int = 3,
    ) -> Path:
        """Download PDF with retry logic."""
        for attempt in range(1, retries + 1):
            try:
                with httpx.Client() as client:
                    with client.stream("GET", pdf_url) as response:
                        response.raise_for_status()

                        output_path.parent.mkdir(parents=True, exist_ok=True)

                        with open(output_path, "wb") as f:
                            for chunk in response.iter_bytes():
                                f.write(chunk)

                return output_path

            except Exception as exc:
                if attempt == retries:
                    raise RuntimeError(
                        f"Download failed after {retries} attempts"
                    ) from exc

        raise RuntimeError("Unreachable")

    def load(self, url: str):
        """Load Zenodo paper into LangChain Documents.

        Parameters
        ----------
        url : str
            Zenodo record URL.

        Returns
        -------
        List[Document]
            List containing one Document with full paper content.
        """
        record_id = self._extract_record_id(url)
        pdf_url = self._get_pdf_url(record_id)

        pdf_path = self.download_dir / f"{record_id}.pdf"
        self._download_pdf(pdf_url, pdf_path)

        markdown = pdf_to_markdown(pdf_path)

        return [
            Document(
                page_content=markdown,
                metadata={
                    "source": url,
                    "record_id": record_id,
                },
            )
        ]
