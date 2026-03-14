from fastapi import APIRouter

from app.api.endpoints import common, manage_ocr

api_router = APIRouter()

api_router.include_router(common.router, prefix="/common")
api_router.include_router(manage_ocr.router, prefix="/manage-ocr")