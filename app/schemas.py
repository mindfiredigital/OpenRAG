from pydantic import BaseModel
from utils.constant import VectorDB, EmbeddingModel


class UploadResponse(BaseModel):
    """
    A response model for the `/upload` endpoint.

    Attributes:
        collection_name (str): The name of the collection created after uploading
                               and processing the PDF file. This is used for
                               referencing the stored data in the vector database.
    """

    collection_name: str


class ChatRequest(BaseModel):
    """
    Represents the structure of the request body for initiating a chat session.

    Attributes:
        collection_name (str): The name of the collection that has been uploaded and is to
                               be queried.
        query (str): The user's query that will be searched against the collection.
        model_name (str): The Large Language Model (LLM) that will be used for processing
                          the query.
        vector_db_name (VectorDB): The vector database used for retrieving relevant results
                                   from the collection.
        embedding_model (EmbeddingModel): The embedding model that was used during the collection's
                                          upload process.
        custom_prompt (str, optional): An optional custom prompt provided by the user, containing
                    placeholders for query, chat history, and results. Defaults to None.
    """

    collection_name: str
    query: str
    model_name: str
    vector_db_name: VectorDB
    embedding_model: EmbeddingModel
    custom_prompt: str = None  # Optional custom prompt
    device: str = "cpu"


class ModelName(BaseModel):
    """
    Represents the structure of the request body for initiating a model download.

    Attributes:
        model_name (str): The Large Language Model (LLM) that will be used for downloading.
    """

    model_name: str
