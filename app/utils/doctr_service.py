import io
import threading
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


class DoctrOCRService:
    """
    Singleton OCR service — loads the model once, thread-safely.
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.model = ocr_predictor(pretrained=True)

    @classmethod
    def get_instance(cls) -> "DoctrOCRService":
        """Return (or create) the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def process_document(self, file_path: str):
        """
        Process a PDF or image file on disk and return the doctr result object.
        """
        if file_path.lower().endswith(".pdf"):
            doc = DocumentFile.from_pdf(file_path)
        else:
            doc = DocumentFile.from_images(file_path)

        return self.model(doc)

    def process_document_bytes(self, file_bytes: bytes, filename: str):
        """
        Process raw file bytes (in-memory) without writing to disk.
        """
        buffer = io.BytesIO(file_bytes)

        if filename.lower().endswith(".pdf"):
            doc = DocumentFile.from_pdf(buffer)
        else:
            doc = DocumentFile.from_images(buffer)

        return self.model(doc)