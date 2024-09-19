import os
import uuid
from pathlib import Path
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2

from Openllm import OpenLLM
from constant import VECTOR_DB_LIST, LLM_OPTIONS, MODEL_LIST
from schemas import UploadResponse
from Openembedder import OpenEmbedder
from utils import chat_histories, manage_chat_history, preprocess_text

# Set up logging
log_file_path = "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Open RAG",
    description="An API for managing LLM operations, file uploads, and chat functionalities.",
    version="0.1",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins, you can use ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods: GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)

session_histories = {}
MAX_TOKENS = 4000

# Ensure temporary directory exists
tmp_dir = Path("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)


@app.get("/", summary="Hello API", description="Returns a basic 'Hello' message.")
def hello_api():
    """
    Endpoint to return a basic greeting message.

    This is a simple GET request that returns a basic 'Hello FastAPI' message.

    Returns:
        dict: A dictionary containing a greeting message.
    """

    logger.info("Hello API called")
    return {"msg": "Hello OpenRAG"}


@app.get(
    "/llm-options",
    summary="Get LLM Options",
    description="Retrieves the available options for Large Language Models (LLM).",
)
async def get_llm_options():
    """
    Endpoint to retrieve available Large Language Models (LLM) options.

    Returns:
        dict: A dictionary of LLM options available for users.
    """

    logger.info("Fetching LLM options")
    return LLM_OPTIONS


# API: upload file and get collection to chat
@app.post(
    "/upload",
    summary="Upload PDF",
    description="""Allows for uploading a PDF file, which will be
    processed and stored in the vector database.""",
    response_model=UploadResponse,
)
async def upload_pdf(
    model_name: str = Form(...),
    vector_db_name: str = Form(...),
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


@app.get(
    "/check-collection",
    summary="Check Collection",
    description="Verifies if a specific collection exists in the vector database.",
)
async def check_collection(collection_name: str, vector_db_name: str):
    """
    Verifies if a collection exists in the specified vector database.

    Args:
        collection_name (str): The name of the collection to check.
        vector_db_name (str): The vector database in which to check the collection.

    Returns:
        dict: A message indicating whether the collection is validated.

    Raises:
        HTTPException: Raised if the vector database name is invalid or if the
        collection cannot be validated.
    """

    logger.info(
        """Collection check request received for collection: %s,
         vector DB: %s""",
        collection_name,
        vector_db_name,
    )
    if vector_db_name not in VECTOR_DB_LIST:
        logger.error("Invalid vector database name: %s", vector_db_name)
        raise HTTPException(status_code=400, detail="Invalid vector database name")

    try:
        OpenEmbedder(vectordb_name=vector_db_name, collection_name=collection_name)
        return {"message": "Validated"}
    except Exception as e:
        logger.exception("Failed to validate collection")
        raise HTTPException(
            status_code=400, detail=f"Failed to validate collection: {str(e)}"
        ) from e


# API: Start chat with collection
@app.post(
    "/chat",
    summary="Start Chat",
    description="Initiates a chat based on the provided collection and query.",
)
async def start_chat(
    collection_name: str, query: str, model_name: str, vector_db_name: str
):
    """
    Initiates a chat session with a specific collection and processes the query.

    Args:
        collection_name (str): The collection name that has been uploaded.
        query (str): The user's query to search against the collection.
        model_name (str): The Large Language Model (LLM) to be used.
        vector_db_name (str): The vector database being used for the collection.

    Returns:
        dict: The assistant's response based on the query and the context from the collection.

    Raises:
        HTTPException: Raised if the query is empty, vector database or model name is invalid,
        or an error occurs during processing.
    """

    session_id = collection_name

    if session_id not in chat_histories:
        chat_histories[session_id] = []

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

        chat_histories[session_id].append({"role": "user", "content": query})
        manage_chat_history(session_id)

        # Create the prompt including the chat history
        history_prompt = "\n".join(
            [f'{msg["role"]}: {msg["content"]}' for msg in chat_histories[session_id]]
        )

        final_prompt = f"""
            Chat History:
            {history_prompt}

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
        processed_text = preprocess_text(llm_result)
        chat_histories[session_id].append(
            {"role": "assistant", "content": processed_text}
        )
        return {"response": llm_result}

    except Exception as e:
        logger.exception("Failed to process chat request")
        raise HTTPException(
            status_code=500, detail=f"Failed to process chat request: {str(e)}"
        ) from e
