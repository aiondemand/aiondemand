"""Utilities for extracting and classifying code artefact linkages from papers.

This module is intentionally **backend-agnostic**: it defines a small interface
(``LLMBackend``) that you can implement for any concrete LLM provider
(OpenAI, Anthropic, local models, etc.).  The high-level orchestration
(``extract_linkages_from_paper``) only depends on that interface.

The primary workflow is:

1. Resolve a paper identifier (Zenodo link, DOI, local PDF path, or raw text)
   into plain text.
2. Call an ``LLMBackend`` implementation to turn that text into structured
   ``CodeLinkage`` objects containing:
   - which artefact (e.g. GitHub repo or PyPI package),
   - what kind of artefact it is,
   - how it relates to the paper (official implementation, used in experiments,
     etc.),
   - and optional comments.
"""

from __future__ import annotations

import json
import re
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class RelationType(str, Enum):
    """Relation between a paper and a code artefact."""

    OFFICIAL_IMPLEMENTATION = "official_implementation"
    """Official implementation of an algorithm proposed in the paper."""

    UNOFFICIAL_IMPLEMENTATION = "unofficial_implementation"
    """Community / third-party implementation of an algorithm in the paper."""

    CODE_USED_IN_EXPERIMENTS = "code_used_in_experiments"
    """Code that is used (e.g. as a baseline or framework) in the experiments."""

    CODE_CITED_NOT_USED = "code_cited_not_used"
    """Code that is only cited, not actually used in experiments."""

    OTHER = "other"
    """Any other relation not covered by the above."""


class ArtefactType(str, Enum):
    """Types of artefacts we link to."""

    GITHUB_REPOSITORY = "github_repository"
    PYPI_PACKAGE = "pypi_package"
    OTHER = "other"


@dataclass
class CodeLinkage:
    """Structured description of a paper-code linkage."""

    artefact_id: str
    """Identifier of the artefact (e.g. 'owner/repo' or 'package-name')."""

    artefact_type: ArtefactType
    """What kind of artefact this is (GitHub repo, PyPI package, etc.)."""

    relation: RelationType
    """How the artefact relates to the paper."""

    comment: str | None = None
    """Optional free-form explanation by the LLM."""

    confidence: float | None = None
    """Optional confidence score in [0, 1]."""


# Simple list kept for compatibility / easier prompting
RELATION_CATEGORIES: List[str] = [r.value for r in RelationType]


# ---------------------------------------------------------------------------
# Shared prompt/parsing helpers
# ---------------------------------------------------------------------------


def _build_extraction_prompt(paper_text: str) -> str:
    """Build a backend-agnostic prompt describing the desired JSON schema."""
    relation_desc = textwrap.dedent("""\
        Relation categories you MUST use (field "relation"):

        - "official_implementation": official implementation of an algorithm proposed in the paper
        - "unofficial_implementation": third-party implementation of an algorithm from the paper
        - "code_used_in_experiments": code used in experiments (e.g. baselines, frameworks, libraries)
        - "code_cited_not_used": code that is only cited or discussed, not actually used
        - "other": any other relation
    """).strip()

    schema_desc = textwrap.dedent("""\
        Return a JSON array. Each element MUST have this shape:

        {
          "artefact_id": "string, e.g. 'owner/repo' or 'package-name'",
          "artefact_type": "github_repository | pypi_package | other",
          "relation": "one of official_implementation | unofficial_implementation | code_used_in_experiments | code_cited_not_used | other",
          "comment": "optional short natural-language explanation",
          "confidence": 0.0-1.0 optional numeric confidence
        }

        Only include artefacts that you believe are truly related to the paper.
    """).strip()

    instructions = textwrap.dedent(f"""\
        You are an expert in scientific software discovery.

        Given the full text of a scientific paper, identify GitHub repositories
        and Python packages (PyPI identifiers) that are related to the paper.

        - Prefer artefacts that are official or clearly linked in the text
          (e.g. in "Code availability" sections, footnotes, or URLs).
        - Also include well-known libraries that are central to the experiments.
        - Distinguish between official vs unofficial implementations and
          between code that is actually used vs only cited.

        {relation_desc}

        {schema_desc}

        Reply with JSON ONLY. Do not include any explanation outside the JSON.
    """).strip()

    return instructions + "\n\nPaper text:\n" + paper_text


