"""Zenodo document downloader implementation."""

import asyncio
import re
from pathlib import Path

import httpx

from aiod.cross_linkages.paper_ingestion.paper_downloader._base import BaseDownloader


class ZenodoDownloader(BaseDownloader):
    """Downloader for fetching PDFs from Zenodo records.

    This downloader extracts the record ID from a Zenodo URL,
    queries the Zenodo API, and downloads the first available PDF.

    Supported URL formats
    ---------------------
    - https://zenodo.org/records/<id>
    - https://zenodo.org/record/<id>
    """

    BASE_API = "https://zenodo.org/api/records"

    def __init__(self):
        super().__init__()

    def _extract_record_id(self, url: str) -> str:
        """Extract Zenodo record ID from URL.

        Parameters
        ----------
        url : str
            Zenodo record URL.

        Returns
        -------
        str
            Extracted record ID.

        Raises
        ------
        ValueError
            If the URL is not a valid Zenodo record URL.
        """
        match = re.search(r"zenodo\.org/(?:record|records)/(\d+)", url)
        if not match:
            raise ValueError(f"Invalid Zenodo URL: {url}")
        return match.group(1)

    async def _get_pdf_url(self, record_id: str) -> str:
        """Fetch the direct PDF URL from Zenodo API.

        Parameters
        ----------
        record_id : str
            Zenodo record identifier.

        Returns
        -------
        str
            Direct download URL for the PDF file.

        Raises
        ------
        ValueError
            If no PDF file is found in the record.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_API}/{record_id}")
            response.raise_for_status()
            data = response.json()

            for file in data.get("files", []):
                if file["key"].endswith(".pdf"):
                    return file["links"]["self"]

        raise ValueError(f"No PDF found for record {record_id}")

    async def download(
        self,
        url: str,
        output_dir: Path,
        retries: int = 3,
    ) -> Path:
        """Download a PDF from a Zenodo URL.

        Parameters
        ----------
        url : str
            Zenodo record URL.
        output_dir : Path
            Directory where the PDF will be saved.
        retries : int, default=3
            Number of retry attempts.

        Returns
        -------
        Path
            Path to the downloaded PDF file.

        Raises
        ------
        RuntimeError
            If download fails after all retry attempts.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        record_id = self._extract_record_id(url)
        pdf_url = await self._get_pdf_url(record_id)

        output_path = output_dir / f"{record_id}.pdf"

        for attempt in range(1, retries + 1):
            try:
                async with httpx.AsyncClient() as client:
                    async with client.stream("GET", pdf_url) as response:
                        response.raise_for_status()

                        with open(output_path, "wb") as f:
                            async for chunk in response.aiter_bytes():
                                f.write(chunk)

                return output_path

            except Exception as exc:
                if attempt == retries:
                    raise RuntimeError(
                        f"Download failed after {retries} attempts"
                    ) from exc

                await asyncio.sleep(2**attempt)

        raise RuntimeError("Unreachable state")
