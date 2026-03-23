"""Paper ingestion pipeline for downloading and converting papers."""

from aiod.cross_linkages.paper_ingestion.converter import (
    DocumentConverter,
    MarkitDownConverter,
)
from aiod.cross_linkages.paper_ingestion.ingestion import IngestionPipeline
from aiod.cross_linkages.paper_ingestion.paper_downloader import (
    BaseDownloader,
    ZenodoDownloader,
)

__all__ = [
    "BaseDownloader",
    "ZenodoDownloader",
    "DocumentConverter",
    "MarkitDownConverter",
    "IngestionPipeline",
]
