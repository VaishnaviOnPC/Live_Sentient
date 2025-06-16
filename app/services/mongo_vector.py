"""
mongo_vector.py

Handles storing and querying vectorized news data in MongoDB Atlas using Vector Search.
"""

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from app.db.mongo_client import atlas_client, COLLECTION_NAME


load_dotenv()

collection = atlas_client.get_collection(COLLECTION_NAME)

def insert_news_vector(doc: Dict[str, Any]) -> bool:
    """
    Inserts a single vectorized news summary with emotion label into MongoDB.
    
    Expected doc:
    {
        "location": "Delhi",
        "summary": "Floods disrupt transportation in several districts.",
        "emotion": "fear",
        "embedding": [...],  # 384/768 dim vector
        "timestamp": "2025-06-11T14:22:00Z",
        "sources": [
            {"title": "Flood hits Delhi", "link": "https://...", "source": "BBC"}
        ]
    }
    """
    try:
        doc["_id"] = f"{doc['location']}_{doc['timestamp']}"  # deduplication ID
        collection.insert_one(doc)
        return True
    except DuplicateKeyError:
        return False


def vector_search_by_location(embedding, location, k=5):
    """
    Perform vector similarity search restricted to a location.

    Args:
        embedding (List[float]): Query vector
        location (str): Location string (e.g., "Paris")
        k (int): Number of results

    Returns:
        List[Dict]: Similar events from same place
    """
    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": k,
                "index": "vector_index"
            }
        },
        {
            "$match": {
                "location": {"$regex": location, "$options": "i"}
            }
        },
        {
            "$sort": {"timestamp": -1}
        },
        {
            "$project": {
                "_id": 0,
                "summary": 1,
                "sentiment": 1,
                "timestamp": 1,
                "raw_title": 1,
                "source_url": 1
            }
        }
    ]
    return list(collection.aggregate(pipeline))
