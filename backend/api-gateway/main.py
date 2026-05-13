from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

app = FastAPI(
    title="API Gateway",
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

# -----------------------------------------
# Service URLs
# -----------------------------------------

RECOMMENDATION_SERVICE = os.getenv(
    "RECOMMENDATION_SERVICE"
)

USER_SERVICE = os.getenv(
    "USER_SERVICE"
)

FEEDBACK_SERVICE = os.getenv(
    "FEEDBACK_SERVICE"
)

# -----------------------------------------
# Health Endpoint
# -----------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "API Gateway Healthy"
    }

# -----------------------------------------
# Recommendation Service Routes
# -----------------------------------------

@app.get("/recommendation/health")
async def recommendation_health():

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{RECOMMENDATION_SERVICE}/health"
        )

    return response.json()

# -----------------------------------------
# Recommendation API Route
# -----------------------------------------

@app.post("/recommend")
async def recommend_courses(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(

            f"{RECOMMENDATION_SERVICE}/recommend",

            json=body

        )

    return response.json()

# -----------------------------------------
# User Service Routes
# -----------------------------------------

@app.get("/users")
async def get_users():

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{USER_SERVICE}/users"
        )

    return response.json()

# -----------------------------------------
# Feedback Service Routes
# -----------------------------------------

@app.get("/feedback")
async def get_feedback():

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{FEEDBACK_SERVICE}/feedback"
        )

    return response.json()

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )