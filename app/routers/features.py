from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from app.models.feature import features_db, next_feature_id, next_vote_id, votes_db

router = APIRouter()


@router.get("/features", response_model=List[dict])
def get_features(skip: int = 0, limit: int = 100):
    """GET /features - список всех фич"""
    return features_db[skip : skip + limit]


@router.get("/features/top", response_model=List[dict])
def get_top_features(limit: int = 10):
    """GET /features/top - топ фич по голосам"""
    sorted_features = sorted(
        features_db, key=lambda x: x.get("votes_count", 0), reverse=True
    )
    return sorted_features[:limit]


@router.get("/features/{feature_id}", response_model=dict)
def get_feature(feature_id: int):
    """GET /features/{id} - детали фичи"""
    for feature in features_db:
        if feature.get("id") == feature_id:
            return feature
    raise HTTPException(status_code=404, detail="Feature not found")


@router.post("/features", response_model=dict)
def create_feature(feature_data: dict):
    """POST /features - создать новую фичу"""
    global next_feature_id

    new_feature = {
        "id": next_feature_id,
        "title": feature_data.get("title", ""),
        "description": feature_data.get("description", ""),
        "votes_count": 0,
        "created_at": datetime.utcnow().isoformat(),
    }
    features_db.append(new_feature)
    next_feature_id += 1
    return new_feature


@router.post("/features/{feature_id}/vote", response_model=dict)
def vote_for_feature(feature_id: int, vote_data: dict):
    """POST /features/{id}/vote - проголосовать за фичу"""
    global next_vote_id

    feature = None
    for f in features_db:
        if f.get("id") == feature_id:
            feature = f
            break

    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    user_id = vote_data.get("user_id")
    for vote in votes_db:
        if vote.get("user_id") == user_id and vote.get("feature_id") == feature_id:
            raise HTTPException(
                status_code=400, detail="User already voted for this feature"
            )

    new_vote = {
        "id": next_vote_id,
        "user_id": user_id,
        "feature_id": feature_id,
        "value": vote_data.get("value", 1),
        "created_at": datetime.utcnow().isoformat(),
    }
    votes_db.append(new_vote)
    next_vote_id += 1

    feature["votes_count"] = feature.get("votes_count", 0) + new_vote["value"]

    return new_vote
