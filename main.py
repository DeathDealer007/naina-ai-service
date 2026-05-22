import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environmental variables from .env
load_dotenv()

from routes import chat, recommend, health

app = FastAPI(
    title="Naina AI Service", 
    description="Conversational Eye Wellness Assistant Service",
    version="1.0.0"
)

# Configure CORS for local development services
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoint routes
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(recommend.router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"Starting Naina AI Service on port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
