from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import re
import json

# --- LangChain Imports ---
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 

from aiod.automation import extract_text_from_pdf

# ---------------------------------------------------------------------------
# 1. AIoD Schema Definitions
# ---------------------------------------------------------------------------

class Estimator(BaseModel):
    """Represents a specific ML model or estimator."""
    name: str = Field(
        description="The class name of the model/estimator, e.g., 'RandomForestClassifier'"
    )
    parameters: Optional[Dict[str, str]] = Field(
        default_factory=dict, 
        description="Hyperparameters mentioned in the text, e.g., {'n_estimators': '100'}"
    )
    instantiable_string: str = Field(
        description="The exact python string representation for the catalogue, e.g., 'RandomForestClassifier(n_estimators=100)'"
    )

class Artefacts(BaseModel):
    """Granular ML components extracted for the AIoD catalogue."""
    estimators: List[Estimator] = Field(default_factory=list)
    datasets: List[str] = Field(default_factory=list)
    metrics: List[str] = Field(default_factory=list)

class PaperExtraction(BaseModel):
    """The master schema for the LLM output during the Population Phase."""
    related_code_used: List[str] = Field(default_factory=list)
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

def extract_urls_deterministic(text: str) -> Dict[str, List[str]]:
    github_re = re.compile(r"https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]*[\w]", re.IGNORECASE)
    pypi_re = re.compile(r"https?://pypi\.org/project/([\w.-]+)", re.IGNORECASE)
    return {
        "candidate_githubs": list(set(github_re.findall(text))),
        "candidate_pypis": list(set(pypi_re.findall(text)))
    }


def extract_paper_metadata(text: str) -> PaperExtraction:
    """Runs the extraction using Qwen 2.5 Coder on the remote GPU laptop."""
    
    hints = extract_urls_deterministic(text)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Text to analyze:\n\n{text}\n\n(Hint: found these candidate URLs: {hints})")
    ])

    llm = ChatOpenAI(
        base_url=f"http://192.168.0.169:1234/v1",
        api_key="not-needed", 
        model="qwen2.5-coder:3b",
        max_tokens=None,
        temperature=0.0
    )

    structured_llm = llm.with_structured_output(PaperExtraction)

    chain = prompt | structured_llm
    
    return chain.invoke({"text": text, "hints": hints})

# ---------------------------------------------------------------------------
# 4. Main Loop
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Set your GPU laptop's IP here
    
    # 2. Extract text using your 'w.py' module
    raw_text = extract_text_from_pdf(r"C:\Users\satvm\Downloads\p.pdf")
        
    # 3. Run the extraction
    result = extract_paper_metadata(raw_text)
        
    print(result.model_dump_json(indent=2))