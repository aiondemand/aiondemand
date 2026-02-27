"""Unit tests for aiod.crosslinker and aiod.crosslink_cli."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import litellm
import pytest

from aiod.crosslinker import (
    _MAX_CHARS,
    ArtefactType,
    CodeLinkage,
    ExtractionResult,
    RelationType,
    _select_best_pdf,
    build_extraction_prompt,
    extract_urls_deterministic,
)

# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------


class TestEnums:
    def test_relation_types(self):
        assert RelationType.OFFICIAL_IMPLEMENTATION.value == "official_implementation"
        assert (
            RelationType.UNOFFICIAL_IMPLEMENTATION.value == "unofficial_implementation"
        )
        assert RelationType.USED_IN_EXPERIMENTS.value == "used_in_experiments"
        assert RelationType.CITED_NOT_USED.value == "cited_not_used"

    def test_artefact_types(self):
        assert ArtefactType.GITHUB_REPOSITORY.value == "github_repository"
        assert ArtefactType.PYPI_PACKAGE.value == "pypi_package"
        assert ArtefactType.DATASET.value == "dataset"
        assert ArtefactType.OTHER.value == "other"


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


class TestExtractionResult:
    def test_default_all_empty(self):
        result = ExtractionResult()
        assert result.linkages == []

    def test_from_dict(self):
        data = {
            "linkages": [
                {
                    "artefact_id": "https://github.com/a/b",
                    "artefact_type": "github_repository",
                    "relation": "official_implementation",
                    "comment": "Authors' code",
                },
                {
                    "artefact_id": "MNIST",
                    "artefact_type": "dataset",
                    "relation": "used_in_experiments",
                    "comment": None,
                },
            ],
        }
        result = ExtractionResult.model_validate(data)
        assert len(result.linkages) == 2
        assert result.linkages[0].artefact_id == "https://github.com/a/b"
        assert result.linkages[0].relation == "official_implementation"
        assert result.linkages[1].artefact_type == "dataset"

    def test_deduplication(self):
        code = [
            CodeLinkage(
                artefact_id="https://github.com/a/b",
                artefact_type="github_repository",
                relation="official_implementation",
            ),
            CodeLinkage(
                artefact_id="https://github.com/a/b",
                artefact_type="github_repository",
                relation="used_in_experiments",
            ),
        ]
        datasets = [
            CodeLinkage(
                artefact_id="MNIST",
                artefact_type="dataset",
                relation="used_in_experiments",
            ),
            CodeLinkage(
                artefact_id="MNIST",
                artefact_type="dataset",
                relation="used_in_experiments",
            ),
            CodeLinkage(
                artefact_id="CIFAR-10",
                artefact_type="dataset",
                relation="used_in_experiments",
            ),
        ]
        result = ExtractionResult(linkages=code + datasets)
        deduped = result.deduplicated()
        assert len(deduped.linkages) == 3  # 1 repo + 2 unique datasets

    def test_deduplication_case_insensitive(self):
        result = ExtractionResult(
            linkages=[
                CodeLinkage(
                    artefact_id="https://GitHub.com/A/B",
                    artefact_type="github_repository",
                    relation="official_implementation",
                ),
                CodeLinkage(
                    artefact_id="https://github.com/a/b",
                    artefact_type="github_repository",
                    relation="used_in_experiments",
                ),
            ],
        )
        deduped = result.deduplicated()
        assert len(deduped.linkages) == 1

    def test_partial_fields_use_defaults(self):
        data = {
            "linkages": [
                {
                    "artefact_id": "numpy",
                    "artefact_type": "pypi_package",
                    "relation": "used_in_experiments",
                },
            ],
        }
        result = ExtractionResult.model_validate(data)
        assert result.linkages[0].comment is None


class TestCodeLinkage:
    def test_all_four_relations(self):
        for rel in [
            "official_implementation",
            "unofficial_implementation",
            "used_in_experiments",
            "cited_not_used",
        ]:
            linkage = CodeLinkage(
                artefact_id="test",
                artefact_type="pypi_package",
                relation=rel,
            )
            assert linkage.relation == rel

    def test_with_comment(self):
        linkage = CodeLinkage(
            artefact_id="pytorch",
            artefact_type="pypi_package",
            relation="used_in_experiments",
            comment="Core framework",
        )
        assert linkage.comment == "Core framework"


# ---------------------------------------------------------------------------
# Deterministic URL extraction tests
# ---------------------------------------------------------------------------


class TestDeterministicExtraction:
    def test_github_urls(self):
        text = (
            "Our code is at https://github.com/author/project and "
            "we compare to https://github.com/other/tool."
        )
        result = extract_urls_deterministic(text)
        ids = [lnk.artefact_id for lnk in result]
        assert "https://github.com/author/project" in ids
        assert "https://github.com/other/tool" in ids
        assert all(lnk.artefact_type == "github_repository" for lnk in result)

    def test_pypi_urls(self):
        text = "Install from https://pypi.org/project/scikit-learn/."
        result = extract_urls_deterministic(text)
        ids = [lnk.artefact_id for lnk in result]
        assert "scikit-learn" in ids
        assert result[0].artefact_type == "pypi_package"

    def test_no_urls(self):
        text = "This paper has no software links."
        result = extract_urls_deterministic(text)
        assert result == []

    def test_deduplication(self):
        text = "See https://github.com/a/b and also https://github.com/a/b."
        result = extract_urls_deterministic(text)
        assert len(result) == 1

    def test_default_relation(self):
        text = "Code at https://github.com/org/repo."
        result = extract_urls_deterministic(text)
        assert result[0].relation == "used_in_experiments"


# ---------------------------------------------------------------------------
# Prompt tests
# ---------------------------------------------------------------------------


class TestPrompt:
    def test_prompt_wraps_text(self):
        prompt = build_extraction_prompt("Hello world")
        assert "--- BEGIN TEXT ---" in prompt
        assert "Hello world" in prompt
        assert "--- END TEXT ---" in prompt

    def test_prompt_is_string(self):
        prompt = build_extraction_prompt("Test")
        assert isinstance(prompt, str)


# ---------------------------------------------------------------------------
# Zenodo PDF selection tests
# ---------------------------------------------------------------------------


class TestSelectBestPdf:
    def test_prefers_paper_filename(self):
        files = [
            {
                "key": "supplementary.pdf",
                "size": 5000,
                "links": {"self": "url1"},
            },
            {
                "key": "paper.pdf",
                "size": 1000,
                "links": {"self": "url2"},
            },
        ]
        assert _select_best_pdf(files) == "url2"

    def test_prefers_article_filename(self):
        files = [
            {
                "key": "data.pdf",
                "size": 5000,
                "links": {"self": "url1"},
            },
            {
                "key": "article_final.pdf",
                "size": 1000,
                "links": {"self": "url2"},
            },
        ]
        assert _select_best_pdf(files) == "url2"

    def test_fallback_to_largest(self):
        files = [
            {
                "key": "small.pdf",
                "size": 100,
                "links": {"self": "url1"},
            },
            {
                "key": "large.pdf",
                "size": 9999,
                "links": {"self": "url2"},
            },
        ]
        assert _select_best_pdf(files) == "url2"

    def test_no_pdfs(self):
        files = [
            {
                "key": "data.csv",
                "size": 100,
                "links": {"self": "url1"},
            },
        ]
        assert _select_best_pdf(files) is None

    def test_empty_files(self):
        assert _select_best_pdf([]) is None


# ---------------------------------------------------------------------------
# PDF extraction tests (mocked)
# ---------------------------------------------------------------------------


class TestPdfExtraction:
    def test_rejects_too_large(self, tmp_path):
        big_file = tmp_path / "big.pdf"
        big_file.write_bytes(b"x" * (51 * 1024 * 1024))

        from aiod.crosslinker import extract_text_from_pdf

        with pytest.raises(RuntimeError, match="too large"):
            extract_text_from_pdf(str(big_file))

    def test_token_budget_enforced(self):
        assert _MAX_CHARS == 60_000


# ---------------------------------------------------------------------------
# URL resolver routing tests
# ---------------------------------------------------------------------------


class TestResolverRouting:
    def test_arxiv_pattern(self):
        import re

        pattern = re.compile(r"https?://arxiv\.org/(abs|pdf)/(\d{4}\.\d{4,5})(v\d+)?")
        assert pattern.match("https://arxiv.org/abs/1810.04805")
        assert pattern.match("https://arxiv.org/pdf/1810.04805v2")
        assert not pattern.match("https://example.com/paper")

    def test_zenodo_pattern(self):
        import re

        pattern = re.compile(r"https?://zenodo\.org/records?/(\d+)")
        m = pattern.match("https://zenodo.org/records/4106480")
        assert m
        assert m.group(1) == "4106480"

        m2 = pattern.match("https://zenodo.org/record/123456")
        assert m2
        assert m2.group(1) == "123456"


# ---------------------------------------------------------------------------
# LLM fallback tests (mocked)
# ---------------------------------------------------------------------------


class TestLlmFallback:
    @pytest.mark.asyncio
    async def test_structured_output_fallback(self):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps(
            {
                "linkages": [],
            }
        )

        with patch("aiod.crosslinker.litellm") as mock_litellm:
            mock_litellm.acompletion = AsyncMock(
                side_effect=[
                    litellm.exceptions.APIError(
                        message="response_format not supported",
                        model="test",
                        llm_provider="test",
                        status_code=400,
                    ),
                    mock_response,
                ]
            )
            mock_litellm.exceptions = litellm.exceptions

            from aiod.crosslinker import (
                _call_llm as call_fn,
            )

            result = await call_fn(
                [{"role": "user", "content": "test"}],
                model="test/model",
            )
            assert result.choices[0].message.content is not None
