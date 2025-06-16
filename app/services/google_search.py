"""
Google Search Service (via Serper.dev)

Fetches latest news headlines and links for a given location-based query.
"""

import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search/news"

if not SERPER_API_KEY:
    print("[Warning] SERPER_API_KEY is not set!")

def fetch_news(query: str, num_results: int = 5) -> List[Dict]:
    """
    Fetch latest news articles related to the user's query using Serper.dev.
    
    Args:
        query (str): Location or topic (e.g., "news in New York")
        num_results (int): Number of results to return (max 10 for free tier)

    Returns:
        List[Dict]: Articles with title, link, snippet, published date
    """
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": num_results
    }

    try:
        response = requests.post(SERPER_API_URL, headers=headers, json=payload)
        print(f"Status: {response.status_code}, Response: {response.text}")  # Add this line
        response.raise_for_status()
        data = response.json()
        news_items = data.get("news") or data.get("topStories", [])

        return [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet") or "",
                "published_date": item.get("date"),
                "source": item.get("source")
            }
            for item in news_items
        ]

    except requests.RequestException as e:
        print(f"[Serper API Error] {e}")
        return [0]
