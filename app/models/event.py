# event.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Event(BaseModel):
    title: str
    summary: str
    source: str
    url: str
    published_at: datetime
    location: str
    sentiment: str
    emotions: List[str]  # e.g., ["joy", "fear"]
    embedding: List[float]  # 768-dimensional or similar
    timestamp: Optional[datetime]


    class Config:
        schema_extra = {
            "example": {
                "title": "Protests erupt in downtown Nairobi",
                "summary": "Mass protests broke out in Nairobi against the new fuel tax policy.",
                "source": "BBC",
                "url": "https://www.bbc.com/news/world-africa-xyz",
                "published_at": "2025-06-10T14:23:00",
                "location": "Nairobi, Kenya",
                "sentiment": "anger",
                "emotions": ["anger", "fear"],
                "embedding": [0.123, 0.456, ...]  # Example placeholder
            }
        }
