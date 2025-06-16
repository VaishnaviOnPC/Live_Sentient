import re
import string
import unicodedata
from typing import List, Optional

try:
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    import nltk
    nltk.download("stopwords")
    STOPWORDS = set(nltk.corpus.stopwords.words("english"))


def clean_text(
    text: str,
    remove_stopwords: bool = False,
    strip_non_ascii: bool = True
) -> str:
    """
    Clean and normalize input text.

    Steps:
    - Lowercase
    - Remove URLs
    - Remove punctuation
    - Remove emojis and non-ASCII (optional)
    - Remove stopwords (optional)
    - Collapse whitespace

    Args:
        text (str): Raw input text
        remove_stopwords (bool): Whether to remove English stopwords
        strip_non_ascii (bool): Whether to remove emojis/non-ASCII

    Returns:
        str: Cleaned and normalized text
    """

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation

    if strip_non_ascii:
        text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()

    words = text.split()

    if remove_stopwords:
        words = [word for word in words if word not in STOPWORDS]

    text = " ".join(words)
    text = re.sub(r"\s+", " ", text).strip()

    return text
