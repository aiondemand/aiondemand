# Code to call the model and get the response
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from aiod.automation.prompt import SYSTEM_PROMPT
from aiod.automation.pydantic import PaperExtraction


def extract_paper_metadata(
    text: str, model_ip: str = "192.168.0.169"
) -> PaperExtraction:
    """Run the extraction using Qwen 2.5 Coder on the remote GPU laptop."""
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("human", "Text to analyze:\n\n{text}")]
    )

    llm = ChatOpenAI(
        base_url=f"http://{model_ip}:1234/v1",
        api_key="not-needed",
        model="qwen2.5-coder:3b",
        max_tokens=None,
        temperature=0.0,
    )

    structured_llm = llm.with_structured_output(PaperExtraction)
    chain = prompt | structured_llm

    return chain.invoke({"text": text})
