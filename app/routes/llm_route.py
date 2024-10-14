from fastapi import APIRouter, HTTPException
from utils.constant import LLM_OPTIONS, VectorDB, EmbeddingModel, MODEL_LIST
from controller.Openembedder import OpenEmbedder
from controller.Openllm import OpenLLM, ModelDownloadInProgressError
from config.log_config import logger
from schemas import ModelName

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
async def check_collection(
    collection_name: str, vector_db_name: VectorDB, embedding_model: EmbeddingModel
):
    """
    Verifies if a collection exists in the specified vector database.

    Args:
        collection_name (str): The name of the collection to check.
        vector_db_name (str): The vector database in which to check the collection.
        embedding_model (str): The embedding model used while uploading the file

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
        embed = OpenEmbedder(
            vectordb_name=vector_db_name,
            collection_name=collection_name,
            embedding_model_name=embedding_model,
        )
        if embed.vectordb is None:
            raise HTTPException(status_code=400, detail="Failed to validate collection")
        return {"message": "Validated"}
    except Exception as e:
        logger.exception("Failed to validate collection")
        raise HTTPException(
            status_code=400, detail=f"Failed to validate collection: {str(e)}"
        ) from e


@router.get(
    "/vector-db-list",
    summary="Vector DB Lists",
    description="Provides all the supported vector db lists",
)
async def vector_db_list():
    """
    Endpoint to retrieve the list of supported vector databases.

    Returns:
        list: A list of lowercase string names representing the supported
        vector databases.

    Example Response:
        [
            "chromadb",
            "qdrant",
            "faiss"
        ]
    """

    # Create a list of all enum names, converted to lowercase.
    lists = [db.name.lower() for db in VectorDB]
    return lists


@router.post(
    "/download-model",
    summary="Download a GPT4All model",
    description="""Initiates the download of a specified
            GPT4All model if it is not already available locally.""",
)
async def model_download(item: ModelName):
    """
    Initiates the download of a GPT4All model if it is not already available locally.
    If the model is already downloaded, a message is returned indicating this.
    If a download is currently in progress, an appropriate message is returned as well.

    Args:
    -----
    item (ModelName):
        An instance of `ModelName` which contains the name of the model to be downloaded.

    Raises:
    -------
    HTTPException:
        - If the `model_name` is empty or invalid.
        - If the model download is already in progress.

    Returns:
    --------
    dict:
        A JSON response indicating the status of the download:
        - "Model is already downloaded" if the model exists locally.
        - "Model download in progress, please wait" if the download is ongoing.
        - "Model download started!" if the download is successfully initiated.
    """

    model_name = item.model_name
    if model_name == "":
        logger.error("Model name can not be empty")
        raise HTTPException(status_code=400, detail="Model name can not be empty")

    if model_name not in MODEL_LIST:
        logger.error("Invalid model name: %s", model_name)
        raise HTTPException(status_code=400, detail="Invalid model name for dwonload")
    try:
        model_status = OpenLLM.download_model(model_name)
        if model_status:
            return {"detail": "Model is already downloaded"}
    except ModelDownloadInProgressError as e:
        logger.info("Model download in progress: %s", model_name)
        raise HTTPException(
            status_code=200, detail="Model download in progress, please wait"
        ) from e
    return {"detail": "Model download started!"}
