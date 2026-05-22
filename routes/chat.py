from fastapi import APIRouter, HTTPException
import uuid
from models.schemas import ChatRequest, ChatResponse, RecommendationData
from services.gemini_service import GeminiService
from services.memory_service import memory_db
from services.recommendation_service import recommendation_engine

router = APIRouter()
gemini_service = GeminiService()

@router.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Establish session ID
        session_id = request.session_id
        if not session_id or session_id.strip() == "":
            session_id = str(uuid.uuid4())

        # 2. Get history and append user message
        user_msg = request.message.strip()
        memory_db.add_message(session_id, "user", user_msg)
        history = memory_db.get_history(session_id)

        # 3. Call Gemini to get response
        ai_response = gemini_service.generate_chat_response(history)

        # 4. Save response to memory
        memory_db.add_message(session_id, "model", ai_response)

        # 5. Extract contextual recommendations
        # Scan the user's message and the response for keywords
        combined_text = (user_msg + " " + ai_response).lower()
        symptoms_detected = []
        
        if any(w in combined_text for w in ["strain", "tired", "burn", "ache", "sore", "hurt", "pressure"]):
            symptoms_detected.append("eye strain")
        if any(w in combined_text for w in ["dry", "blink", "gritty", "scratchy", "watery"]):
            symptoms_detected.append("dry eyes")
        if any(w in combined_text for w in ["focus", "concentrat", "distract", "game", "reflex", "attention"]):
            symptoms_detected.append("low focus")
        if any(w in combined_text for w in ["fatigue", "screen", "break", "posture", "neck", "shoulder"]):
            symptoms_detected.append("screen fatigue")

        recommendations = None
        if symptoms_detected:
            rec_results = recommendation_engine.recommend(symptoms_detected)
            # Limit recommendations to 2 items per category for inline messaging to keep it clean
            recommendations = RecommendationData(
                exercises=rec_results["exercises"][:2],
                games=rec_results["games"][:2]
            )

        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            recommendations=recommendations
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"AI service chat error: {str(e)}")
