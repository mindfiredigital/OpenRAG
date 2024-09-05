from pydantic import BaseModel

class UploadResponse(BaseModel):
    collection_name: str
