"""
Summarizer Service

Summarizes text using either:
1. OpenAI GPT (if OPENAI_API_KEY is present)
2. HuggingFace transformers pipeline as fallback
"""

from __future__ import annotations
import os
from typing import List, Union
from functools import lru_cache

from transformers import pipeline, Pipeline
import vertexai
from rouge import Rouge
from vertexai.generative_models import GenerationConfig, GenerativeModel
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------ #
# Config
# ------------------------------------------------------------------------ #

USE_GEMINI = bool(os.getenv("GCP_PROJECT_ID"))

vertexai.init(project=os.getenv("GCP_PROJECT_ID"), location="us-central1")

generation_model = GenerativeModel("gemini-2.0-flash")

generation_config = GenerationConfig(temperature=0.1, max_output_tokens=256)

print("USE_GEMINI:", bool(os.getenv("GCP_PROJECT_ID")))

# ------------------------------------------------------------------------ #
# Core API
# ------------------------------------------------------------------------ #

def summarize(text: str) -> str:
    """
    Summarize a single news article or paragraph.

    Uses Gemini if enabled, otherwise falls back to local model.
    """
    text = text.strip()
    if not text:
        print("Empty text received for summarization.")
        return ""

    if USE_GEMINI:
        print("Using Gemini summarizer")
        try:
            return _gemini_summary(text)
        except Exception as e:
            print(f"Gemini summarization failed: {e}")
            # Optional: fallback to local summarizer if Gemini fails
            print("Falling back to local Hugging Face summarizer")
            return _local_summarizer().__call__(text, truncation=True, max_length=128)[0]["summary_text"]
    else:
        print("Using local Hugging Face summarizer")
        return _local_summarizer().__call__(text, truncation=True, max_length=128)[0]["summary_text"]

def summarize_batch(texts: List[str]) -> List[str]:
    """
    Summarize a batch of texts (used for dataset ingestion).
    """
    if not texts:
        print("Empty batch received for summarization.")
        return []

    if USE_GEMINI:
        print("Using Gemini summarizer for batch")
        summaries = []
        for t in texts:
            try:
                summaries.append(_gemini_summary(t))
            except Exception as e:
                print(f"Gemini summarization failed for batch item: {e}")
                # Optional: fallback to local summarizer for this item
                summaries.append(_local_summarizer().__call__(t, truncation=True, max_length=128)[0]["summary_text"])
        return summaries
    else:
        print("Using local Hugging Face summarizer for batch")
        summarizer = _local_summarizer()
        return [r["summary_text"] for r in summarizer(texts, truncation=True, max_length=128)]

# ------------------------------------------------------------------------ #
# Local Model (HuggingFace)
# ------------------------------------------------------------------------ #

@lru_cache(maxsize=1)
def _local_summarizer() -> Pipeline:
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


# ------------------------------------------------------------------------ #
# OpenAI Summarizer
# ------------------------------------------------------------------------ #

def _gemini_summary(text: str) -> str:
    prompt = (
        "Summarize the following news story in one short paragraph. "
        "Preserve all key facts and emotional tone.\n\n"
        f"Article:\n{text}\n\nSummary:"
    )

    try:
        response = generation_model.generate_content(
            contents=prompt,
            generation_config=generation_config
        )
        # For Vertex AI, response.text is usually the summary
        summary = getattr(response, "text", None)
        if not summary or not summary.strip():
            return "[No summary generated]"
        return summary.strip()
    except Exception as e:
        return f"[Summarization failed: {e}]"