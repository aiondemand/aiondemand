from aiod.automation import papers
from aiod.automation.pydantic import Artefacts, Estimator, PaperExtraction


def test_paper_population_and_fetch(monkeypatch, tmp_path):
    cache_path = tmp_path / "paper_cache.json"
    monkeypatch.setattr(papers, "PAPER_CACHE_FILE", cache_path)

    def fake_extract_paper_metadata(*args, **kwargs):
        return PaperExtraction(
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
        )

    monkeypatch.setattr(papers, "extract_paper_metadata", fake_extract_paper_metadata)
    monkeypatch.setattr(papers, "extract_text_from_pdf", lambda pdf_path: "dummy text")

    paper = papers.populate_paper("doi:10.1000/xyz123", source="dummy.pdf", force=True)
    assert paper.fetch("metrics") == ["Accuracy"]

    loaded = papers.get_paper("doi:10.1000/xyz123")
    assert loaded.fetch("metrics") == ["Accuracy"]


def test_aiod_get_dispatches_to_paper(monkeypatch, tmp_path):
    from aiod import get

    # create minimal cached paper
    cache_path = tmp_path / "paper_cache.json"
    monkeypatch.setattr(papers, "PAPER_CACHE_FILE", cache_path)

    monkeypatch.setattr(
        papers,
        "populate_paper",
        lambda paper_id, source, model_name="gpt-4o-mini", force=False: papers.Paper(
            paper_id,
            PaperExtraction(
                related_code_used=[],
                artefacts=Artefacts(estimators=[], datasets=[], metrics=[]),
            ),
        ),
    )

    paper = get("doi:10.1000/xyz321")
    assert paper.paper_id == "doi:10.1000/xyz321"
