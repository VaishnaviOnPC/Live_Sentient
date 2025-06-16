# schema_setup.py
from app.db.mongo_client import atlas_client, COLLECTION_NAME
db =  atlas_client.database

def create_indexes():
    collection = atlas_client.get_collection(COLLECTION_NAME)

    print(f"[+] Creating indexes on `{COLLECTION_NAME}`...")

    # Fallback text index for summary (if not using full Atlas Vector Search yet)
    #collection.create_index(
    #    [("embedding", "text")],
    #    name="embedding_text_fallback"
    #)

    # Text index for search capabilities (useful for fallback and hybrid search)
    collection.create_index(
        [("summary", "text"), ("raw_title", "text"), ("raw_description", "text")],
        name="text_search_index"
    )

    # Index on location for efficient vectorSearch + location match
    collection.create_index(
        [("location", 1)],
        name="location_index"
    )

    # Optional: index on timestamp if you want timeline visualizations
    collection.create_index(
        [("timestamp", -1)],
        name="timestamp_desc_index"
    )

    print("[✓] Indexes created successfully.")

if __name__ == "__main__":
    create_indexes()
