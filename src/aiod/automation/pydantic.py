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

    estimators: list[Estimator] = Field(
        default_factory=list,
        description="""List of all machine learning models, algorithms,
        and preprocessing modules mentioned.""",
    )
    datasets: list[str] = Field(
        default_factory=list,
        description="""Specific names of benchmark datasets used for training
        or evaluation, e.g., 'MNIST', '20-Newsgroups', 'CIFAR-10'.""",
    )
    metrics: list[str] = Field(
        default_factory=list,
        description="""Evaluation metrics used to score the models, e.g., 'Accuracy',
        'F1-Score', 'Zero-One Loss'.""",
    )


class PaperExtraction(BaseModel):
    """The master schema for the LLM output during the Population Phase."""

    related_code_used: list[str] = Field(default_factory=list)
    artefacts: Artefacts = Field(
        description="Granular ML components like estimators, datasets, and metrics."
    )
