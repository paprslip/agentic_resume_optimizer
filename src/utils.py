import pdfplumber

def load(filename):
    """
    Loads the content of a file. If the file is a PDF, extracts and returns the text content.

    Args:
        filename (str): The path to the file.

    Returns:
        str: The extracted text content of the file.
    """
    if filename.endswith('.pdf'):
        with pdfplumber.open(filename) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            return text
    elif filename.endswith('.txt') or filename.endswith('.tex') or filename.endswith('.json'):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("Unsupported file format. Only PDF, text, JSON, and LaTeX files are supported.")


if __name__ == "__main__":
    print("###############################################")
    print("Loader Tester")
    print("###############################################")
    content = load("data/resume.json")
    print(content)
    print(f"Total characters loaded: {len(content)}")