import os

import fitz  # PyMuPDF


def extract_text_from_pdf(
    pdf_path: str,
    head_pages: int = 5,
    tail_pages: int = 3,
    max_chars: int = 60000,
) -> str:
    """Extract high-priority PDF text for LLM extraction in the population stage."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find PDF at {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        if total_pages == 0:
            doc.close()
            raise ValueError("The PDF appears to be empty.")

        if total_pages <= (head_pages + tail_pages):
            full_text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return full_text[:max_chars]

        head_text = "\n".join(doc[i].get_text() for i in range(head_pages))
        tail_text = "\n".join(
            doc[i].get_text() for i in range(total_pages - tail_pages, total_pages)
        )
        doc.close()

        combined_text = (
            f"{head_text}\n\n[... DOCUMENT TRUNCATED FOR CONTEXT ...]\n\n{tail_text}"
        )
        return combined_text[:max_chars]
    except Exception as exc:
        raise RuntimeError(f"Failed to extract PDF text: {exc}") from exc
