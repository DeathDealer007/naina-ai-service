from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user message to send to the chatbot")
    session_id: Optional[str] = Field(None, description="Unique session identifier for conversation history")

class ExerciseSchema(BaseModel):
    id: str
    title: str
    category: str
    description: str
    duration: str
    steps: List[str]
    tags: List[str]

class GameSchema(BaseModel):
    id: str
    title: str
    category: str
    description: str
    type: str
    difficulty: str
    tags: List[str]

class RecommendationData(BaseModel):
    exercises: List[ExerciseSchema]
    games: List[GameSchema]

class ChatResponse(BaseModel):
    response: str = Field(..., description="Naina's natural language response")
    session_id: str = Field(..., description="The active session ID")
    recommendations: Optional[RecommendationData] = Field(None, description="Contextual game and exercise recommendations")

class RecommendRequest(BaseModel):
    symptoms: List[str] = Field(..., description="List of symptoms, issues, or tags")
    limit: Optional[int] = Field(3, description="Maximum number of recommendations to return")

class RecommendResponse(BaseModel):
    exercises: List[ExerciseSchema]
    games: List[GameSchema]

class HealthResponse(BaseModel):
    status: str
