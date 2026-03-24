from langchain_community.document_loaders import ArxivLoader


def load_arxiv_paper(identifier: str, search_by: str = "id") -> list:
    """
    Loads a paper from arXiv using LangChain's ArxivLoader.

    Args:
        identifier (str): The arXiv ID or the DOI.
        search_by (str): Set to 'id' for arXiv ID, or 'doi' for DOI.

    Returns
    -------
        list: A list containing LangChain Document objects.
    """
    if search_by.lower() == "doi":
        query = f"doi:{identifier}"
    else:
        query = identifier

    loader = ArxivLoader(query=query, load_max_docs=1)
    documents = loader.load()

    if not documents:
        print("No papers found matching that identifier.")

    return documents


arxiv_id = "1706.03762"
papers = load_arxiv_paper(identifier=arxiv_id, search_by="id")

if papers:
    paper = papers[0]

    print("\n--- WHAT THE RETURNED OBJECT CAN DO ---")
    print(f"Type of object: {type(paper)}\n")

    # 1. Access the Metadata (Dictionary)
    print("1. METADATA (Summary, Authors, Title, etc.):")
    print(f"Title: {paper.metadata.get('Title')}")
    print(f"Published Date: {paper.metadata.get('Published')}")
    print(f"Authors: {paper.metadata.get('Authors')}")
    print(f"Abstract Snippet: {paper.metadata.get('Summary')[:150]}...\n")

    # 2. Access the Raw Text Content
    print("2. PAGE CONTENT (The actual parsed text from the PDF):")
    print(f"First 300 characters of the paper:\n{paper.page_content[:300]}...\n")

    # 3. Check document length
    print("3. DOCUMENT LENGTH:")
    print(f"Total characters in paper: {len(paper.page_content)}")
