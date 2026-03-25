# Code to call the model and get the response
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from aiod.automation.prompt import SYSTEM_PROMPT
from aiod.automation.pydantic import Paper, PaperExtraction
from aiod.cross_linkages._loaders._arxiv import ArxivLoader


def extract_paper_data(text: str, model_ip: str = "192.168.0.169") -> PaperExtraction:
    """Run the extraction using Qwen 2.5 Coder on the remote GPU laptop."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Text to analyze:\n\n{text}",
            ),
        ]
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


def get_paper(url: str, model_ip: str = "192.168.0.169") -> Paper:
    """Get paper metadata by URL."""
    loader = ArxivLoader()
    documents = loader.load(url)
    if documents:
        text = documents[0].page_content

    metadata = extract_paper_data(text, model_ip)
    return Paper(url, metadata)
