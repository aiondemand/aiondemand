"""Pipeline orchestrating download and conversion."""

from pathlib import Path

from skbase.base import BaseObject

from aiod.cross_linkages.paper_ingestion.converter import DocumentConverter
from aiod.cross_linkages.paper_ingestion.paper_downloader import BaseDownloader


class IngestionPipeline(BaseObject):
    """Pipeline for document ingestion.

    This class orchestrates downloading a document and converting it
    into a target format using injected strategies.
    """

    def __init__(
        self,
        downloader: BaseDownloader,
        converter: DocumentConverter,
    ):
        self.downloader = downloader
        self.converter = converter
        super().__init__()

    async def run(
        self,
        url: str,
        download_dir: Path,
        output_dir: Path,
        retries: int = 3,
    ) -> Path:
        """Execute the ingestion pipeline.

        Parameters
        ----------
        url : str
            Source URL of the document.
        download_dir : Path
            Directory to store downloaded files.
        output_dir : Path
            Directory to store converted files.
        retries : int, default=3
            Number of retry attempts for downloading.

        Returns
        -------
        Path
            Path to the converted document.
        """
        pdf_path = await self.downloader.download(url, download_dir, retries)
        return self.converter.convert(pdf_path, output_dir)
