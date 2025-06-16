from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.user_query import UserQuery
from app.services.google_search import fetch_news
from app.services.summarizer import summarize
from app.services.sentiment import classify
from app.services.embeddings import get_embedding
from app.services.mongo_vector import insert_news_vector, vector_search_by_location
from app.template.response_formatter import format_response

router = APIRouter()

@router.post("/query")
async def handle_query(user_query: UserQuery):
    try:
        timestamp = user_query.timestamp or datetime.utcnow().isoformat()

        # 1. Pull live news using query
        articles = fetch_news(user_query.location)
        if not articles:
            raise HTTPException(status_code=404, detail="No news found for this location.")

        results = []
        summary_vectors = []

        for article in articles:
            title = article.get("title", "")
            description = article.get("snippet", "")
            combined_text = f"{title}. {description}"

            # 2. Summarize
            summary = summarize(combined_text)

            # 3. Classify emotion
            sentiment_result = classify(summary)
            sentiment = sentiment_result["emotion"]  # Only store the emotion string

            # 4. Generate vector embedding
            embedding = get_embedding(summary)

            # 5. Construct document and insert into MongoDB
            doc = {
                "location": user_query.location,
                "raw_title": title,
                "raw_description": description,
                "summary": summary,
                "sentiment": sentiment,
                "embedding": embedding,
                "source_url": article.get("link", ""),
                "timestamp": timestamp, 
            }
            insert_news_vector(doc)

            # Store result for response + save embedding for similarity search
            results.append(doc)
            summary_vectors.append(embedding)

        # 6. Perform similarity search on one of the vectors (e.g., first)
        similar_past = []
        if summary_vectors:
            similar_past = vector_search_by_location(
                summary_vectors[0],
                user_query.location,
                k=5
            )

        # 7. Format response including similar past events
        return format_response(results, user_query.location, similar_past)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
