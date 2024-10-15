from fastapi import APIRouter, HTTPException
from config.log_config import logger
from utils.utils import (
    chat_histories,
    generate_final_prompt,
    manage_chat_history,
    preprocess_text,
    validate_custom_prompt,
)
from utils.constant import MODEL_LIST
from controller.Openembedder import OpenEmbedder
from controller.Openllm import OpenLLM, ModelNotFoundError
from schemas import ChatRequest


router = APIRouter(prefix="", tags=["Chat"])


# API: Start chat with collection
@router.post(
    "/chat",
    summary="Start Chat",
    description="Initiates a chat based on the provided collection and query.",
)
async def start_chat(request: ChatRequest):
    """
    Initiates a chat session with a specific collection and processes the query.

    Args:
        request (ChatRequest): The request body containing collection_name, query, model_name,
        vector_db_name, embedding_model, and optionally, a custom_prompt.

    Returns:
        dict: The assistant's response based on the query and the context from the collection.

    Raises:
        HTTPException: Raised if the query is empty, vector database or model name is invalid,
        or an error occurs during processing.
    """

    # Extract all variables from the request body at once
    custom_prompt = request.custom_prompt

    session_id = request.collection_name

    if session_id not in chat_histories:
        chat_histories[session_id] = []

    logger.info(
        """Chat request received for collection: %s,
         model: %s, vector DB: %s""",
        request.collection_name,
        request.model_name,
        request.vector_db_name,
    )

    if not request.query.strip():
        logger.error("Received an empty query")
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if request.model_name not in MODEL_LIST:
        logger.error("Invalid model name: %s", request.model_name)
        raise HTTPException(status_code=400, detail="Invalid model name")

    try:
        embedder = OpenEmbedder(
            vectordb_name=request.vector_db_name,
            collection_name=request.collection_name,
            embedding_model_name=request.embedding_model,
        )
        llm = OpenLLM(model_name=request.model_name)
        hybrid_result = embedder.query_database(query=request.query, k=3)

        if hybrid_result is None:
            logger.error(
                """Collection not matching with provided
                        Database and embedding model"""
            )
            raise HTTPException(
                status_code=400,
                detail="""Collection not matching with
                provided Database and embedding model""",
            )

        results = "\n".join([h.page_content for h in hybrid_result])
        logger.info(
            "Query results retrieved for collection: %s", request.collection_name
        )

        chat_histories[session_id].append({"role": "user", "content": request.query})
        manage_chat_history(session_id)

        # Create the prompt including the chat history
        history_prompt = "\n".join(
            [f'{msg["role"]}: {msg["content"]}' for msg in chat_histories[session_id]]
        )

        if custom_prompt:
            # Validate the custom prompt
            validate_custom_prompt(custom_prompt)
            final_prompt = custom_prompt.format(
                query=request.query, chat_history=history_prompt, results=results
            )
        else:
            # Use the default prompt if no custom prompt is provided
            final_prompt = generate_final_prompt(history_prompt, results, request.query)

        llm_result = llm.generate_response(final_prompt)
        logger.info("LLM Response: %s", llm_result)
        processed_text = preprocess_text(llm_result)
        chat_histories[session_id].append(
            {"role": "assistant", "content": processed_text}
        )
        return {"response": llm_result}
    except ModelNotFoundError as e:
        logger.exception("Model is not downloaded yet, please download first")
        raise HTTPException(
            status_code=500,
            detail="Model is not downloaded yet, please download first.",
        ) from e

    except Exception as e:
        logger.exception("Failed to process chat request")
        raise HTTPException(
            status_code=500, detail=f"Failed to process chat request: {str(e)}"
        ) from e
