"""
dataset_ingest.py

Reads local dataset, summarizes, classifies emotion, generates embeddings,
and stores them in MongoDB with optional metadata.
"""

import json
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
import os

from app.services.summarizer import summarize_text
from app.services.sentiment import classify_emotion
from app.services.embeddings import get_embedding
from app.db.mongo_client import get_collection

load_dotenv()

# Dataset location
DATA_PATH = Path("public_dataset/news_category.json")

# Load collection
collection = get_collection()

def clean_text(text):
    return text.strip().replace("\n", " ").replace("  ", " ")

def ingest_dataset(limit=500):
    print(f"[+] Loading dataset from {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f.readlines()]

    print(f"[+] Found {len(records)} records. Ingesting up to {limit} entries...")

    for record in tqdm(records[:limit]):
        try:
            title = clean_text(record.get("headline", ""))
            desc = clean_text(record.get("short_description", ""))
            text = f"{title}. {desc}"

            # 1. Summarize
            summary = summarize_text(text)

            # 2. Sentiment
            sentiment = classify_emotion(summary)

            # 3. Embedding
            embedding = get_embedding(summary)

            # 4. Mongo document
            doc = {
                "raw_title": title,
                "raw_description": desc,
                "summary": summary,
                "sentiment": sentiment,
                "category": record.get("category", ""),
                "link": record.get("link", ""),
                "authors": record.get("authors", ""),
                "date": record.get("date", ""),
                "embedding": embedding,
                "source": "RMisra Kaggle"
            }

            collection.insert_one(doc)

        except Exception as e:
            print(f"[!] Error processing record: {e}")
            continue

    print("[✓] Dataset ingestion complete.")


if __name__ == "__main__":
    ingest_dataset(limit=500)  # Adjust the limit based on MongoDB storage
