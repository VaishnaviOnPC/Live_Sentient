# response_formatter.py

from typing import List, Dict
from datetime import datetime
from collections import Counter


def format_response(articles: List[Dict], location: str, similar_past=None) -> Dict:
    """
    Formats the list of enriched news articles into a structured API response.

    Args:
        articles (List[Dict]): List of news entries after summarization and sentiment analysis.
        location (str): The location passed by the user.

    Returns:
        Dict: Clean, structured output with metadata and article breakdown.
    """

    sentiment_counter = Counter([a.get("sentiment", "neutral") for a in articles])
    total = sum(sentiment_counter.values())

    if total > 0:
        top_sentiment, count = sentiment_counter.most_common(1)[0]
        mood_summary = f"The prevailing mood in {location} is '{top_sentiment}' ({round((count / total) * 100, 1)}% of articles)."
    else:
        top_sentiment = "neutral"
        mood_summary = f"No strong emotional signals detected in recent news for {location}."

    formatted_articles = []
    for a in articles:
        formatted_articles.append({
            "title": a.get("raw_title", "No title"),
            "summary": a.get("summary", "No summary available."),
            "sentiment": a.get("sentiment", "neutral"),
            "source": a.get("source_url", "#")
        })

    return {
        "location": location.title(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dominant_mood": top_sentiment,
        "summary_insight": mood_summary,
        "total_articles": total,
        "articles": formatted_articles,
        "similar_past": similar_past or []
    }