def _parse_linkage_response(response: str) -> List[CodeLinkage]:
    """Parse an LLM JSON response into ``CodeLinkage`` objects.

    Handles common quirks like markdown fences around the JSON.
    """
    cleaned = response.strip()

    # Strip markdown code fences if present (```json ... ```)
    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response is not valid JSON") from exc

    if not isinstance(data, list):
        raise ValueError("LLM response JSON must be a list")

    results: List[CodeLinkage] = []
    for item in data:
        if not isinstance(item, dict):
            continue

        artefact_id = str(item.get("artefact_id", "")).strip()
        if not artefact_id:
            continue

        artefact_type_raw = str(item.get("artefact_type", "other"))
        try:
            artefact_type = ArtefactType(artefact_type_raw)
        except ValueError:
            artefact_type = ArtefactType.OTHER

        relation_raw = str(item.get("relation", RelationType.OTHER.value))
        try:
            relation = RelationType(relation_raw)
        except ValueError:
            relation = RelationType.OTHER

        comment_val = item.get("comment")
        comment = str(comment_val).strip() if comment_val is not None else None
        if comment == "":
            comment = None

        confidence_val = item.get("confidence")
        confidence: Optional[float]
        try:
            confidence = float(confidence_val)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            confidence = None

        results.append(
            CodeLinkage(
                artefact_id=artefact_id,
                artefact_type=artefact_type,
                relation=relation,
                comment=comment,
                confidence=confidence,
            )
        )

    return results


# ---------------------------------------------------------------------------
# LLM backends
# ---------------------------------------------------------------------------


class LLMBackend(ABC):
    """Abstract base class for LLM backends.

    Implementations should:

    - take raw paper text,
    - run a prompt against an LLM,
    - and return a list of :class:`CodeLinkage` instances.
    """

    @abstractmethod
    def extract_linkages(self, paper_text: str) -> List[CodeLinkage]:
        """Return code linkages for a given paper."""


class TextCompletionBackend(LLMBackend):
    """Backend that wraps a simple text-completion style interface.

    Parameters
    ----------
    generator:
        Callable that takes a prompt and returns a string response. This can be
        backed by any provider (OpenAI, Anthropic, local LLM, etc.).
    """

    def __init__(self, generator: Callable[[str], str]) -> None:
        self._generator = generator

    def extract_linkages(self, paper_text: str) -> List[CodeLinkage]:
        """Extract linkages by calling the generator with a structured prompt."""
        prompt = _build_extraction_prompt(paper_text)
        raw = self._generator(prompt)
        return _parse_linkage_response(raw)


class LiteLLMBackend(LLMBackend):
    """Backend powered by `litellm <https://docs.litellm.ai/>`_.

    ``litellm`` provides a unified interface to 100+ LLM providers.  Pass any
    model string that ``litellm`` supports (e.g. ``"openai/gpt-4o"``,
    ``"anthropic/claude-3.5-sonnet"``, ``"ollama/llama3"``).

    Parameters
    ----------
    model:
        The model identifier, following litellm naming conventions.
    api_key:
        Optional API key.  If *None*, litellm falls back to environment
        variables (e.g. ``OPENAI_API_KEY``).
    api_base:
        Optional base URL, useful for self-hosted endpoints.
    completion_kwargs:
        Additional keyword arguments forwarded to ``litellm.completion``.
    """

    def __init__(
        self,
        model: str,
        *,
        api_key: str | None = None,
        api_base: str | None = None,
        completion_kwargs: Dict[str, Any] | None = None,
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.completion_kwargs: Dict[str, Any] = completion_kwargs or {}

    def extract_linkages(self, paper_text: str) -> List[CodeLinkage]:
        """Extract linkages using a litellm-supported model."""
        try:
            import litellm  # type: ignore[import-untyped]
        except ImportError as exc:
            raise RuntimeError(
                "The 'litellm' package is required for LiteLLMBackend. "
                "Install it with: pip install litellm"
            ) from exc

        prompt = _build_extraction_prompt(paper_text)

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            **self.completion_kwargs,
        }
        if self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if self.api_base is not None:
            kwargs["api_base"] = self.api_base

        response = litellm.completion(**kwargs)
        raw_text: str = response.choices[0].message.content  # type: ignore[union-attr]
        return _parse_linkage_response(raw_text)


