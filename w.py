from aiod.cross_linkages._loaders._arxiv import ArxivLoader
from aiod.automation import extract_paper_data

# ---------------------------------------------------------------------------
# Test the integration with ArxivLoader
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 1. Load a paper from arXiv using the loader
    loader = ArxivLoader()
    documents = loader.load("https://arxiv.org/abs/1706.03762")  # Example paper

    if documents:
        paper_doc = documents[0]
        raw_text = paper_doc.page_content

        print("Loaded paper text (first 500 chars):")
        print(raw_text[:500])
        print("\n" + "=" * 50 + "\n")

        # 2. Run the extraction using the automation module
        result = extract_paper_data(raw_text)

        print("Extraction result:")
        print(result.model_dump_json(indent=2))

        print("\n" + "=" * 50 + "\n")

        # 3. Test the get command pipeline
        from aiod import get

        print("Testing get command with DOI:")
        paper_obj = get("https://arxiv.org/abs/1706.03762")

        print(paper_obj)
        print(type(paper_obj))
