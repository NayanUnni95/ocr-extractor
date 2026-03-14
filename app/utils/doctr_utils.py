from __future__ import annotations

from typing import Any

from .doctr_service import DoctrOCRService


def doctr_to_dict(result) -> dict[str, Any]:
    """
    Return the raw doctr export dict (structured layout JSON).
    """
    return result.export()


def doctr_to_plain_text(result) -> str:
    """
    Flatten all words to a single plain-text string, preserving newlines
    between lines and blank lines between blocks.
    """
    lines: list[str] = []
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                words = [word.value for word in line.words]
                lines.append(" ".join(words))
            lines.append("")
    return "\n".join(lines).strip()


def doctr_to_words(result) -> list[dict[str, Any]]:
    """
    Return a flat list of every word with its page index, confidence score,
    and bounding-box geometry.
    """
    words: list[dict[str, Any]] = []
    for page_idx, page in enumerate(result.pages):
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    words.append(
                        {
                            "page": page_idx,
                            "word": word.value,
                            "confidence": round(float(word.confidence), 4),
                            "geometry": word.geometry,
                        }
                    )
    return words


def doctr_to_pages(result) -> list[dict[str, Any]]:
    """
    Return per-page summary: page index, dimensions, and all extracted text
    lines grouped by block.
    """
    pages: list[dict[str, Any]] = []
    for page_idx, page in enumerate(result.pages):
        blocks: list[dict[str, Any]] = []
        for block in page.blocks:
            block_lines: list[str] = []
            for line in block.lines:
                block_lines.append(" ".join(w.value for w in line.words))
            blocks.append(
                {
                    "geometry": block.geometry,
                    "lines": block_lines,
                }
            )
        pages.append(
            {
                "page": page_idx,
                "dimensions": page.dimensions,
                "blocks": blocks,
            }
        )
    return pages


def doctr_avg_confidence(result) -> float:
    """
    Compute the document-wide average word confidence score (0-1).
    Returns 0.0 if no words are found.
    """
    total, count = 0.0, 0
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    total += float(word.confidence)
                    count += 1
    return round(total / count, 4) if count else 0.0


def extract_document_text(file_path: str, structured: bool = False) -> Any:
    """
    Convenience wrapper for file-path based OCR extraction.
    """
    ocr_service = DoctrOCRService.get_instance()
    result = ocr_service.process_document(file_path)
    return doctr_to_dict(result) if structured else doctr_to_plain_text(result)


def extract_document_from_bytes(
    file_bytes: bytes,
    filename: str,
    structured: bool = False,
) -> Any:
    """
    OCR extraction directly from in-memory bytes (no temp file required).
    """
    ocr_service = DoctrOCRService.get_instance()
    result = ocr_service.process_document_bytes(file_bytes, filename)
    return doctr_to_dict(result) if structured else doctr_to_plain_text(result)


def build_json_ocr_response(
    file_bytes: bytes,
    filename: str,
) -> dict[str, Any]:
    """
    Full structured OCR response consumed by the /json-ocr/ endpoint.
    """
    ocr_service = DoctrOCRService.get_instance()
    result = ocr_service.process_document_bytes(file_bytes, filename)

    return {
        "filename": filename,
        "page_count": len(result.pages),
        "avg_confidence": doctr_avg_confidence(result),
        "plain_text": doctr_to_plain_text(result),
        "pages": doctr_to_pages(result),
        "structured": doctr_to_dict(result),
    }