from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.base_route import api_router


app = FastAPI(
    title="OpenRAG",
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


app.include_router(api_router)
