"""Feature schemas"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class FeatureBase(BaseModel):
    """Base wish model with common fields"""

    title: str = Field(..., min_length=1, max_length=200)
    link: Optional[str] = Field(None, max_length=500)
    price_estimate: Optional[float] = Field(None, ge=0)
    votes: int = Field(None, ge=0)

class FeatureCreate(FeatureBase):
    """Schema for creating a new wish"""

    pass

class FeatureUpdate(BaseModel):
    """Schema for updating a wish (all fields optional)"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    link: Optional[str] = Field(None, max_length=500)
    price_estimate: Optional[float] = Field(None, ge=0)
    votes: int = Field(None, ge=0)

class Feature(FeatureBase):
    """Complete wish model with all fields"""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

