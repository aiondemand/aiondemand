from pydantic import BaseModel, Field


class Estimator(BaseModel):
    """Represents a specific ML model or estimator."""

    name: str = Field(
        description="""The class name of the model/estimator,
        e.g., 'RandomForestClassifier'"""
    )
    parameters: dict[str, str] | None = Field(
        default_factory=dict,
        description="""Hyperparameters mentioned in the text,
        e.g., {'n_estimators': '100'}""",
    )
    instantiable_string: str = Field(
        description="""The exact python string representation for the catalogue,
        e.g., 'RandomForestClassifier(n_estimators=100)'"""
    )


class Artefacts(BaseModel):
    """Granular ML components extracted for the AIoD catalogue."""

    estimators: list[Estimator] = Field(default_factory=list)
    datasets: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)


class PaperExtraction(BaseModel):
    """The master schema for the LLM output during the Population Phase."""

    related_code_used: list[str] = Field(default_factory=list)
    artefacts: Artefacts = Field(
        description="Granular ML components like estimators, datasets, and metrics."
    )
