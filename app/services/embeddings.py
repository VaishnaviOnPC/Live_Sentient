import os
from typing import List
from functools import lru_cache

from dotenv import load_dotenv
load_dotenv()

USE_GEMINI = bool(os.getenv("GCP_PROJECT_ID"))
# ------------------------------------------------------------------------ #
if USE_GEMINI:
    import vertexai
    from vertexai.preview.language_models import TextEmbeddingModel
    vertexai.init(project=os.getenv("GCP_PROJECT_ID"), location="us-central1")
    embedding_model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")
    

else:
    from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------------------ #
# Embedding Generator
# ------------------------------------------------------------------------ #

def get_embedding(text: str) -> List[float]:
    """
    Get a single embedding vector from the given text.
    """
    text = text.strip().replace("\n", " ")
    if not text:
        return []

    if USE_GEMINI:
        return _gemini_embed(text)
    else:
        return _local_model().encode(text).tolist()


def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    cleaned = [t.strip().replace("\n", " ") for t in texts]
    if USE_GEMINI:
        try:
            response = embedding_model.get_embeddings(cleaned)
            return [r.values for r in response]
        except Exception as e:
            print(f"[Gemini Batch Embedding failed]: {e}")
            return [[] for _ in cleaned]
    else:
        return _local_model().encode(cleaned).tolist()


# ------------------------------------------------------------------------ #
# Gemini Embedding (embedding-001)
# ------------------------------------------------------------------------ #

def _gemini_embed(text: str) -> List[float]:
    """
    Get a single embedding from Gemini's embedding-001 model.
    """
    try:
        response = embedding_model.get_embeddings(
            [text]             # Input parameter is 'content'
        )
        # Access the embedding values directly from the response
        return response[0].values
    except Exception as e:
        print(f"[Gemini Embedding failed]: {e}")
        return []


# ------------------------------------------------------------------------ #
# Local Sentence Transformer
# ------------------------------------------------------------------------ #

@lru_cache(maxsize=1)
def _local_model():
    """
    Loads and caches the Sentence Transformer model.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")