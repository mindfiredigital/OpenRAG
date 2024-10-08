import PyPDF2


def extract_and_create_temp_file(file, tmp_file_path):
    pdf_text = ""
    reader = PyPDF2.PdfReader(file.file)
    for _, page in enumerate(reader.pages):  # Use enumerate for iteration
        pdf_text += page.extract_text()

    with open(tmp_file_path, "w", encoding="utf-8") as f:
        f.write(pdf_text)
