"""Feature API endpoints"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query

from app.core.config import get_db
from app.core.exceptions import ApiError
from app.schemas.feature import Feature, FeatureCreate, FeatureUpdate

router = APIRouter(prefix="/feature", tags=["features"])

@router.post("", response_model=Feature, status_code=201)
def create_feature(feature: FeatureCreate, user_id: int = 1):
    """Создать новую фичу"""
    db = get_db()
    new_id = max([w["id"] for w in db["features"]], default=0) + 1
    now = datetime.now()

    feature_data = {
        "id": new_id,
        "user_id": user_id,
        "title": feature.title,
        "link": feature.link,
        "price_estimate": feature.price_estimate,
        "votes": feature.votes or 0,
        "created_at": now,
        "updated_at": now,
    }

    db["features"].append(feature_data)
    return feature_data


@router.get("", response_model=List[Feature])
def get_features(
        price_lt: Optional[float] = Query(None, description="Фильтр по максимальной цене")
):
    """Получить все фичи с опциональной фильтрацией по цене"""
    db = get_db()
    features = db["features"]

    if price_lt is not None:
        features = [
            f
            for f in features
            if f["price_estimate"] is not None and f["price_estimate"] < price_lt
        ]

    return features


@router.get("/{feature_id}", response_model=Feature)
def get_feature(feature_id: int):
    """Получить фичу по ID"""
    db = get_db()
    for feature in db["features"]:
        if feature["id"] == feature_id:
            return feature

    from app.core.exceptions import ApiError
    raise ApiError(
        code="not_found",
        message="Feature not found",
        status=404
    )


@router.put("/{feature_id}", response_model=Feature)
def update_feature(feature_id: int, feature_update: FeatureUpdate):
    """Обновить фичу"""
    db = get_db()
    for i, feature in enumerate(db["features"]):
        if feature["id"] == feature_id:
            update_data = feature_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                feature[field] = value
            feature["updated_at"] = datetime.now()
            db["features"][i] = feature
            return feature

    raise ApiError(
        code="not_found",
        message="Feature not found",
        status=404
    )


@router.delete("/{feature_id}")
def delete_feature(feature_id: int):
    """Удалить фичу"""
    db = get_db()
    for i, feature in enumerate(db["features"]):
        if feature["id"] == feature_id:
            del db["features"][i]
            return {"message": "feature deleted successfully"}

    raise ApiError(
        code="not_found",
        message="Feature not found",
        status=404
    )