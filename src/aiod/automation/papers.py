from __future__ import annotations

import json
import tempfile
from pathlib import Path
from threading import RLock
from typing import Any

import fitz
import requests

from aiod.automation.pydantic import PaperExtraction, extract_paper_metadata

PAPER_CACHE_FILE = Path(__file__).resolve().parent / "paper_cache.json"
_CACHE_LOCK = RLock()


def _load_cache() -> dict[str, dict[str, Any]]:
    with _CACHE_LOCK:
        if not PAPER_CACHE_FILE.exists():
            return {}

        try:
            data = json.loads(PAPER_CACHE_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return {}
            return data
        except Exception:
            return {}


def _save_cache(cache: dict[str, dict[str, Any]]) -> None:
    with _CACHE_LOCK:
        PAPER_CACHE_FILE.write_text(
            json.dumps(cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


class Paper:
    """Cached paper metadata object with a request-time fetch API."""

    def __init__(self, paper_id: str, metadata: PaperExtraction):
        self.paper_id = paper_id
        self.metadata = metadata

    def fetch(self, object_type: str, as_object: bool = True):
        object_type = object_type.strip().lower()

        allowed = {
            "estimators",
            "datasets",
            "metrics",
            "related_code_used",
        }

        if object_type not in allowed:
            raise ValueError(
                "object_type must be one of estimators, datasets, metrics, "
                "related_code_used"
            )
        if object_type == "estimators":
            result = self.metadata.artefacts.estimators
            return result if as_object else [est.model_dump() for est in result]

        values = {
            "datasets": self.metadata.artefacts.datasets,
            "metrics": self.metadata.artefacts.metrics,
            "related_code_used": self.metadata.related_code_used,
        }[object_type]

        return values if as_object else list(values)

    def model_dump(self) -> dict[str, Any]:
        return self.metadata.model_dump()

    def model_dump_json(self, **kwargs: Any) -> str:
        return self.metadata.model_dump_json(**kwargs)


def _write_paper_to_cache(paper_id: str, metadata: PaperExtraction) -> None:
    cache = _load_cache()
    cache[paper_id] = metadata.model_dump()
    _save_cache(cache)


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def _download_pdf(url: str) -> str:
    """Download a PDF from a URL and return local temp file path."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(response.content)
        return f.name


def _resolve_doi_to_pdf(doi: str) -> str:
    """Resolve DOI to a PDF file."""
    doi = doi.replace("doi:", "").strip()
    url = f"https://doi.org/{doi}"

    response = requests.get(url, allow_redirects=True, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")

    if "application/pdf" in content_type:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(response.content)
            return f.name

    return _download_pdf(response.url)


def populate_paper_from_pdf(
    paper_id: str,
    pdf_path: str,
    model_name: str = "gpt-4o-mini",
    force: bool = False,
) -> Paper:

    cache = _load_cache()

    if paper_id in cache and not force:
        metadata = PaperExtraction.model_validate(cache[paper_id])
        return Paper(paper_id=paper_id, metadata=metadata)

    text = extract_text_from_pdf(pdf_path)

    metadata = extract_paper_metadata(text=text, model_name=model_name)

    _write_paper_to_cache(paper_id, metadata)

    return Paper(paper_id=paper_id, metadata=metadata)


def populate_paper(
    paper_id: str,
    source: str,
    model_name: str = "gpt-4o-mini",
    force: bool = False,
) -> Paper:
    """
    Populate a paper from:
    - local PDF path
    - PDF URL
    - DOI (doi:10.xxxx/xxxxx)
    """
    source = source.strip()

    if source.lower().startswith("doi:"):
        pdf_path = _resolve_doi_to_pdf(source)

    elif source.startswith("http://") or source.startswith("https://"):
        pdf_path = _download_pdf(source)

    else:
        pdf_path = source

    return populate_paper_from_pdf(
        paper_id=paper_id,
        pdf_path=pdf_path,
        model_name=model_name,
        force=force,
    )


def get_paper(paper_id: str) -> Paper:
    cache = _load_cache()

    if paper_id not in cache:
        # If doi-style id is provided, attempt auto-population from DOI.
        if isinstance(paper_id, str) and paper_id.strip().lower().startswith("doi:"):
            return populate_paper(paper_id=paper_id, source=paper_id)

        raise KeyError(
            f"Paper '{paper_id}' not found in cache. Run populate_paper(...) first."
        )

    metadata = PaperExtraction.model_validate(cache[paper_id])

    return Paper(paper_id=paper_id, metadata=metadata)


def list_cached_papers() -> list[str]:
    return list(_load_cache().keys())
