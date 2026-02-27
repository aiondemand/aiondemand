"""Extract code-to-publication linkages from scientific papers via LLM.

This module provides functions to extract GitHub repositories, PyPI
packages, and datasets from scientific papers and classify each artifact
by its relation to the paper.  It supports local PDFs, raw text, DOIs,
and Zenodo/arxiv URLs as input.

The extraction pipeline has two stages:

1. **Deterministic** — regex-based extraction of GitHub, Zenodo, and
   PyPI URLs directly from the text.
2. **LLM classification** — an LLM classifies each artifact into one of
   the four relation categories defined in issue #104.

See Also
--------
aiod.crosslink_cli : CLI entry point for this module.
"""

from __future__ import annotations

import asyncio
import json
import os
import random
import re
import sys
import tempfile
import urllib.error
import urllib.request
from enum import Enum
from typing import Any

import litellm
from pydantic import BaseModel, Field, ValidationError

_DEFAULT_MODEL: str = os.environ.get("LLM_MODEL", "openai/gpt-4o-mini")
"""LiteLLM model identifier — override via ``LLM_MODEL`` env var."""

_MAX_RETRIES: int = 3
"""Number of retry attempts on transient API or parse failures."""

_MAX_CHARS: int = 60_000
"""Maximum characters sent to the LLM (~15k tokens for gpt-4o-mini)."""

_MAX_PDF_BYTES: int = 50 * 1024 * 1024  # 50 MB
"""Reject PDFs larger than this to prevent memory issues."""

_MAX_PDF_PAGES: int = 200
"""Reject PDFs with more pages than this."""


# ---------------------------------------------------------------------------
# Schema — maps exactly to issue #104's four relation categories
# ---------------------------------------------------------------------------


class RelationType(str, Enum):
    """Relation between a paper and a code artefact (issue #104).

    Attributes
    ----------
    OFFICIAL_IMPLEMENTATION
        Official implementation of an algorithm proposed in the paper.
    UNOFFICIAL_IMPLEMENTATION
        Third-party / community re-implementation.
    USED_IN_EXPERIMENTS
        Code used in experiments but algorithm is not proposed in
        the paper (e.g. baseline frameworks, libraries).
    CITED_NOT_USED
        Cited or discussed but not directly used in experiments.
    """

    OFFICIAL_IMPLEMENTATION = "official_implementation"
    UNOFFICIAL_IMPLEMENTATION = "unofficial_implementation"
    USED_IN_EXPERIMENTS = "used_in_experiments"
    CITED_NOT_USED = "cited_not_used"


class ArtefactType(str, Enum):
    """Type of code artefact linked to a paper.

    Attributes
    ----------
    GITHUB_REPOSITORY
        A GitHub (or GitLab) repository URL.
    PYPI_PACKAGE
        A pip-installable Python package name.
    DATASET
        A named dataset or download link.
    OTHER
        Any other artefact type.
    """

    GITHUB_REPOSITORY = "github_repository"
    PYPI_PACKAGE = "pypi_package"
    DATASET = "dataset"
    OTHER = "other"


class CodeLinkage(BaseModel):
    """A single paper-to-artefact linkage with classification.

    Attributes
    ----------
    artefact_id : str
        Identifier (URL, package name, or dataset name).
    artefact_type : ArtefactType
        What kind of artefact this is.
    relation : RelationType
        How the artefact relates to the paper.
    comment : str or None
        Optional explanation from the LLM.
    """

    artefact_id: str = Field(
        description="Identifier: URL, package name, or dataset name.",
    )
    artefact_type: str = Field(
        description=("One of: github_repository, pypi_package, dataset, other."),
    )
    relation: str = Field(
        description=(
            "One of: official_implementation, "
            "unofficial_implementation, "
            "used_in_experiments, cited_not_used."
        ),
    )
    comment: str | None = Field(
        default=None,
        description="Optional short explanation.",
    )


