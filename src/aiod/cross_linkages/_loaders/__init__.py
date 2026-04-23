"""Paper Loaders."""

from aiod.cross_linkages._loaders._base import BaseLoader
from aiod.cross_linkages._loaders._zenodo import ZenodoLoader

__all__ = ["BaseLoader", "ZenodoLoader"]
