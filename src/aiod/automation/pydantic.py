import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Estimator(BaseModel):
    """Represents a specific ML model or estimator."""

    name: str = Field(
        description="The class name of the model/estimator, e.g., 'RandomForestClassifier'"
    )
    parameters: dict[str, str] | None = Field(
        default_factory=dict,
        description="Hyperparameters mentioned in the text, e.g., {'n_estimators': '100'}",
    )
    instantiable_string: str = Field(
        description="The exact python string representation for the catalogue, e.g., 'RandomForestClassifier(n_estimators=100)'"
    )


class Artefacts(BaseModel):
    """Granular ML components extracted for the AIoD catalogue."""

    estimators: list[Estimator] = Field(
        default_factory=list,
        description="Machine learning models and estimators used or proposed in the paper.",
    )
    datasets: list[str] = Field(
        default_factory=list,
        description="Specific names of datasets used for training, testing, or benchmarking.",
    )
    metrics: list[str] = Field(
        default_factory=list,
        description="Evaluation metrics used for comparison, e.g., 'Accuracy', 'F1-Score', 'RMSE'.",
    )


class PaperExtraction(BaseModel):
    """The master schema for the LLM output during the Population Phase."""

    related_code_used: list[str] = Field(
        default_factory=list,
        description="Libraries or tools used for experiments but not proposed in the paper.",
    )
    artefacts: Artefacts = Field(
        description="Granular ML components like estimators, datasets, and metrics."
    )


SYSTEM_PROMPT = """You are a technical machine learning metadata extraction engine. Your goal is to identify all machine learning algorithms, their specific hyperparameters, datasets, and metrics from scientific publications.

### ARTEFACT DISCOVERY RULES
1. **Identify Estimators**: Scan for every mentioned algorithm, model, or preprocessing module (e.g., SVC, PCA, RandomForestClassifier).
2. **STRICT PASCALCASE NAMING**: You MUST convert all model names to PascalCase for the 'name' and 'instantiable_string' fields. 
    - INCORRECT: svc(), pca(), random_forest()
    - CORRECT: SVC(), PCA(), RandomForestClassifier()
3. **Capture Arguments**: Extract the actual numerical or categorical values mentioned (e.g., "n_estimators=100", "whiten=True"). If no values are found, use empty parentheses: "ClassName()".
4. **Exhaustive List**: Look past the first example. If the paper lists 12 different components in its configuration or search space, include all 12 in the 'estimators' list.

### DATA SOURCES
- Scan lists of terms like "SVM, KNN, PCA, Gradient Boosting".
- Look for words followed by parentheses: "ModelName(...)".
- Check tables comparing different "Methods" or "Baselines".

### MANDATORY OUTPUT FORMAT
Return ONLY a JSON object. Use double curly braces {{ }} to escape JSON characters.

{{
  "related_code_used": ["List actual library names found, e.g., 'Scikit-Learn', 'Hyperopt'"],
  "artefacts": {{
    "estimators": [
      {{
        "name": "PascalCaseClassName",
        "parameters": {{"param_name": "value"}},
        "instantiable_string": "PascalCaseClassName(param_name=value)"
      }}
    ],
    "datasets": ["Names of datasets used"],
    "metrics": ["Names of evaluation metrics used"]
  }}
}}

CRITICAL: In Python, Class Names are always PascalCase. You must return 'SVC' not 'svc', and 'RandomForestClassifier' not 'random_forest'. If you fail this, the code will crash.
"""

# ---------------------------------------------------------------------------
# 3. Deterministic Extraction (Regex Pre-pass)
# ---------------------------------------------------------------------------


def extract_urls_deterministic(text: str) -> dict[str, list[str]]:
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
    text: str,
    model_name: str = "qwen2.5-coder:3b",
    base_url: str = "http://192.168.0.169:1234/v1",
    api_key: str = "not-needed",
    temperature: float = 0.0,
    max_tokens: int | None = None,
) -> PaperExtraction:
    """Run the full extraction pipeline for the Population Phase."""
    hints = extract_urls_deterministic(text)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Text to analyze:\n\n{text}\n\n(Hint: found these candidate URLs: {hints})",
            ),
        ]
    )

    llm = ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    structured_llm = llm.with_structured_output(PaperExtraction)

    chain = prompt | structured_llm

    return chain.invoke({"text": text, "hints": hints})
