from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from recommender import CourseRecommender

import time
import psutil
import pandas as pd
import numpy as np

from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    Gauge
)

from fastapi import Response

# -----------------------------------------
# FastAPI App
# -----------------------------------------

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

# -----------------------------------------
# Prometheus Metrics
# -----------------------------------------

REQUEST_COUNT = Counter(
    "recommendation_requests_total",
    "Total recommendation requests"
)

FAILED_REQUEST_COUNT = Counter(
    "recommendation_failed_requests_total",
    "Total failed recommendation requests"
)

REQUEST_LATENCY = Histogram(
    "recommendation_latency_seconds",
    "Recommendation API latency"
)

ACTIVE_REQUESTS = Gauge(
    "recommendation_active_requests",
    "Currently active recommendation requests"
)

TOTAL_RECOMMENDATIONS = Counter(
    "recommendations_returned_total",
    "Total recommendations returned"
)

CPU_USAGE = Gauge(
    "system_cpu_usage_percent",
    "System CPU usage percentage"
)

MEMORY_USAGE = Gauge(
    "system_memory_usage_percent",
    "System memory usage percentage"
)

PRECISION_AT_K = Gauge(
    "precision_at_k",
    "Precision at K"
)

RECALL_AT_K = Gauge(
    "recall_at_k",
    "Recall at K"
)

MAP_AT_K = Gauge(
    "map_at_k",
    "Mean Average Precision"
)

MRR_SCORE = Gauge(
    "mrr_score",
    "Mean Reciprocal Rank"
)

# -----------------------------------------
# Request Model
# -----------------------------------------

class RecommendationRequest(BaseModel):

    query: str

    difficulty: Optional[str] = None

    top_n: int = 5

# -----------------------------------------
# Health Endpoint
# -----------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

# -----------------------------------------
# Evaluation Helper Functions
# -----------------------------------------

def get_relevant_items(query, df):

    query_words = query.lower().split()

    relevant = []

    for _, row in df.iterrows():

        title = str(row['course_title']).lower()

        if any(word in title for word in query_words):

            relevant.append(row['course_title'])

    return set(relevant)


def precision_at_k(recommended, relevant, k):

    recommended_k = recommended[:k]

    relevant_found = len(
        set(recommended_k) & relevant
    )

    return relevant_found / k


def recall_at_k(recommended, relevant, k):

    recommended_k = recommended[:k]

    relevant_found = len(
        set(recommended_k) & relevant
    )

    if len(relevant) == 0:
        return 0

    return relevant_found / len(relevant)


def average_precision(recommended, relevant, k):

    score = 0

    hits = 0

    for i, item in enumerate(recommended[:k]):

        if item in relevant:

            hits += 1

            score += hits / (i + 1)

    if hits == 0:
        return 0

    return score / hits


def reciprocal_rank(recommended, relevant):

    for i, item in enumerate(recommended):

        if item in relevant:

            return 1 / (i + 1)

    return 0

# -----------------------------------------
# Recommendation Endpoint
# -----------------------------------------

@app.post("/recommend")
def recommend_courses(request: RecommendationRequest):

    ACTIVE_REQUESTS.inc()

    start_time = time.time()

    try:

        REQUEST_COUNT.inc()

        results = recommender.recommend_courses(
            query=request.query,
            difficulty=request.difficulty,
            top_n=request.top_n
        )

        TOTAL_RECOMMENDATIONS.inc(len(results))

        latency = time.time() - start_time

        REQUEST_LATENCY.observe(latency)

        # -----------------------------------------
        # System Metrics
        # -----------------------------------------

        CPU_USAGE.set(psutil.cpu_percent())

        MEMORY_USAGE.set(psutil.virtual_memory().percent)

        # -----------------------------------------
        # Recommendation Quality Metrics
        # -----------------------------------------

        recommended_titles = list(
            results['course_title']
        )

        relevant_items = get_relevant_items(
            request.query,
            recommender.df
        )

        k = request.top_n

        precision = precision_at_k(
            recommended_titles,
            relevant_items,
            k
        )

        recall = recall_at_k(
            recommended_titles,
            relevant_items,
            k
        )

        ap = average_precision(
            recommended_titles,
            relevant_items,
            k
        )

        rr = reciprocal_rank(
            recommended_titles,
            relevant_items
        )

        PRECISION_AT_K.set(precision)

        RECALL_AT_K.set(recall)

        MAP_AT_K.set(ap)

        MRR_SCORE.set(rr)

        return results.to_dict(orient="records")

    except Exception as e:

        FAILED_REQUEST_COUNT.inc()

        return {
            "error": str(e)
        }

    finally:

        ACTIVE_REQUESTS.dec()

# -----------------------------------------
# Metrics Endpoint
# -----------------------------------------

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
