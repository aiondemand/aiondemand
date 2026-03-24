from aiod.automation import papers
from aiod.automation.pydantic import Artefacts, Estimator, PaperExtraction


def test_paper_population_and_fetch(monkeypatch, tmp_path):
    cache_path = tmp_path / "paper_cache.json"
    monkeypatch.setattr(papers, "PAPER_CACHE_FILE", cache_path)

    def fake_extract_paper_metadata(*args, **kwargs):
        return PaperExtraction(
            official_github=["https://github.com/example/repo"],
            unofficial_github=[],
            pypi_packages=["example-pkg"],
            related_code_used=["scikit-learn"],
            artefacts=Artefacts(
                estimators=[
                    Estimator(
                        name="RandomForestClassifier",
                        parameters={"n_estimators": "100"},
                        instantiable_string="RandomForestClassifier(n_estimators=100)",
                    )
                ],
                datasets=["Adult"],
                metrics=["Accuracy"],
            ),
            confidence_score=0.95,
        )

    monkeypatch.setattr(papers, "extract_paper_metadata", fake_extract_paper_metadata)

    # cached retrieval should return same object
    loaded = papers.get_paper("doi:10.1000/xyz123")
    assert loaded.fetch("metrics") == ["Accuracy"]


def test_aiod_get_dispatches_to_paper(monkeypatch, tmp_path):
    from aiod import get

    # create minimal cached paper
    cache_path = tmp_path / "paper_cache.json"
    monkeypatch.setattr(papers, "PAPER_CACHE_FILE", cache_path)

    def fake_extract_paper_metadata(*args, **kwargs):
        return PaperExtraction(
            official_github=[],
            unofficial_github=[],
            pypi_packages=[],
            related_code_used=[],
            artefacts=Artefacts(estimators=[], datasets=[], metrics=[]),
            confidence_score=0.5,
        )

    monkeypatch.setattr(papers, "extract_paper_metadata", fake_extract_paper_metadata)

    paper = get("doi:10.1000/xyz321")
    assert paper.paper_id == "doi:10.1000/xyz321"