class OpenAIBackend(LLMBackend):
    """Example backend placeholder for OpenAI or compatible APIs.

    This is intentionally left unimplemented so that this package does not
    depend on any specific LLM provider.  You can implement this class in your
    own codebase by calling the provider of your choice and returning
    :class:`CodeLinkage` instances.
    """

    def extract_linkages(self, paper_text: str) -> List[CodeLinkage]:
        """Raise ``NotImplementedError`` — implement in downstream code."""
        raise NotImplementedError(
            "OpenAIBackend is a placeholder. Implement it in your application "
            "using your preferred OpenAI client and return `CodeLinkage` objects."
        )


# ---------------------------------------------------------------------------
# Paper text retrieval
# ---------------------------------------------------------------------------

# Regex patterns for identifier detection
_DOI_RE = re.compile(r"^10\.\d{4,9}/[^\s]+$")
_ZENODO_RE = re.compile(
    r"https?://zenodo\.org/records?/(\d+)", re.IGNORECASE
)


def retrieve_paper_text(paper_identifier: str | Path) -> str:
    """Resolve a paper identifier into plain text.

    Supported identifiers (checked in order):

    1. **Local file path** — if ``paper_identifier`` points to an existing file:
       - ``.pdf`` files are read with ``pypdf`` (optional dependency).
       - Everything else is read as UTF-8 text.
    2. **Zenodo URL** (e.g. ``https://zenodo.org/records/12345``):
       fetches record metadata via the Zenodo API, finds the first PDF file,
       downloads it, and extracts text.
    3. **DOI** (e.g. ``10.48550/arXiv.2307.09288``):
       resolves via ``https://doi.org/<doi>``.  If the DOI leads to Zenodo the
       Zenodo path is used; otherwise plain-text / HTML content is returned.
    4. **Arbitrary HTTPS URL**: downloads the resource; PDF content-types are
       extracted with ``pypdf``; HTML is stripped to text via ``BeautifulSoup``.
    5. **Raw text** — if none of the above match, the string is returned as-is.
    """
    identifier = str(paper_identifier).strip()

    # 1. Local file -------------------------------------------------------
    path = Path(identifier)
    if path.exists():
        return _read_local_file(path)

    # 2. Zenodo URL -------------------------------------------------------
    zenodo_match = _ZENODO_RE.search(identifier)
    if zenodo_match:
        record_id = zenodo_match.group(1)
        return _fetch_zenodo_record(record_id)

    # 3. DOI --------------------------------------------------------------
    if _DOI_RE.match(identifier):
        return _resolve_doi(identifier)

    # 4. Arbitrary URL ----------------------------------------------------
    if identifier.startswith(("http://", "https://")):
        return _fetch_url(identifier)

    # 5. Raw text ---------------------------------------------------------
    return identifier


def _read_local_file(path: Path) -> str:
    """Read a local file as text, using ``pypdf`` for PDFs."""
    if path.suffix.lower() == ".pdf":
        try:
            import pypdf  # type: ignore[import-untyped]
        except ImportError as exc:
            raise RuntimeError(
                "PDF support requires the optional 'pypdf' dependency. "
                "Install it with `pip install pypdf`."
            ) from exc

        reader = pypdf.PdfReader(str(path))
        texts: Iterable[str] = (
            page.extract_text() or "" for page in reader.pages
        )
        return "\n\n".join(texts)

    return path.read_text(encoding="utf-8")


def _fetch_zenodo_record(record_id: str) -> str:
    """Fetch the first PDF from a Zenodo record and extract its text."""
    import requests  # already a project dependency

    api_url = f"https://zenodo.org/api/records/{record_id}"
    resp = requests.get(api_url, timeout=30)
    resp.raise_for_status()
    metadata = resp.json()

    # Find the first PDF file in the record
    pdf_url: str | None = None
    for f in metadata.get("files", []):
        if f.get("key", "").lower().endswith(".pdf"):
            # Prefer the direct download link
            pdf_url = f.get("links", {}).get("self")
            if not pdf_url:
                # Fallback: construct from bucket
                pdf_url = f"https://zenodo.org/records/{record_id}/files/{f['key']}"
            break

    if pdf_url is None:
        raise ValueError(
            f"No PDF file found in Zenodo record {record_id}. "
            "Please provide a direct PDF link or the paper text."
        )

    return _download_and_extract_pdf(pdf_url)


