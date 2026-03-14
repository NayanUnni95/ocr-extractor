from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from app.utils.doctr_utils import build_json_ocr_response

router = APIRouter()

_ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/tiff",
    "image/bmp",
    "image/webp",
}

_ALLOWED_EXTENSIONS = {".pdf", ".jpeg", ".jpg", ".png", ".tiff", ".tif", ".bmp", ".webp"}


def _validate_file(file: UploadFile) -> None:
    """Raise 400 if the uploaded file is not a supported type."""
    suffix = "." + (file.filename or "").rsplit(".", 1)[-1].lower()
    content_type = (file.content_type or "").lower()

    if suffix not in _ALLOWED_EXTENSIONS and content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type '{file.filename}'. "
                f"Accepted types: PDF, JPEG, PNG, TIFF, BMP, WEBP."
            ),
        )

@router.post("/json-ocr/")
async def json_ocr(file: UploadFile):
    _validate_file(file)
    try:
        file_bytes = await file.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to read uploaded file: {exc}",
        ) from exc

    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        result = build_json_ocr_response(file_bytes, file.filename or "document")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OCR processing failed: {exc}",
        ) from exc

    return result