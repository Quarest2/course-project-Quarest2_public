from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.monitoring import logger, track_performance
from app.schemas.feature import Feature, VoteRequest

router = APIRouter()

# Временное хранилище данных
votes_data = {
    "features": [
        {"id": 1, "name": "Dark Mode", "votes": 0},
        {"id": 2, "name": "Mobile App", "votes": 0},
        {"id": 3, "name": "API Access", "votes": 0}
    ]
}


@router.get("/features", response_model=List[Feature])
async def get_features(
        skip: int = Query(0, ge=0, description="Пропустить первые N записей"),
        limit: int = Query(100, ge=1, le=1000, description="Лимит записей")
):
    """Получить список фич для голосования"""
    with track_performance("get_features") as correlation_id:
        features = votes_data["features"][skip:skip + limit]
        logger.info("Fetching features list",
                    correlation_id=correlation_id,
                    feature_count=len(features),
                    skip=skip,
                    limit=limit)
        return features


@router.get("/features/{feature_id}", response_model=Feature)
async def get_feature(feature_id: int):
    """Получить конкретную фичу по ID"""
    with track_performance("get_feature") as correlation_id:
        logger.info("Fetching specific feature",
                    correlation_id=correlation_id,
                    feature_id=feature_id)

        feature = next((f for f in votes_data["features"] if f["id"] == feature_id), None)
        if not feature:
            logger.warning("Feature not found",
                           correlation_id=correlation_id,
                           feature_id=feature_id)
            raise HTTPException(status_code=404, detail="Feature not found")

        return feature


@router.post("/votes")
async def cast_vote(vote: VoteRequest):
    """Проголосовать за фичу"""
    with track_performance("cast_vote") as correlation_id:
        logger.info("Casting vote",
                    correlation_id=correlation_id,
                    feature_id=vote.feature_id,
                    user_id=vote.user_id)

        # Поиск фичи
        feature = next((f for f in votes_data["features"] if f["id"] == vote.feature_id), None)
        if not feature:
            logger.warning("Feature not found",
                           correlation_id=correlation_id,
                           feature_id=vote.feature_id)
            raise HTTPException(status_code=404, detail="Feature not found")

        # Голосование
        feature["votes"] += 1
        logger.info("Vote cast successfully",
                    correlation_id=correlation_id,
                    feature_id=vote.feature_id,
                    new_vote_count=feature["votes"],
                    user_id=vote.user_id)

        return {
            "message": "Vote cast successfully",
            "feature_id": vote.feature_id,
            "votes": feature["votes"],
            "correlation_id": correlation_id
        }


@router.get("/votes")
async def get_votes():
    """Получить результаты голосования"""
    with track_performance("get_votes") as correlation_id:
        total_votes = sum(f["votes"] for f in votes_data["features"])
        logger.info("Fetching vote results",
                    correlation_id=correlation_id,
                    total_votes=total_votes,
                    feature_count=len(votes_data["features"]))
        return {
            "results": votes_data["features"],
            "total_votes": total_votes,
            "correlation_id": correlation_id
        }