import PyPDF2


def extract_and_create_temp_file(file, tmp_file_path):
    """
    Extracts text from a PDF file and writes it to a temporary file.

    This function reads the content of a provided PDF file, extracts the text from each page,
    and writes the combined text into a specified temporary file.

    Args:
        file (File): The file object containing the PDF to extract text from.
        tmp_file_path (str): The path where the extracted text will be saved as a temporary file.

    Returns:
        None

    Raises:
        PyPDF2.utils.PdfReadError: If there is an issue reading the PDF file.
    """

    pdf_text = ""
    reader = PyPDF2.PdfReader(file.file)
    for _, page in enumerate(reader.pages):  # Use enumerate for iteration
        pdf_text += page.extract_text()

    with open(tmp_file_path, "w", encoding="utf-8") as f:
        f.write(pdf_text)
