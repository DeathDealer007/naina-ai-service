from fastapi import APIRouter
from models.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Utility"])
async def health_check():
    return {"status": "ok"}
