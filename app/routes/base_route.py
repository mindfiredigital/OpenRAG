from fastapi import APIRouter
from . import chat_route, llm_route, upload_route

api_router = APIRouter()

api_router.include_router(chat_route.router)
api_router.include_router(llm_route.router)
api_router.include_router(upload_route.router)
