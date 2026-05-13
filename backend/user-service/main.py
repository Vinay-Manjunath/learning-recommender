from fastapi import FastAPI
from pydantic import BaseModel
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI(
    title="User Service",
    version="1.0.0"
)

# -----------------------------------------
# User Model
# -----------------------------------------

class User(BaseModel):

    username: str

    email: str

    password: str

# -----------------------------------------
# Temporary In-Memory Storage
# -----------------------------------------

users = []

# -----------------------------------------
# Health Endpoint
# -----------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "User Service Healthy"
    }

# -----------------------------------------
# Register User
# -----------------------------------------

@app.post("/register")
def register_user(user: User):

    users.append(user.dict())

    return {
        "message": "User registered successfully",
        "user": user
    }

# -----------------------------------------
# Get All Users
# -----------------------------------------

@app.get("/users")
def get_users():

    return users

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )