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
    official_github: List[str] = Field(default_factory=list)
    unofficial_github: List[str] = Field(default_factory=list)
    pypi_packages: List[str] = Field(default_factory=list)
    related_code_used: List[str] = Field(default_factory=list)
    artefacts: Artefacts = Field(
        description="Granular ML components like estimators, datasets, and metrics."
    )

# ---------------------------------------------------------------------------
# 2. Prompts & Regex
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert machine learning metadata extraction engine designed to cross-link scientific papers with software artifacts for the AI-on-Demand (AIoD) catalogue.

Your task is to analyze excerpts from research papers and extract a structured JSON object.

### CORE DEFINITIONS
1. Official Implementation: The paper's own code or package.
2. Unofficial Implementation: Third-party community reproductions.
3. Used in Experiments: Frameworks, libraries, and datasets used.

### GRANULAR ARTIFACT EXTRACTION
- Estimators: Capture model class names and hyperparameters. Format as a valid Python string (e.g., "XGBClassifier(max_depth=3)").

### MANDATORY RULES
- Output strictly valid JSON matching the schema.
- Do not guess parameters or artifacts not explicitly mentioned.
"""

def extract_urls_deterministic(text: str) -> Dict[str, List[str]]:
    github_re = re.compile(r"https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]*[\w]", re.IGNORECASE)
    pypi_re = re.compile(r"https?://pypi\.org/project/([\w.-]+)", re.IGNORECASE)
    return {
        "candidate_githubs": list(set(github_re.findall(text))),
        "candidate_pypis": list(set(pypi_re.findall(text)))
    }

# ---------------------------------------------------------------------------
# 3. LLM Orchestration (Configured for remote Qwen 2.5 Coder)
# ---------------------------------------------------------------------------

def extract_paper_metadata(text: str) -> PaperExtraction:
    """Runs the extraction using Qwen 2.5 Coder on the remote GPU laptop."""
    
    hints = extract_urls_deterministic(text)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Text to analyze:\n\n{text}\n\n(Hint: found these candidate URLs: {hints})")
    ])

    # Connecting to your other laptop via the OpenAI-compatible endpoint
    # Note: 11434 is the default for Ollama. Use 1234 if using LM Studio.
    llm = ChatOpenAI(
        base_url=f"",
        api_key="not-needed", 
        model="qwen2.5-coder:3b",
        max_tokens=None,
        temperature=0.0
    )

    # Bind the Pydantic schema
    structured_llm = llm.with_structured_output(PaperExtraction)

    chain = prompt | structured_llm
    
    return chain.invoke({"text": text, "hints": hints})

# ---------------------------------------------------------------------------
# 4. Main Loop
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Set your GPU laptop's IP here
    
    # 2. Extract text using your 'w.py' module
    raw_text = extract_text_from_pdf(r"")
        
    # 3. Run the extraction
    result = extract_paper_metadata(raw_text)
        
    print(result.model_dump_json(indent=2))