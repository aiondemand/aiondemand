# example_usage.py

from aiod.cross_linkages._loaders._arxiv import ArxivLoader



def run_arxiv_example():
    # 1. Initialize the loader
    # This will trigger the _check_soft_dependencies check
    loader = ArxivLoader()

    # 2. Define the ArXiv URL (can be /abs/ or /pdf/ format)
    # Example: "Attention Is All You Need" paper
    paper_url = "https://arxiv.org/abs/1706.03762"

    print(f"--- Fetching paper from: {paper_url} ---")

        # 3. Load the document
        # documents is a List[Document]
    documents = loader.load(paper_url)
    print(documents)

        