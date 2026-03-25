from aiod.automation import get_paper
from aiod.automation.pydantic import Artefacts, Estimator, PaperExtraction


def test_get_paper(monkeypatch):
    def fake_extract_paper_data(*args, **kwargs):
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

    monkeypatch.setattr(
        "aiod.automation.llm.extract_paper_data", fake_extract_paper_data
    )
    # Mock the ArxivLoader
    from unittest.mock import MagicMock

    mock_loader = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "dummy text"
    mock_loader.load.return_value = [mock_doc]
    monkeypatch.setattr("aiod.automation.llm.ArxivLoader", lambda: mock_loader)

    paper = get_paper("doi:10.48550/arXiv.1234.56789")
    assert paper.fetch("metrics") == ["Accuracy"]
    assert paper.paper_id == "doi:10.48550/arXiv.1234.56789"