def _resolve_doi(doi: str) -> str:
    """Resolve a DOI to paper text.

    If the DOI redirects to Zenodo, falls back to the Zenodo path.
    Otherwise tries to fetch plain-text or HTML content.
    """
    import requests

    doi_url = f"https://doi.org/{doi}"

    # First, follow redirects to see where the DOI points
    head_resp = requests.head(doi_url, allow_redirects=True, timeout=30)
    final_url = head_resp.url

    # If it redirects to Zenodo, use the Zenodo path
    zenodo_match = _ZENODO_RE.search(final_url)
    if zenodo_match:
        return _fetch_zenodo_record(zenodo_match.group(1))

    # Otherwise, try to fetch content
    return _fetch_url(final_url)


def _fetch_url(url: str) -> str:
    """Download a URL and extract text.

    - PDF content-types are processed with ``pypdf``.
    - HTML is stripped to plain text with ``BeautifulSoup`` (optional dep).
    - Everything else is returned as-is.
    """
    import requests

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "").lower()

    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        return _extract_pdf_from_bytes(resp.content)

    if "text/html" in content_type:
        return _html_to_text(resp.text)

    # Fallback: plain text
    return resp.text


def _download_and_extract_pdf(url: str) -> str:
    """Download a PDF from *url* and extract its text."""
    import requests

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return _extract_pdf_from_bytes(resp.content)


def _extract_pdf_from_bytes(pdf_bytes: bytes) -> str:
    """Extract text from raw PDF bytes using ``pypdf``."""
    import io

    try:
        import pypdf  # type: ignore[import-untyped]
    except ImportError as exc:
        raise RuntimeError(
            "PDF support requires the optional 'pypdf' dependency. "
            "Install it with `pip install pypdf`."
        ) from exc

    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    texts: Iterable[str] = (
        page.extract_text() or "" for page in reader.pages
    )
    return "\n\n".join(texts)


def _html_to_text(html: str) -> str:
    """Strip HTML tags and return plain text.

    Uses ``BeautifulSoup`` if available, else falls back to a naive regex strip.
    """
    try:
        from bs4 import BeautifulSoup  # type: ignore[import-untyped]

        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except ImportError:
        # Naive fallback: strip tags with regex
        return re.sub(r"<[^>]+>", "", html)


# ---------------------------------------------------------------------------
# High-level orchestration
# ---------------------------------------------------------------------------


def extract_linkages_from_paper(
    paper_identifier: str | Path,
    backend: Optional[LLMBackend] = None,
) -> List[CodeLinkage]:
    """Extract and classify code artefact linkages for a given paper.

    Parameters
    ----------
    paper_identifier:
        One of:

        - local PDF path,
        - local plain-text path,
        - Zenodo URL (e.g. ``https://zenodo.org/records/12345``),
        - DOI string (e.g. ``10.48550/arXiv.2307.09288``),
        - arbitrary HTTPS URL,
        - raw paper text (if it does not correspond to an existing file).

    backend:
        Implementation of :class:`LLMBackend`.  If omitted, you must provide
        one yourself; this function does **not** assume a default service.

    Returns
    -------
    list[CodeLinkage]
        Structured linkages between the paper and code artefacts.
    """
    paper_text = retrieve_paper_text(paper_identifier)
    if backend is None:
        raise ValueError(
            "No LLM backend provided. Pass an implementation of `LLMBackend`, "
            "e.g. `TextCompletionBackend` or `LiteLLMBackend`."
        )

    return backend.extract_linkages(paper_text)


def extract_linkages_from_text(
    paper_text: str,
    backend: LLMBackend,
) -> List[CodeLinkage]:
    """Convenience wrapper when you already have the paper text."""
    return backend.extract_linkages(paper_text)
