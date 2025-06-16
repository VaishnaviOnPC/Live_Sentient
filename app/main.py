# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import query
from app.db.schema_setup import create_indexes

app = FastAPI(
    title="LiveSentient AI Agent",
    description="Get real-time emotional insights on any place in the world using AI + MongoDB + Google News.",
    version="1.0.0"
)

# CORS — allow frontend to make API calls (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all app routes
app.include_router(query.router, prefix="")

# Optional: Set up indexes on startup
@app.on_event("startup")
async def startup_event():
    print("[🔧] Running MongoDB index setup...")
    create_indexes()
    print("[✅] LiveSentient backend is ready.")


@app.get("/")
def root():
    return {"message": "Welcome to LiveSentient! Use POST /query to begin."}
