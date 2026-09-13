"""
week03/embedder.py — turning text into vectors.

An embedding model is not an LLM. It does not generate text; it places meaning
in a coordinate system so that similar things end up close together.

You will reuse this module in Week 6 as the retrieval half of a RAG pipeline.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# BGE-M3 is multilingual and good at Turkish, but downloads ~2.2 GB.
# If your machine cannot take it, switch to the lighter model below and say so
# in model_notes.md.
MODEL_NAME = "BAAI/bge-m3"
# MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"   # ~470 MB fallback

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Load the model once and keep it — loading is slow, encoding is not."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def encode(texts: list[str]) -> np.ndarray:
    """Return one normalised vector per input text, shape (len(texts), dim)."""
    # TODO: call _get_model().encode(texts, normalize_embeddings=True)
    # Normalising matters: it makes the dot product equal to cosine similarity.
    raise NotImplementedError("Implement encode")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors: 1.0 identical, 0.0 unrelated."""
    # TODO: implement. If both vectors are already normalised this is just a
    # dot product — but write the general form so it works either way.
    raise NotImplementedError("Implement cosine_similarity")


if __name__ == "__main__":
    # Week 3 experiment: pick five sentences of your own — some related in
    # meaning, some not — and look at the matrix. Does it match your intuition?
    sentences = [
        "Kedi kanepede uyuyor.",
        "Pisi koltukta uykuya dalmış.",
        "Yarın hava yağmurlu olacak.",
        "Python popüler bir programlama dilidir.",
        "Java da yaygın kullanılan bir dildir.",
    ]
    vectors = encode(sentences)
    matrix = vectors @ vectors.T
    np.set_printoptions(precision=3, suppress=True)
    print(matrix)
