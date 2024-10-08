import io

# def test_pdf_upload_200(client):
#     # Create a valid minimal PDF content
#     valid_pdf_content = (
#         b"%PDF-1.4\n"
#         b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
#         b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
#         b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
#         b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
#         b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
#         b"%%EOF\n"
#     )

#     file_content = io.BytesIO(valid_pdf_content)
#     file_content.name = "test.pdf"
#     response = client.post(
#         "/upload",
#         data={"model_name": "Meta-Llama-3-8B-Instruct.Q4_0.gguf", "vector_db_name": "faiss"},
#         files={"file": ("test.pdf", file_content, "application/pdf")},
#     )
#     data = response.json()
#     assert response.status_code == 200


def test_pdf_upload_no_model_key_422(client):
    # Create a valid minimal PDF content
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
        b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
        b"%%EOF\n"
    )

    file_content = io.BytesIO(valid_pdf_content)
    file_content.name = "test.pdf"
    response = client.post(
        "/upload",
        data={
            "vector_db_name": "faiss",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 422


def test_pdf_upload_wrong_model_name_400(client):
    # Create a valid minimal PDF content
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
        b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
        b"%%EOF\n"
    )

    file_content = io.BytesIO(valid_pdf_content)
    file_content.name = "test.pdf"
    response = client.post(
        "/upload",
        data={
            "model_name": "test-model",
            "vector_db_name": "faiss",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 400


def test_pdf_upload_no_file_key_422(client):
    response = client.post(
        "/upload",
        data={
            "model_name": "test-model",
            "vector_db_name": "faiss",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
    )
    assert response.status_code == 422


def test_pdf_upload_no_vector_db_key_422(client):
    # Create a valid minimal PDF content
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
        b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
        b"%%EOF\n"
    )

    file_content = io.BytesIO(valid_pdf_content)
    file_content.name = "test.pdf"
    response = client.post(
        "/upload",
        data={
            "model_name": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 422


def test_pdf_upload_wrong_vector_db_422(client):
    # Create a valid minimal PDF content
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
        b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
        b"%%EOF\n"
    )

    file_content = io.BytesIO(valid_pdf_content)
    file_content.name = "test.pdf"
    response = client.post(
        "/upload",
        data={
            "model_name": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
            "vector_db_name": "test",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 422


def test_pdf_upload_wrong_file_content_400(client):
    # Create a valid minimal PDF content
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
        b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
        b"%%EOF\n"
    )

    file_content = io.BytesIO(valid_pdf_content)
    file_content.name = "test.pdf"
    response = client.post(
        "/upload",
        data={
            "model_name": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
            "vector_db_name": "faiss",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
        files={"file": ("test.pdf", file_content, "application/json")},
    )
    assert response.status_code == 400


def test_pdf_upload_large_file_size_400(client):
    # Create a valid minimal PDF content
    valid_pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] >>\nendobj\n"
        b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000074 00000 n \n"
        b"0000000178 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n261\n"
        b"%%EOF\n"
    )

    # Repeat the content to exceed 10 MB
    large_pdf_content = valid_pdf_content * (
        10 * 1024 * 1024 // len(valid_pdf_content) + 1
    )

    file_content = io.BytesIO(large_pdf_content)
    file_content.name = "test.pdf"
    response = client.post(
        "/upload",
        data={
            "model_name": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
            "vector_db_name": "faiss",
            "embedding_model": "mixedbread-ai/mxbai-embed-large-v1",
        },
        files={"file": ("test.pdf", file_content, "application/pdf")},
    )
    assert response.status_code == 400
