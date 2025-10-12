from datetime import datetime

from pydantic import BaseModel


class FeatureBase(BaseModel):
    title: str
    description: str


class FeatureCreate(FeatureBase):
    pass


class FeatureResponse(FeatureBase):
    id: int
    votes_count: int
    created_at: datetime

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    user_id: int
    value: int


class VoteResponse(BaseModel):
    id: int
    user_id: int
    feature_id: int
    value: int
    created_at: datetime

    class Config:
        orm_mode = True
