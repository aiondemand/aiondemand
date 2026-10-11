"""Tests for explicitly selected, safe notebook examples."""

from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
nbclient = pytest.importorskip("nbclient")
NotebookClient = nbclient.NotebookClient

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = (
    REPO_ROOT / "docs" / "examples" / "ai-on-demand.ipynb"
)


def test_tagged_ai_on_demand_notebook_cells_execute():
    """Execute only notebook cells explicitly tagged for CI."""
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)

    tagged_cells = [
        cell
        for cell in notebook.cells
        if cell.cell_type == "code"
        and "ci" in cell.metadata.get("tags", [])
    ]

    assert tagged_cells, "No code cells are tagged for CI execution."

    # Keep markdown and explicitly selected code cells only.
    # Execute in memory; never save outputs to the source notebook.
    notebook.cells = [
        cell
        for cell in notebook.cells
        if cell.cell_type != "code"
        or "ci" in cell.metadata.get("tags", [])
    ]

    NotebookClient(
        notebook,
        timeout=120,
        kernel_name="python3",
        resources={"metadata": {"path": str(REPO_ROOT)}},
    ).execute()
