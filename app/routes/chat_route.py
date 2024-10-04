from fastapi import APIRouter, HTTPException
from config.log_config import logger
from utils.utils import chat_histories, manage_chat_history, preprocess_text
from utils.constant import MODEL_LIST, VectorDB
from controller.Openembedder import OpenEmbedder
from controller.Openllm import OpenLLM


router = APIRouter(prefix="", tags=["Chat"])


# API: Start chat with collection
@router.post(
    "/chat",
    summary="Start Chat",
    description="Initiates a chat based on the provided collection and query.",
)
async def start_chat(
    collection_name: str, query: str, model_name: str, vector_db_name: VectorDB
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
