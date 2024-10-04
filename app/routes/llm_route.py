from fastapi import APIRouter, HTTPException
from utils.constant import LLM_OPTIONS, VectorDB
from controller.Openembedder import OpenEmbedder
from config.log_config import logger

router = APIRouter(prefix="", tags=["LLM"])


@router.get(
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


@router.get(
    "/check-collection",
    summary="Check Collection",
    description="Verifies if a specific collection exists in the vector database.",
)
async def check_collection(collection_name: str, vector_db_name: VectorDB):
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

    try:
        OpenEmbedder(vectordb_name=vector_db_name, collection_name=collection_name)
        return {"message": "Validated"}
    except Exception as e:
        logger.exception("Failed to validate collection")
        raise HTTPException(
            status_code=400, detail=f"Failed to validate collection: {str(e)}"
        ) from e
