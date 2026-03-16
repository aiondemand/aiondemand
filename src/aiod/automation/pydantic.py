import re
from typing import Dict, List, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Estimator(BaseModel):
    """Represents a specific ML model or estimator."""

    name: str = Field(
        description="The class name of the model/estimator, e.g., 'RandomForestClassifier'"
    )
    parameters: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Hyperparameters mentioned in the text, e.g., {'n_estimators': '100'}",
    )
    instantiable_string: str = Field(
        description="The exact python string representation for the catalogue, e.g., 'RandomForestClassifier(n_estimators=100)'"
    )


class Artefacts(BaseModel):
    """Granular ML components extracted for the AIoD catalogue."""

    estimators: List[Estimator] = Field(
        default_factory=list,
        description="Machine learning models and estimators used or proposed in the paper.",
    )
    datasets: List[str] = Field(
        default_factory=list,
        description="Specific names of datasets used for training, testing, or benchmarking.",
    )
    metrics: List[str] = Field(
        default_factory=list,
        description="Evaluation metrics used for comparison, e.g., 'Accuracy', 'F1-Score', 'RMSE'.",
    )


class PaperExtraction(BaseModel):
    """The master schema for the LLM output during the Population Phase."""

    official_github: List[str] = Field(
        default_factory=list, description="URLs to the official code repositories."
    )
    unofficial_github: List[str] = Field(
        default_factory=list,
        description="URLs to unofficial reproductions or related repositories.",
    )
    pypi_packages: List[str] = Field(
        default_factory=list,
        description="Specific PyPI package names created or required by the paper.",
    )
    related_code_used: List[str] = Field(
        default_factory=list,
        description="Libraries or tools used for experiments but not proposed in the paper.",
    )
    artefacts: Artefacts = Field(
        description="Granular ML components like estimators, datasets, and metrics."
    )


SYSTEM_PROMPT = """You are an expert machine learning metadata extraction engine designed to cross-link scientific papers with software artifacts for the AI-on-Demand (AIoD) catalogue.

Your task is to analyze excerpts from research papers and extract a structured JSON object detailing the code repositories, packages, and specific machine learning artifacts mentioned.

### CORE DEFINITIONS
1. Official Implementation: The paper's own code or package.
2. Unofficial Implementation: Third-party community reproductions.
3. Used in Experiments: Frameworks, libraries, and datasets used to conduct the research, but not proposed as the novel contribution.
4. Cited Not Used: Tools discussed but not executed.

### GRANULAR ARTIFACT EXTRACTION
- Estimators: Extract specific model class names. If hyperparameters are mentioned, capture them. Format as a valid Python string (e.g., "XGBClassifier(max_depth=3)").
- Datasets: Extract names of specific benchmark datasets.
- Metrics: Extract evaluation metrics used.

### MANDATORY RULES
- Output strictly valid JSON matching the schema.
- Do not guess parameters or artifacts not explicitly mentioned in the text.
"""

# ---------------------------------------------------------------------------
# 3. Deterministic Extraction (Regex Pre-pass)
# ---------------------------------------------------------------------------


def extract_urls_deterministic(text: str) -> Dict[str, List[str]]:
    """Quick regex pass to find URLs before hitting the LLM."""
    github_re = re.compile(
        r"https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]*[\w]", re.IGNORECASE
    )
    pypi_re = re.compile(r"https?://pypi\.org/project/([\w.-]+)", re.IGNORECASE)

    return {
        "candidate_githubs": list(set(github_re.findall(text))),
        "candidate_pypis": list(set(pypi_re.findall(text))),
    }


# ---------------------------------------------------------------------------
# 4. LLM Orchestration
# ---------------------------------------------------------------------------


def extract_paper_metadata(
    text: str, model_name: str = "gpt-4o-mini"
) -> PaperExtraction:
    """Run the full extraction pipeline for the Population Phase."""
    # Step 1: Get deterministic hints (optional, but helps guide the LLM if you inject it into the prompt)
    hints = extract_urls_deterministic(text)
    user_content = (
        f"Text to analyze:\n\n{text}\n\n(Hint: found these candidate URLs: {hints})"
    )

    # Step 2: Call the LLM with structured output enforcement via LangChain
    prompt_text = (
        f"""{SYSTEM_PROMPT}\n\nPlease answer as strictly valid JSON matching the schema.
        \n{user_content}"""
    )

    llm = ChatOpenAI(model_name=model_name, temperature=0.0)
    llm = llm.with_structured_output(PaperExtraction)
    result = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt_text)]
    )
    
    return result
