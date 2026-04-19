from pypdf import PdfReader
import os

def extract_text_from_pdf(pdf_source):
    """
    Extracts text from a PDF file. pdf_source can be a file path or a file-like object.
    """
    # Handle text files for testing/demo
    if isinstance(pdf_source, str):
        if not os.path.exists(pdf_source):
            raise FileNotFoundError(f"File not found: {pdf_source}")
        if pdf_source.endswith('.txt'):
            with open(pdf_source, 'r') as f:
                return f.read().strip()
    elif hasattr(pdf_source, 'name') and pdf_source.name.endswith('.txt'):
        return pdf_source.read().decode('utf-8').strip()

    text = ""
    try:
        reader = PdfReader(pdf_source)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    
    return text.strip()

if __name__ == "__main__":
    # Quick test
    import sys
    if len(sys.argv) > 1:
        extracted_text = extract_text_from_pdf(sys.argv[1])
        if extracted_text:
            print("Successfully extracted text.")
            print(extracted_text[:500] + "...")
        else:
            print("Failed to extract text.")
    else:
        print("Usage: python parser.py <path_to_pdf>")
