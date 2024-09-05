import os
import uuid
from pathlib import Path
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import PyPDF2

from Openllm import OpenLLM
from constant import VECTOR_DB_LIST, LLM_OPTIONS, MODEL_LIST
from schemas import UploadResponse
from Openembedder import OpenEmbedder

# Set up logging
log_file_path = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Open RAG", version="0.1")

session_histories = {}
MAX_TOKENS = 4000

# Ensure temporary directory exists
tmp_dir = Path("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)


@app.get("/")
def hello_api():
    logger.info("Hello API called")
    return {"msg": "Hello FastAPI🚀"}


@app.get("/llm-options")
async def get_llm_options():
    logger.info("Fetching LLM options")
    return LLM_OPTIONS


# API: upload file and get collection to chat
@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    model_name: str = Form(...),
    vector_db_name: str = Form(...),
    file: UploadFile = File(...),
):
    logger.info(
        "Upload request received for model: %s and vector DB: %s",
        model_name,
        vector_db_name,
    )

    if vector_db_name not in VECTOR_DB_LIST:
        logger.error("Invalid vector database name: %s", vector_db_name)
        raise HTTPException(status_code=400, detail="Invalid vector database name")

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
            pdf_text += reader.pages[page].extract_text()

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


# API: Start chat with collection
@app.post("/chat")
async def start_chat(
    collection_name: str, query: str, model_name: str, vector_db_name: str
):
    logger.info(
        """Chat request received for collection: %s,
         model: %s, vector DB: %s""",
        collection_name,
        model_name,
        vector_db_name,
    )

    if not query.strip():
        logger.error("Received an empty query")
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if vector_db_name not in VECTOR_DB_LIST:
        logger.error("Invalid vector database name: %s", vector_db_name)
        raise HTTPException(status_code=400, detail="Invalid vector database name")

    if model_name not in MODEL_LIST:
        logger.error("Invalid model name: %s", model_name)
        raise HTTPException(status_code=400, detail="Invalid model name")

    try:
        embedder = OpenEmbedder(
            vectordb_name=vector_db_name, collection_name=collection_name
        )
        llm = OpenLLM(model_name=model_name)
        hybrid_result = embedder.query_database(query=query, k=3)
        results = "\n".join([h.page_content for h in hybrid_result])
        logger.info("Query results retrieved for collection: %s", collection_name)

        # Retrieve or initialize chat history
        # history = session_histories.get(collection_name, "")

        # Format the prompt with history, context, and current query
        # new_interaction = f"User: {query}\nAI: {results}\n"
        # combined_prompt = f"{history}"

        # Trim history if the prompt exceeds MAX_TOKENS
        # while len(combined_prompt) > MAX_TOKENS:
        #     first_interaction_end = combined_prompt.find("AI: ") + len("AI: ")
        #     combined_prompt = combined_prompt[first_interaction_end:]

        # Store updated history back to the session
        # session_histories[collection_name] = combined_prompt

        final_prompt = f"""
            Context:
            {results}

            Prompt:
            1. Give a response matching with the query.
            2. Only respond from the above context.
            3. Provide an answer in a good format.
            4. Do not repeat the query.
            5. Do not add questions in the response.
            6. Do not repeat the prompt in the response.

            Query:
            {query}
        """

        llm_result = llm.generate_response(final_prompt)
        logger.info("LLM Response: %s", llm_result)

        return {"response": llm_result}

    except Exception as e:
        logger.exception("Failed to process chat request")
        raise HTTPException(
            status_code=500, detail=f"Failed to process chat request: {str(e)}"
        ) from e
