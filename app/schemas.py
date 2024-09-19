from pydantic import BaseModel


class UploadResponse(BaseModel):
    """
    A response model for the `/upload` endpoint.

    Attributes:
        collection_name (str): The name of the collection created after uploading
                               and processing the PDF file. This is used for
                               referencing the stored data in the vector database.
    """

    collection_name: str
