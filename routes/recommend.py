from fastapi import APIRouter, HTTPException
from models.schemas import RecommendRequest, RecommendResponse
from services.recommendation_service import recommendation_engine

router = APIRouter()

@router.post("/api/recommend", response_model=RecommendResponse, tags=["Recommendations"])
async def get_recommendations(request: RecommendRequest):
    try:
        results = recommendation_engine.recommend(request.symptoms)
        
        # Apply limits if provided
        limit = request.limit if request.limit else 3
        exercises = results["exercises"][:limit]
        games = results["games"][:limit]
        
        return {
            "exercises": exercises,
            "games": games
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation engine error: {str(e)}")
