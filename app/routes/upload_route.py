from pathlib import Path
import os
import uuid
import PyPDF2

from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from schemas import UploadResponse
from config.log_config import logger
from utils.constant import MODEL_LIST, VectorDB
from controller.Openembedder import OpenEmbedder

# Ensure temporary directory exists
tmp_dir = Path("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="", tags=["Upload"])


@router.post(
    "/upload",
    summary="Upload PDF",
    description="""Allows for uploading a PDF file, which will be
    processed and stored in the vector database.""",
    response_model=UploadResponse,
)
async def upload_pdf(
    model_name: str = Form(...),
    vector_db_name: VectorDB = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a PDF file for processing and storing in the vector database.

    Args:
        model_name (str): The name of the Large Language Model (LLM) to be used.
        vector_db_name (str): The vector database in which the PDF will be stored.
        file (UploadFile): The uploaded PDF file.

    Returns:
        UploadResponse: A response object containing the generated collection name.

    Raises:
        HTTPException: Raised if the file is not a PDF, the file size exceeds 10 MB,
        or the vector DB/model name is invalid.
    """

    logger.info(
        "Upload request received for model: %s and vector DB: %s",
        model_name,
        vector_db_name,
    )

    if model_name not in MODEL_LIST:
        logger.error("Invalid model name: %s", model_name)
        raise HTTPException(status_code=400, detail="Invalid model name")

    if file.content_type != "application/pdf":
        logger.error("Invalid file type: %s", file.content_type)
        raise HTTPException(status_code=400, detail="File must be a PDF")

    file_size = file.size
    if file_size > 10 * 1024 * 1024:  # 10 MB in bytes
        logger.error("File size exceeds limit: %s", file_size)
        raise HTTPException(
            status_code=400, detail="PDF file size must be less than 10 MB"
        )

    tmp_filename = uuid.uuid4().hex + ".txt"
    tmp_file_path = tmp_dir / tmp_filename

    try:
        pdf_text = ""
        reader = PyPDF2.PdfReader(file.file)
        for _, page in enumerate(reader.pages):  # Use enumerate for iteration
            pdf_text += page.extract_text()

        with open(tmp_file_path, "w", encoding="utf-8") as f:
            f.write(pdf_text)

        logger.info("PDF text extracted and saved to %s", tmp_file_path)

    except Exception as e:
        logger.exception("Failed to process PDF")
        raise HTTPException(
            status_code=500, detail=f"Failed to process PDF: {str(e)}"
        ) from e

    collection_name = uuid.uuid4().hex
    try:
        embedder = OpenEmbedder(
            vectordb_name=vector_db_name, collection_name=collection_name
        )
        embedder.create_database(str(tmp_file_path))
        logger.info("Database created for collection: %s", collection_name)

    except Exception as e:
        logger.exception("Failed to create database")
        raise HTTPException(
            status_code=500, detail=f"Failed to create database: {str(e)}"
        ) from e

    finally:
        if tmp_file_path.exists():
            os.remove(tmp_file_path)
            logger.info("Temporary file %s removed", tmp_file_path)

    return UploadResponse(collection_name=collection_name)