class ExtractionResult(BaseModel):
    """Structured output from the linkage extraction pipeline.

    A single flat array of typed, classified artefacts.  Datasets,
    repositories, and packages all live in the same ``linkages`` list,
    distinguished by ``artefact_type``.

    Attributes
    ----------
    linkages : list[CodeLinkage]
        Per-artefact classified linkages.
    """

    linkages: list[CodeLinkage] = Field(
        default_factory=list,
        description="Per-artefact classified linkages.",
    )

    def deduplicated(self) -> ExtractionResult:
        """Return a copy with duplicate artefact IDs removed."""
        seen: set[str] = set()
        unique: list[CodeLinkage] = []
        for linkage in self.linkages:
            key = linkage.artefact_id.lower()
            if key not in seen:
                seen.add(key)
                unique.append(linkage)
        return ExtractionResult(linkages=unique)


# ---------------------------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------------------------


def extract_text_from_pdf(
    path: str,
    *,
    head_pages: int = 15,
    tail_pages: int = 5,
) -> str:
    """Extract text from a PDF with head+tail priority chunking.

    Parameters
    ----------
    path : str
        Path to a local PDF file.
    head_pages : int
        Number of leading pages to always include.
    tail_pages : int
        Number of trailing pages to always include (captures references).

    Returns
    -------
    str
        Extracted and chunked plain text.

    Raises
    ------
    RuntimeError
        If the PDF exceeds size or page limits, or cannot be read.
    """
    import fitz  # pymupdf — lazy import so the dep is optional

    file_size = os.path.getsize(path)
    if file_size > _MAX_PDF_BYTES:
        msg = (
            f"PDF too large: {file_size / 1e6:.0f} MB "
            f"(limit {_MAX_PDF_BYTES / 1e6:.0f} MB)"
        )
        raise RuntimeError(msg)

    doc = fitz.open(path)
    n_pages = len(doc)

    if n_pages > _MAX_PDF_PAGES:
        doc.close()
        msg = f"PDF has {n_pages} pages (limit {_MAX_PDF_PAGES})"
        raise RuntimeError(msg)

    if n_pages == 0:
        doc.close()
        msg = "PDF has no pages"
        raise RuntimeError(msg)

    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    if n_pages <= head_pages + tail_pages:
        return full_text[:_MAX_CHARS]

    # Re-open for priority chunking.
    doc = fitz.open(path)
    head = "\n".join(doc[i].get_text() for i in range(head_pages))
    tail = "\n".join(doc[i].get_text() for i in range(n_pages - tail_pages, n_pages))
    doc.close()

    chunked = f"{head}\n\n[...truncated...]\n\n{tail}"
    return chunked[:_MAX_CHARS]


# ---------------------------------------------------------------------------
# Deterministic URL extraction (Stage 1)
# ---------------------------------------------------------------------------

_GITHUB_RE = re.compile(
    r"https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]*[\w]",
    re.IGNORECASE,
)
_ZENODO_RE = re.compile(r"https?://zenodo\.org/records?/\d+", re.IGNORECASE)
_PYPI_RE = re.compile(r"https?://pypi\.org/project/([\w.-]+)", re.IGNORECASE)


def extract_urls_deterministic(
    text: str,
) -> list[CodeLinkage]:
    """Extract GitHub, Zenodo, and PyPI URLs from text via regex.

    Parameters
    ----------
    text : str
        Plain text content of a paper.

    Returns
    -------
    list[CodeLinkage]
        Linkages with ``relation`` set to ``used_in_experiments``
        as a conservative default (the LLM refines this).
    """
    linkages: list[CodeLinkage] = []
    seen: set[str] = set()

    for url in _GITHUB_RE.findall(text):
        if url.lower() not in seen:
            seen.add(url.lower())
            linkages.append(
                CodeLinkage(
                    artefact_id=url,
                    artefact_type="github_repository",
                    relation="used_in_experiments",
                    comment="Detected via URL regex",
                )
            )

    for pkg in _PYPI_RE.findall(text):
        if pkg.lower() not in seen:
            seen.add(pkg.lower())
            linkages.append(
                CodeLinkage(
                    artefact_id=pkg,
                    artefact_type="pypi_package",
                    relation="used_in_experiments",
                    comment="Detected via PyPI URL regex",
                )
            )

    return linkages


