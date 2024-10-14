from pathlib import Path
import os
import uuid

from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from schemas import UploadResponse
from config.log_config import logger
from utils.constant import MODEL_LIST, VectorDB, EmbeddingModel
from controller.upload_file import extract_and_create_temp_file
from controller.Openembedder import OpenEmbedder
from controller.Openllm import OpenLLM

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
    embedding_model: EmbeddingModel = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a PDF file for processing and storing in the vector database.

    Args:
        model_name (str): The name of the Large Language Model (LLM) to be used.
        vector_db_name (str): The vector database in which the PDF will be stored.
        file (UploadFile): The uploaded PDF file.
        embedding_model (str): The embedding model which will embed the text.

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

    is_model_exists = OpenLLM.model_exists(model_name)

    if not is_model_exists:
        logger.error("Model is not downloaded, Please download first: %s", model_name)
        raise HTTPException(
            status_code=400, detail="Model is not downloaded, Please download first"
        )

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
        extract_and_create_temp_file(file, tmp_file_path)
        logger.info("PDF text extracted and saved to %s", tmp_file_path)
    except Exception as e:
        logger.exception("Failed to process PDF")
        raise HTTPException(
            status_code=500, detail=f"Failed to process PDF: {str(e)}"
        ) from e

    collection_name = uuid.uuid4().hex
    try:
        embedder = OpenEmbedder(
            vectordb_name=vector_db_name,
            collection_name=collection_name,
            embedding_model_name=embedding_model,
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
