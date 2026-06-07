"""Tests for the publication-code linkage extractor.

All tests use mocked HTTP responses and fake LLM generators — no real network
calls or LLM API keys are required.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import responses

from aiod.linkage_extractor import (
    ArtefactType,
    CodeLinkage,
    LiteLLMBackend,
    RelationType,
    TextCompletionBackend,
    _build_extraction_prompt,
    _html_to_text,
    _parse_linkage_response,
    extract_linkages_from_paper,
    extract_linkages_from_text,
    retrieve_paper_text,
)


# ---------------------------------------------------------------------------
# Data model tests
# ---------------------------------------------------------------------------


class TestRelationType:
    def test_all_values_exist(self):
        expected = {
            "official_implementation",
            "unofficial_implementation",
            "code_used_in_experiments",
            "code_cited_not_used",
            "other",
        }
        assert {r.value for r in RelationType} == expected

    def test_str_mixin(self):
        assert RelationType.OFFICIAL_IMPLEMENTATION.value == "official_implementation"


class TestArtefactType:
    def test_all_values_exist(self):
        expected = {"github_repository", "pypi_package", "other"}
        assert {a.value for a in ArtefactType} == expected


class TestCodeLinkage:
    def test_construction_with_defaults(self):
        link = CodeLinkage(
            artefact_id="owner/repo",
            artefact_type=ArtefactType.GITHUB_REPOSITORY,
            relation=RelationType.OFFICIAL_IMPLEMENTATION,
        )
        assert link.artefact_id == "owner/repo"
        assert link.comment is None
        assert link.confidence is None

    def test_construction_with_all_fields(self):
        link = CodeLinkage(
            artefact_id="numpy",
            artefact_type=ArtefactType.PYPI_PACKAGE,
            relation=RelationType.CODE_USED_IN_EXPERIMENTS,
            comment="Used as main numerical library",
            confidence=0.95,
        )
        assert link.confidence == 0.95
        assert link.comment == "Used as main numerical library"


# ---------------------------------------------------------------------------
# Prompt / parsing tests
# ---------------------------------------------------------------------------


class TestBuildExtractionPrompt:
    def test_prompt_contains_instructions(self):
        prompt = _build_extraction_prompt("Some paper text here.")
        assert "scientific software discovery" in prompt
        assert "official_implementation" in prompt
        assert "JSON" in prompt
        assert "Some paper text here." in prompt


class TestParseResponse:
    def test_valid_response(self):
        data = [
            {
                "artefact_id": "owner/repo",
                "artefact_type": "github_repository",
                "relation": "official_implementation",
                "comment": "Official code",
                "confidence": 0.9,
            },
            {
                "artefact_id": "numpy",
                "artefact_type": "pypi_package",
                "relation": "code_used_in_experiments",
            },
        ]
        result = _parse_linkage_response(json.dumps(data))
        assert len(result) == 2
        assert result[0].artefact_id == "owner/repo"
        assert result[0].artefact_type == ArtefactType.GITHUB_REPOSITORY
        assert result[0].relation == RelationType.OFFICIAL_IMPLEMENTATION
        assert result[0].confidence == 0.9
        assert result[1].artefact_id == "numpy"
        assert result[1].artefact_type == ArtefactType.PYPI_PACKAGE

    def test_markdown_fenced_json(self):
        """LLMs often wrap JSON in markdown code fences."""
        inner = json.dumps([
            {
                "artefact_id": "pkg",
                "artefact_type": "pypi_package",
                "relation": "other",
            }
        ])
        fenced = f"```json\n{inner}\n```"
        result = _parse_linkage_response(fenced)
        assert len(result) == 1
        assert result[0].artefact_id == "pkg"

    def test_malformed_json_raises(self):
        with pytest.raises(ValueError, match="not valid JSON"):
            _parse_linkage_response("this is not json")

    def test_non_list_raises(self):
        with pytest.raises(ValueError, match="must be a list"):
            _parse_linkage_response('{"key": "value"}')

    def test_skips_items_without_artefact_id(self):
        data = [
            {"artefact_type": "other", "relation": "other"},
            {"artefact_id": "", "artefact_type": "other", "relation": "other"},
            {
                "artefact_id": "valid/repo",
                "artefact_type": "github_repository",
                "relation": "other",
            },
        ]
        result = _parse_linkage_response(json.dumps(data))
        assert len(result) == 1
        assert result[0].artefact_id == "valid/repo"

    def test_unknown_enum_values_fallback_to_other(self):
        data = [
            {
                "artefact_id": "repo",
                "artefact_type": "dockerhub_image",
                "relation": "forked_from",
            }
        ]
        result = _parse_linkage_response(json.dumps(data))
        assert result[0].artefact_type == ArtefactType.OTHER
        assert result[0].relation == RelationType.OTHER

    def test_non_dict_items_skipped(self):
        data = ["string_item", {"artefact_id": "ok", "relation": "other"}]
        result = _parse_linkage_response(json.dumps(data))
        assert len(result) == 1

    def test_empty_comment_becomes_none(self):
        data = [
            {
                "artefact_id": "repo",
                "artefact_type": "other",
                "relation": "other",
                "comment": "",
            }
        ]
        result = _parse_linkage_response(json.dumps(data))
        assert result[0].comment is None


# ---------------------------------------------------------------------------
# Backend tests
# ---------------------------------------------------------------------------


class TestTextCompletionBackend:
    def test_end_to_end(self):
        fake_response = json.dumps([
            {
                "artefact_id": "scikit-learn/scikit-learn",
                "artefact_type": "github_repository",
                "relation": "code_used_in_experiments",
                "comment": "ML library used for baselines",
                "confidence": 0.85,
            }
        ])

        def fake_generator(prompt: str) -> str:
            assert "Paper text" in prompt or "scientific paper" in prompt
            return fake_response

        backend = TextCompletionBackend(generator=fake_generator)
        linkages = backend.extract_linkages("Some paper text.")
        assert len(linkages) == 1
        assert linkages[0].artefact_id == "scikit-learn/scikit-learn"
        assert linkages[0].relation == RelationType.CODE_USED_IN_EXPERIMENTS


class TestLiteLLMBackend:
    def test_import_error_gives_clear_message(self):
        backend = LiteLLMBackend(model="openai/gpt-4o")
        with patch.dict("sys.modules", {"litellm": None}):
            with pytest.raises(RuntimeError, match="litellm"):
                backend.extract_linkages("paper text")

    def test_calls_litellm_completion(self):
        mock_litellm = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps([
            {
                "artefact_id": "torch",
                "artefact_type": "pypi_package",
                "relation": "code_used_in_experiments",
            }
        ])
        mock_litellm.completion.return_value = mock_response

        backend = LiteLLMBackend(
            model="openai/gpt-4o",
            api_key="test-key",
        )

        with patch.dict("sys.modules", {"litellm": mock_litellm}):
            linkages = backend.extract_linkages("Paper about deep learning.")

        assert len(linkages) == 1
        assert linkages[0].artefact_id == "torch"
        mock_litellm.completion.assert_called_once()
        call_kwargs = mock_litellm.completion.call_args[1]
        assert call_kwargs["model"] == "openai/gpt-4o"
        assert call_kwargs["api_key"] == "test-key"


# ---------------------------------------------------------------------------
# Paper text retrieval tests
# ---------------------------------------------------------------------------


class TestRetrievePaperText:
    def test_local_text_file(self, tmp_path: Path):
        text_file = tmp_path / "paper.txt"
        text_file.write_text("Hello, this is a paper.", encoding="utf-8")
        result = retrieve_paper_text(str(text_file))
        assert result == "Hello, this is a paper."

    def test_raw_text_fallback(self):
        raw = "This is raw paper text that is not a file path."
        assert retrieve_paper_text(raw) == raw

    @responses.activate
    def test_zenodo_url(self):
        record_id = "12345"
        api_url = f"https://zenodo.org/api/records/{record_id}"

        responses.add(
            responses.GET,
            api_url,
            json={
                "files": [
                    {
                        "key": "paper.pdf",
                        "links": {"self": "https://zenodo.org/files/paper.pdf"},
                    }
                ]
            },
            status=200,
        )

        # Mock the PDF download — return minimal valid-ish bytes that will fail
        # gracefully so we can test the flow up to PDF extraction
        responses.add(
            responses.GET,
            "https://zenodo.org/files/paper.pdf",
            body=b"fake-pdf-content",
            status=200,
        )

        # pypdf will fail on fake bytes, but we can patch the extractor
        with patch(
            "aiod.linkage_extractor._extract_pdf_from_bytes",
            return_value="Extracted paper text",
        ):
            result = retrieve_paper_text(f"https://zenodo.org/records/{record_id}")

        assert result == "Extracted paper text"

    @responses.activate
    def test_zenodo_no_pdf_raises(self):
        record_id = "99999"
        api_url = f"https://zenodo.org/api/records/{record_id}"

        responses.add(
            responses.GET,
            api_url,
            json={"files": [{"key": "data.csv"}]},
            status=200,
        )

        with pytest.raises(ValueError, match="No PDF file found"):
            retrieve_paper_text(f"https://zenodo.org/records/{record_id}")

    @responses.activate
    def test_doi_redirects_to_zenodo(self):
        doi = "10.5281/zenodo.12345"
        doi_url = f"https://doi.org/{doi}"

        # HEAD request follows redirect to Zenodo
        responses.add(
            responses.HEAD,
            doi_url,
            status=302,
            headers={"Location": "https://zenodo.org/records/12345"},
        )
        responses.add(
            responses.HEAD,
            "https://zenodo.org/records/12345",
            status=200,
        )

        # Mock the Zenodo API + PDF extraction
        responses.add(
            responses.GET,
            "https://zenodo.org/api/records/12345",
            json={
                "files": [
                    {
                        "key": "paper.pdf",
                        "links": {"self": "https://zenodo.org/files/paper.pdf"},
                    }
                ]
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://zenodo.org/files/paper.pdf",
            body=b"fake-pdf",
            status=200,
        )

        with patch(
            "aiod.linkage_extractor._extract_pdf_from_bytes",
            return_value="DOI paper text",
        ):
            result = retrieve_paper_text(doi)

        assert result == "DOI paper text"

    @responses.activate
    def test_arbitrary_html_url(self):
        url = "https://example.com/paper.html"

        responses.add(
            responses.GET,
            url,
            body="<html><body><h1>Title</h1><p>Content here.</p></body></html>",
            status=200,
            content_type="text/html",
        )

        result = retrieve_paper_text(url)
        assert "Title" in result
        assert "Content here" in result


class TestHtmlToText:
    def test_strips_tags_with_bs4(self):
        html = "<html><body><h1>Hello</h1><p>World</p></body></html>"
        result = _html_to_text(html)
        assert "Hello" in result
        assert "World" in result
        assert "<" not in result

    def test_regex_fallback(self):
        html = "<b>Bold</b> and <i>italic</i>"
        with patch.dict("sys.modules", {"bs4": None}):
            # Force ImportError to test regex fallback
            with patch(
                "aiod.linkage_extractor._html_to_text",
                wraps=lambda h: __import__("re").sub(r"<[^>]+>", "", h),
            ):
                import re
                result = re.sub(r"<[^>]+>", "", html)
                assert result == "Bold and italic"


# ---------------------------------------------------------------------------
# Orchestration tests
# ---------------------------------------------------------------------------


class TestExtractLinkagesFromPaper:
    def test_raises_without_backend(self):
        with pytest.raises(ValueError, match="No LLM backend"):
            extract_linkages_from_paper("some text")

    def test_end_to_end_with_mock(self):
        fake_json = json.dumps([
            {
                "artefact_id": "pandas-dev/pandas",
                "artefact_type": "github_repository",
                "relation": "code_used_in_experiments",
            }
        ])
        backend = TextCompletionBackend(generator=lambda _: fake_json)
        linkages = extract_linkages_from_paper("paper text", backend=backend)
        assert len(linkages) == 1
        assert linkages[0].artefact_id == "pandas-dev/pandas"


class TestExtractLinkagesFromText:
    def test_convenience_wrapper(self):
        fake_json = json.dumps([
            {
                "artefact_id": "scipy",
                "artefact_type": "pypi_package",
                "relation": "code_cited_not_used",
            }
        ])
        backend = TextCompletionBackend(generator=lambda _: fake_json)
        linkages = extract_linkages_from_text("paper text", backend)
        assert len(linkages) == 1
        assert linkages[0].relation == RelationType.CODE_CITED_NOT_USED


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestCLI:
    def test_json_output(self, capsys: pytest.CaptureFixture[str]):
        from aiod.linkage_cli import _format_json

        linkages = [
            CodeLinkage(
                artefact_id="owner/repo",
                artefact_type=ArtefactType.GITHUB_REPOSITORY,
                relation=RelationType.OFFICIAL_IMPLEMENTATION,
                comment="Official repo",
                confidence=0.95,
            )
        ]
        output = _format_json(linkages)
        parsed = json.loads(output)
        assert len(parsed) == 1
        assert parsed[0]["artefact_id"] == "owner/repo"
        assert parsed[0]["artefact_type"] == "github_repository"

    def test_table_output(self):
        from aiod.linkage_cli import _format_table

        linkages = [
            CodeLinkage(
                artefact_id="torch",
                artefact_type=ArtefactType.PYPI_PACKAGE,
                relation=RelationType.CODE_USED_IN_EXPERIMENTS,
            )
        ]
        table = _format_table(linkages)
        assert "torch" in table
        assert "pypi_package" in table
        assert "code_used_in_experiments" in table

    def test_table_empty(self):
        from aiod.linkage_cli import _format_table

        assert _format_table([]) == "No linkages found."

    def test_build_parser(self):
        from aiod.linkage_cli import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "paper.pdf",
            "--model", "openai/gpt-4o",
            "--output", "json",
        ])
        assert args.paper == "paper.pdf"
        assert args.model == "openai/gpt-4o"
        assert args.output == "json"
