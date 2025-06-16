# user_query.py

from pydantic import BaseModel, Field
from typing import Optional


class UserQuery(BaseModel):
    location: str = Field(..., example="Berlin, Germany")
    timestamp: Optional[str] = None  # Make timestamp optional
    days_ago: Optional[int] = Field(0, ge=0, le=30, example=2)

    class Config:
        schema_extra = {
            "example": {
                "location": "New York, USA",
                "days_ago": 1
            }
        }
