import hashlib
import json

from typing import Union


class HashingUtils:
    """
    Utility class for generating deterministic hashes
    for documents or structured data.
    """

    @staticmethod
    def sha256_from_text(text: str) -> str:
        """
        Generate SHA256 hash from plain text.
        """
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def sha256_from_json(data: Union[dict, list]) -> str:
        """
        Deterministic hashing for structured OCR data.
        """
        normalized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()