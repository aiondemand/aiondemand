"""Document converters for paper ingestion."""

from aiod.cross_linkages.paper_ingestion.converter._base import DocumentConverter
from aiod.cross_linkages.paper_ingestion.converter.markitdown import MarkitDownConverter

__all__ = ["DocumentConverter", "MarkitDownConverter"]
