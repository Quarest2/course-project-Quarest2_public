from pydantic import BaseModel, Field
from typing import Optional

class Feature(BaseModel):
    id: int = Field(..., gt=0, description="ID фичи")
    name: str = Field(..., min_length=1, max_length=100, description="Название фичи")
    votes: int = Field(0, ge=0, description="Количество голосов")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Dark Mode",
                "votes": 5
            }
        }

class VoteRequest(BaseModel):
    feature_id: int = Field(..., gt=0, description="ID фичи для голосования")
    user_id: Optional[str] = Field(None, description="ID пользователя")

    class Config:
        schema_extra = {
            "example": {
                "feature_id": 1,
                "user_id": "user123"
            }
        }

class HealthResponse(BaseModel):
    status: str
    service: str
    correlation_id: str
    timestamp: str