# app/services/sentiment.py
"""
Emotion classifier service using Hugging Face model:
https://huggingface.co/boltuix/bert-emotion
"""

from __future__ import annotations
from typing import List, Dict, Any
from functools import lru_cache

import torch
import torch.nn.functional as F
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    PreTrainedTokenizerBase,
    PreTrainedModel,
)

MODEL_NAME = "boltuix/bert-emotion"


# --------------------------------------------------------------------------- #
# Lazy singletons – load once, reuse everywhere                               #
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=1)
def _get_tokenizer() -> PreTrainedTokenizerBase:
    return AutoTokenizer.from_pretrained(MODEL_NAME)


@lru_cache(maxsize=1)
def _get_model() -> PreTrainedModel:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()  # inference mode
    return model


# --------------------------------------------------------------------------- #
# Public API                                                                  #
# --------------------------------------------------------------------------- #
def classify(text: str) -> Dict[str, Any]:
    """
    Classify a single text into one of six emotions:
    { anger, disgust, fear, joy, sadness, surprise }

    Returns
    -------
    dict  e.g.
        {
          "emotion": "anger",
          "confidence": 0.842,
          "scores": { "anger": 0.842, "joy": 0.02, ... }
        }
    """
    if not text.strip():
        return _empty_response()

    tokenizer = _get_tokenizer()
    model = _get_model()

    with torch.no_grad():
        inputs = tokenizer(text, truncation=True, return_tensors="pt")
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=-1)[0]

    return _probs_to_response(probs)


def classify_batch(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Classify a batch of texts (better GPU/CPU utilisation).

    `texts` length can be anything; empty / blank strings will return neutral.
    """
    tokenizer = _get_tokenizer()
    model = _get_model()

    cleaned = [t if t.strip() else " " for t in texts]  # keep positional order
    with torch.no_grad():
        inputs = tokenizer(
            cleaned,
            truncation=True,
            padding=True,
            return_tensors="pt",
        )
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=-1)

    return [_probs_to_response(p) for p in probs]


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
_id2label = _get_model().config.id2label  # cache once


def _probs_to_response(probs: torch.Tensor) -> Dict[str, Any]:
    top_idx = int(torch.argmax(probs))
    scores = { _id2label[i]: float(round(probs[i].item(), 4)) for i in range(len(probs)) }

    return {
        "emotion": _id2label[top_idx],
        "confidence": scores[_id2label[top_idx]],
        "scores": scores,
    }


def _empty_response() -> Dict[str, Any]:
    return {
        "emotion": "neutral",
        "confidence": 1.0,
        "scores": {lbl: (1.0 if lbl == "neutral" else 0.0) for lbl in _id2label.values()},
    }
