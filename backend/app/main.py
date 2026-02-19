from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import auth, questions, predictions, leaderboard

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SignalRanking API",
    description="Skill-based forecasting platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(predictions.router)
app.include_router(leaderboard.router)

@app.get("/")
def root():
    return {"message": "SignalRanking API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
