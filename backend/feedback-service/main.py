from fastapi import FastAPI
from pydantic import BaseModel
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI(
    title="Feedback Service",
    version="1.0.0"
)

# -----------------------------------------
# Feedback Model
# -----------------------------------------

class Feedback(BaseModel):

    username: str

    course_title: str

    rating: int

    comment: str

# -----------------------------------------
# Temporary Feedback Storage
# -----------------------------------------

feedback_list = []

# -----------------------------------------
# Health Endpoint
# -----------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "Feedback Service Healthy"
    }

# -----------------------------------------
# Submit Feedback
# -----------------------------------------

@app.post("/feedback")
def submit_feedback(feedback: Feedback):

    feedback_list.append(feedback.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback
    }

# -----------------------------------------
# Get All Feedback
# -----------------------------------------

@app.get("/feedback")
def get_feedback():

    return feedback_list

# -----------------------------------------
# Get Feedback By Course
# -----------------------------------------

@app.get("/feedback/{course_title}")
def get_course_feedback(course_title: str):

    results = []

    for feedback in feedback_list:

        if feedback["course_title"].lower() == course_title.lower():

            results.append(feedback)

    return results

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )