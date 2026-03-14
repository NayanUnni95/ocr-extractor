if __name__ == "__main__":
    import uvicorn
    import os
    from app.core.config import settings

    port = int(os.environ.get("PORT", 8000))
    workers = int(os.environ.get("WORKERS", 1))

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=settings.IS_DEV, workers=workers)