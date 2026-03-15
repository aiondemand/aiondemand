from aiod.automation.pdf import extract_text_from_pdf

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract text from PDF for AIoD metadata extraction.')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('--head_pages', type=int, default=5)
    parser.add_argument('--tail_pages', type=int, default=3)
    parser.add_argument('--max_chars', type=int, default=60000)
    args = parser.parse_args()
    print(extract_text_from_pdf(args.pdf_path, head_pages=args.head_pages, tail_pages=args.tail_pages, max_chars=args.max_chars))
