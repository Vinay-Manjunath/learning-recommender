from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from recommender import CourseRecommender
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response


app = FastAPI(
    title="Course Recommendation API",
    version="1.0.0"
)

# -----------------------------------------
# Enable CORS
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Starting recommendation engine...")

recommender = CourseRecommender()

print("Recommendation engine ready")

class RecommendationRequest(BaseModel):

    query: str

    difficulty: Optional[str] = None

    top_n: int = 5

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

@app.post("/recommend")
def recommend_courses(request: RecommendationRequest):

    results = recommender.recommend_courses(
        query=request.query,
        difficulty=request.difficulty,
        top_n=request.top_n
    )

    return results.to_dict(orient="records")
    

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )