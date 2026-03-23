"""Document downloaders for paper ingestion."""

from aiod.cross_linkages.paper_ingestion.paper_downloader._base import BaseDownloader
from aiod.cross_linkages.paper_ingestion.paper_downloader.zenodo import ZenodoDownloader

__all__ = ["BaseDownloader", "ZenodoDownloader"]
