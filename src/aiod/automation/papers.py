from __future__ import annotations

import json
from pathlib import Path
from threading import RLock
from typing import Any

from aiod.automation.pdf import extract_text_from_pdf
from aiod.automation.pydantic import PaperExtraction, extract_paper_metadata

PAPER_CACHE_FILE = Path(__file__).resolve().parent / "paper_cache.json"
_CACHE_LOCK = RLock()


def _ensure_paper_id(paper_id: str) -> str:
    if not isinstance(paper_id, str) or not paper_id.strip():
        raise ValueError("paper_id must be a non-empty string")
    return paper_id.strip()


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
            json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8"
        )


class Paper:
    """Cached paper metadata object with a request-time fetch API."""

    def __init__(self, paper_id: str, metadata: PaperExtraction):
        self.paper_id = _ensure_paper_id(paper_id)
        self.metadata = metadata

    def fetch(self, object_type: str, as_object: bool = True):
        object_type = object_type.strip().lower()
        if object_type not in {
            "estimators",
            "datasets",
            "metrics",
            "official_github",
            "unofficial_github",
            "pypi_packages",
            "related_code_used",
        }:
            raise ValueError(
                "object_type must be one of estimators, datasets, metrics, official_github, unofficial_github, pypi_packages, related_code_used"
            )

        if object_type == "estimators":
            result = self.metadata.artefacts.estimators
            if as_object:
                return result
            return [est.model_dump() for est in result]

        values = {
            "datasets": self.metadata.artefacts.datasets,
            "metrics": self.metadata.artefacts.metrics,
            "official_github": self.metadata.official_github,
            "unofficial_github": self.metadata.unofficial_github,
            "pypi_packages": self.metadata.pypi_packages,
            "related_code_used": self.metadata.related_code_used,
        }[object_type]

        return values if as_object else list(values)

    def model_dump(self) -> dict[str, Any]:
        return self.metadata.model_dump()

    def model_dump_json(self, **kwargs: Any) -> str:
        return self.metadata.model_dump_json(**kwargs)


def _write_paper_to_cache(paper_id: str, metadata: PaperExtraction) -> None:
    paper_id = _ensure_paper_id(paper_id)
    cache = _load_cache()
    cache[paper_id] = metadata.model_dump()
    _save_cache(cache)


def populate_paper_from_text(
    paper_id: str,
    text: str,
    model_name: str = "gpt-4o-mini",
    force: bool = False,
) -> Paper:
    """Run long-form extraction (population phase) and store in cache.

    If paper_id already exists and force=False, it returns cached output.
    """
    paper_id = _ensure_paper_id(paper_id)
    if not text or not text.strip():
        raise ValueError("text must be non-empty for paper population")

    cache = _load_cache()
    if paper_id in cache and not force:
        metadata = PaperExtraction.model_validate(cache[paper_id])
        return Paper(paper_id=paper_id, metadata=metadata)

    metadata = extract_paper_metadata(text=text, model_name=model_name)
    _write_paper_to_cache(paper_id=paper_id, metadata=metadata)
    return Paper(paper_id=paper_id, metadata=metadata)


def populate_paper_from_pdf(
    paper_id: str,
    pdf_path: str,
    model_name: str = "gpt-4o-mini",
    force: bool = False,
    head_pages: int = 5,
    tail_pages: int = 3,
    max_chars: int = 60000,
) -> Paper:
    text = extract_text_from_pdf(
        pdf_path=pdf_path,
        head_pages=head_pages,
        tail_pages=tail_pages,
        max_chars=max_chars,
    )
    return populate_paper_from_text(
        paper_id=paper_id,
        text=text,
        model_name=model_name,
        force=force,
    )


def get_paper(paper_id: str) -> Paper:
    paper_id = _ensure_paper_id(paper_id)
    cache = _load_cache()
    if paper_id not in cache:
        raise KeyError(
            f"Paper with id '{paper_id}' not found in cache. Run populate_paper_from_text(...) first."
        )

    metadata = PaperExtraction.model_validate(cache[paper_id])
    return Paper(paper_id=paper_id, metadata=metadata)


def list_cached_papers() -> list[str]:
    return list(_load_cache().keys())
