import os
import fitz  # PyMuPDF

def extract_text_from_pdf(
    pdf_path: str, 
    head_pages: int = 5, 
    tail_pages: int = 3, 
    max_chars: int = 60000
) -> str:
    """
    Extracts text from a PDF, prioritizing the beginning and end of the document
    to capture abstracts, introductions, and references while fitting within LLM context windows.

    Args:
        pdf_path: Local path to the PDF file.
        head_pages: Number of pages to extract from the start of the document.
        tail_pages: Number of pages to extract from the end of the document.
        max_chars: Maximum characters to return to prevent token limit overflow.

    Returns:
        A formatted string containing the extracted text.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find PDF at {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        if total_pages == 0:
            doc.close()
            raise ValueError("The PDF appears to be empty.")

        # If the document is short, just grab the whole thing
        if total_pages <= (head_pages + tail_pages):
            full_text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return full_text[:max_chars]

        # For longer documents, grab the head and tail
        head_text = "\n".join(doc[i].get_text() for i in range(head_pages))
        tail_text = "\n".join(doc[i].get_text() for i in range(total_pages - tail_pages, total_pages))
        doc.close()

        # Combine with a clear divider so the LLM knows text was skipped
        combined_text = f"{head_text}\n\n[... DOCUMENT TRUNCATED FOR CONTEXT ...]\n\n{tail_text}"
        
        return combined_text[:max_chars]

    except Exception as e:
        raise RuntimeError(f"Failed to process PDF {pdf_path}: {str(e)}")