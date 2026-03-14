from fastapi import APIRouter

router = APIRouter()


@router.get("/health/")
async def common():
    return {"message": "✅ Server is healthy and running 🚀"}