# ---------------------------------------------------------------------------
# URL / DOI resolution
# ---------------------------------------------------------------------------

_USER_AGENT = "aiod-crosslink/0.1"


def _download_pdf(url: str) -> str:
    """Download a PDF from *url* into a temporary file.

    The caller is responsible for deleting the file when done.

    Parameters
    ----------
    url : str
        Direct URL to a PDF resource.

    Returns
    -------
    str
        Path to the downloaded temporary file.

    Raises
    ------
    RuntimeError
        If the download fails.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
            tmp = tempfile.NamedTemporaryFile(  # noqa: SIM115
                delete=False, suffix=".pdf"
            )
            tmp.write(resp.read())
            tmp.close()
            return tmp.name
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        msg = f"Failed to download PDF from {url}: {exc}"
        raise RuntimeError(msg) from exc


def _select_best_pdf(files: list[dict]) -> str | None:
    """Pick the best PDF from a Zenodo record's file list.

    Prefers filenames containing 'paper', 'article', or 'manuscript'.
    Falls back to the largest PDF.

    Parameters
    ----------
    files : list[dict]
        File entries from the Zenodo API response.

    Returns
    -------
    str or None
        Download URL of the best PDF, or ``None`` if no PDF found.
    """
    pdfs = [f for f in files if f.get("key", "").lower().endswith(".pdf")]
    if not pdfs:
        return None

    preferred = ["paper", "article", "manuscript"]
    for pdf in pdfs:
        name = pdf.get("key", "").lower()
        if any(kw in name for kw in preferred):
            return pdf["links"]["self"]

    # Fallback: largest PDF.
    largest = max(pdfs, key=lambda f: f.get("size", 0))
    return largest["links"]["self"]


def resolve_url_to_pdf(identifier: str, *, is_doi: bool = False) -> str:
    """Resolve a DOI, Zenodo URL, or arxiv URL to a local PDF path.

    The caller must delete the returned file when done.

    Parameters
    ----------
    identifier : str
        A DOI string, arxiv URL, or Zenodo record URL.
    is_doi : bool
        If ``True``, treat *identifier* as a bare DOI.

    Returns
    -------
    str
        Path to the downloaded temporary PDF.

    Raises
    ------
    RuntimeError
        If resolution or download fails.
    """
    if is_doi:
        identifier = f"https://doi.org/{identifier}"

    # --- arxiv --------------------------------------------------------
    arxiv_match = re.match(
        r"https?://arxiv\.org/(abs|pdf)/(\d{4}\.\d{4,5})(v\d+)?",
        identifier,
    )
    if arxiv_match:
        arxiv_id = arxiv_match.group(2)
        version = arxiv_match.group(3) or ""
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}{version}"
        sys.stderr.write(f"[resolve] arxiv \u2192 {pdf_url}\n")
        return _download_pdf(pdf_url)

    # --- Zenodo -------------------------------------------------------
    zenodo_match = re.match(r"https?://zenodo\.org/records?/(\d+)", identifier)
    if zenodo_match:
        record_id = zenodo_match.group(1)
        api_url = f"https://zenodo.org/api/records/{record_id}"
        sys.stderr.write(f"[resolve] Zenodo API \u2192 {api_url}\n")
        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": _USER_AGENT},
            )
            with urllib.request.urlopen(  # noqa: S310
                req, timeout=30
            ) as resp:
                record = json.loads(resp.read().decode())
        except (
            urllib.error.URLError,
            TimeoutError,
            OSError,
        ) as exc:
            msg = f"Zenodo API request failed: {exc}"
            raise RuntimeError(msg) from exc

        pdf_link = _select_best_pdf(record.get("files", []))
        if pdf_link is None:
            msg = f"No PDF found in Zenodo record {record_id}"
            raise RuntimeError(msg)

        sys.stderr.write(f"[resolve] Found PDF: {pdf_link}\n")
        return _download_pdf(pdf_link)

    # --- DOI (generic redirect) ---------------------------------------
    if identifier.startswith("https://doi.org/") or is_doi:
        sys.stderr.write(f"[resolve] DOI redirect \u2192 {identifier}\n")
        try:
            req = urllib.request.Request(
                identifier,
                headers={
                    "User-Agent": _USER_AGENT,
                    "Accept": "application/pdf",
                },
            )
            with urllib.request.urlopen(  # noqa: S310
                req, timeout=30
            ) as resp:
                final_url: str = resp.url
        except (
            urllib.error.URLError,
            TimeoutError,
            OSError,
        ) as exc:
            msg = f"DOI resolution failed: {exc}"
            raise RuntimeError(msg) from exc

        return resolve_url_to_pdf(final_url)

    # --- Fallback: treat as direct PDF URL ----------------------------
    sys.stderr.write(f"[resolve] Direct URL \u2192 {identifier}\n")
    return _download_pdf(identifier)


# ---------------------------------------------------------------------------
# Prompt engineering
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT: str = (
    "You are a metadata extraction engine for cross-linking scientific "
    "papers with software artefacts.\n\n"
    "Given the text of a research paper, return a single JSON object with "
    'one key: "linkages" (array of objects).\n\n'
    "Each element in the linkages array MUST have:\n"
    '  "artefact_id": identifier (GitHub URL, pypi package name, '
    "or dataset name)\n"
    '  "artefact_type": one of "github_repository", "pypi_package", '
    '"dataset", "other"\n'
    '  "relation": one of the FOUR categories below\n'
    '  "comment": optional short explanation (or null)\n\n'
    "RELATION CATEGORIES (use exactly these values):\n"
    '1. "official_implementation" \u2014 the paper\'s OWN code, written by '
    "the authors. Look in Abstract, Footnotes, Code Availability.\n"
    '2. "unofficial_implementation" \u2014 third-party re-implementations '
    "mentioned in the text. Exclude integration standards "
    "(ONNX, DLPack).\n"
    '3. "used_in_experiments" \u2014 code or data used in experiments but '
    "the algorithm is NOT proposed in the paper. Includes: frameworks "
    "(PyTorch, TF), libraries (scikit-learn), baselines (LIBSVM), "
    "and DATASETS (MNIST, SQuAD, WMT).\n"
    '4. "cited_not_used" \u2014 code cited or discussed but NOT used in '
    "experiments.\n\n"
    "DATASETS: Include datasets as linkages with "
    'artefact_type="dataset" and relation="used_in_experiments". '
    "Include pre-training corpora, evaluation benchmarks, and "
    "download links (Zenodo, Figshare).\n\n"
    "MANDATORY RULES:\n"
    "- If the paper introduces a pip-installable tool, it MUST appear "
    'with relation "official_implementation".\n'
    "- Only extract what is in the text. Do NOT use outside knowledge.\n"
    "- Return valid JSON only \u2014 no markdown, no commentary.\n"
    "- Empty arrays must be [].\n\n"
    "EXAMPLE:\n"
    "Text: 'We introduce DGL (https://github.com/dmlc/dgl), built on "
    "PyTorch. We evaluate on Cora and Reddit. We compare against "
    "PyTorch-Geometric.'\n"
    "Output:\n"
    '{"linkages": ['
    '{"artefact_id": "https://github.com/dmlc/dgl", '
    '"artefact_type": "github_repository", '
    '"relation": "official_implementation", '
    '"comment": "Authors\' own code"}, '
    '{"artefact_id": "dgl", '
    '"artefact_type": "pypi_package", '
    '"relation": "official_implementation", '
    '"comment": "Paper\'s own package"}, '
    '{"artefact_id": "PyTorch", '
    '"artefact_type": "pypi_package", '
    '"relation": "used_in_experiments", '
    '"comment": "Core framework"}, '
    '{"artefact_id": "Cora", '
    '"artefact_type": "dataset", '
    '"relation": "used_in_experiments", '
    '"comment": "Evaluation dataset"}, '
    '{"artefact_id": "Reddit", '
    '"artefact_type": "dataset", '
    '"relation": "used_in_experiments", '
    '"comment": "Evaluation dataset"}, '
    '{"artefact_id": "PyTorch-Geometric", '
    '"artefact_type": "pypi_package", '
    '"relation": "cited_not_used", '
    '"comment": "Comparison baseline"}]}'
)


def build_extraction_prompt(text: str) -> str:
    """Build the user-side prompt that wraps the document text.

    Parameters
    ----------
    text : str
        Plain text extracted from the paper.

    Returns
    -------
    str
        Formatted prompt for the LLM.
    """
    return (
        "Extract structured metadata from the following "
        "scientific text.\n\n"
        f"--- BEGIN TEXT ---\n{text}\n--- END TEXT ---"
    )


# ---------------------------------------------------------------------------
# LLM extraction (Stage 2)
# ---------------------------------------------------------------------------


async def extract_links_from_text(
    text: str,
    *,
    model: str = _DEFAULT_MODEL,
) -> ExtractionResult:
    """Send text to an LLM and parse the structured extraction result.

    Uses structured output when available, falls back to JSON mode.
    Includes exponential backoff with jitter on retries.

    Parameters
    ----------
    text : str
        Plain text of a scientific paper (or abstract).
    model : str
        LiteLLM model identifier.

    Returns
    -------
    ExtractionResult
        Parsed and deduplicated extraction result.

    Raises
    ------
    ValueError
        If the LLM returns invalid JSON after all retries.
    ValidationError
        If the response fails Pydantic validation after all retries.
    """
    # Enforce token budget.
    text = text[:_MAX_CHARS]

    messages: list[dict[str, str]] = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {
            "role": "user",
            "content": build_extraction_prompt(text),
        },
    ]

    last_exc: Exception | None = None

    for attempt in range(_MAX_RETRIES):
        # Exponential backoff with jitter (skip first attempt).
        if attempt > 0:
            delay = min(
                2**attempt + random.uniform(0, 1),
                30,  # noqa: S311
            )
            await asyncio.sleep(delay)

        try:
            response: Any = await _call_llm(messages, model=model)
        except litellm.exceptions.APIError as exc:
            sys.stderr.write(f"LiteLLM API error (attempt {attempt + 1}): {exc}\n")
            last_exc = exc
            continue

        raw: str = response.choices[0].message.content

        try:
            payload: dict[str, Any] = json.loads(raw)
        except json.JSONDecodeError as exc:
            sys.stderr.write(f"Invalid JSON (attempt {attempt + 1}): {raw[:300]}\n")
            last_exc = ValueError("LLM response was not valid JSON")
            last_exc.__cause__ = exc
            continue

        try:
            result = ExtractionResult.model_validate(payload)
        except ValidationError as exc:
            sys.stderr.write(
                f"Schema validation failed (attempt {attempt + 1}): {exc}\n"
            )
            last_exc = exc
            continue

        return result.deduplicated()

    assert last_exc is not None  # noqa: S101
    raise last_exc


async def _call_llm(
    messages: list[dict[str, str]],
    *,
    model: str,
) -> Any:
    """Call the LLM with structured output fallback.

    Tries ``response_format=ExtractionResult`` first.  If the provider
    does not support structured output, falls back to
    ``{"type": "json_object"}``.

    Parameters
    ----------
    messages : list[dict[str, str]]
        Chat messages to send.
    model : str
        LiteLLM model identifier.

    Returns
    -------
    Any
        LiteLLM completion response.
    """
    try:
        return await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=0.0,
            timeout=90,
            response_format=ExtractionResult,
        )
    except (
        litellm.exceptions.APIError,
        NotImplementedError,
        Exception,
    ) as exc:
        # If structured output unsupported, fall back.
        err_msg = str(exc).lower()
        if any(
            kw in err_msg
            for kw in (
                "response_format",
                "structured",
                "unsupported",
                "not supported",
            )
        ):
            sys.stderr.write(
                "[fallback] Structured output not supported, using json_object mode\n"
            )
            return await litellm.acompletion(
                model=model,
                messages=messages,
                temperature=0.0,
                timeout=90,
                response_format={"type": "json_object"},
            )
        raise


# ---------------------------------------------------------------------------
# Public API — high-level extraction functions
# ---------------------------------------------------------------------------


def _merge_deterministic(
    result: ExtractionResult,
    det: list[CodeLinkage],
) -> ExtractionResult:
    """Merge deterministic regex results into the LLM result.

    Deterministic results are added only if the LLM didn't already
    find the same artefact.

    Parameters
    ----------
    result : ExtractionResult
        LLM extraction result.
    det : list[CodeLinkage]
        Deterministic regex results.

    Returns
    -------
    ExtractionResult
        Merged and deduplicated result.
    """
    llm_ids = {lnk.artefact_id.lower() for lnk in result.linkages}
    extra = [d for d in det if d.artefact_id.lower() not in llm_ids]
    return ExtractionResult(
        linkages=result.linkages + extra,
    ).deduplicated()


async def extract_from_text(
    text: str, *, model: str = _DEFAULT_MODEL
) -> ExtractionResult:
    """Extract linkages from raw text.

    Parameters
    ----------
    text : str
        Plain text content of a scientific paper.
    model : str
        LiteLLM model identifier.

    Returns
    -------
    ExtractionResult
        Structured extraction result.
    """
    det = extract_urls_deterministic(text)
    result = await extract_links_from_text(text, model=model)
    return _merge_deterministic(result, det)


async def extract_from_pdf(
    path: str, *, model: str = _DEFAULT_MODEL
) -> ExtractionResult:
    """Extract linkages from a local PDF file.

    Parameters
    ----------
    path : str
        Path to a local PDF file.
    model : str
        LiteLLM model identifier.

    Returns
    -------
    ExtractionResult
        Structured extraction result.

    Raises
    ------
    RuntimeError
        If the PDF cannot be read or exceeds limits.
    """
    text = extract_text_from_pdf(path)
    return await extract_from_text(text, model=model)


async def extract_from_url(
    url: str, *, model: str = _DEFAULT_MODEL
) -> ExtractionResult:
    """Extract linkages from a Zenodo or arxiv URL.

    Downloads the PDF to a temp file, extracts text, cleans up.

    Parameters
    ----------
    url : str
        Zenodo record URL or arxiv URL.
    model : str
        LiteLLM model identifier.

    Returns
    -------
    ExtractionResult
        Structured extraction result.
    """
    tmp_path = resolve_url_to_pdf(url)
    try:
        return await extract_from_pdf(tmp_path, model=model)
    finally:
        _safe_unlink(tmp_path)


async def extract_from_doi(
    doi: str, *, model: str = _DEFAULT_MODEL
) -> ExtractionResult:
    """Extract linkages from a DOI.

    Resolves the DOI to a PDF, downloads, extracts, cleans up.

    Parameters
    ----------
    doi : str
        DOI string (e.g. ``10.48550/arXiv.1810.04805``).
    model : str
        LiteLLM model identifier.

    Returns
    -------
    ExtractionResult
        Structured extraction result.
    """
    tmp_path = resolve_url_to_pdf(doi, is_doi=True)
    try:
        return await extract_from_pdf(tmp_path, model=model)
    finally:
        _safe_unlink(tmp_path)


def _safe_unlink(path: str) -> None:
    """Delete a file, ignoring errors."""
    try:
        os.unlink(path)
    except OSError:
        pass
