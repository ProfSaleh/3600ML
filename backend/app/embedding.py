from __future__ import annotations

import hashlib
import math
import re
from typing import List

from openai import OpenAI

from .config import settings


def _l2_normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def _local_hash_embedding(text: str) -> list[float]:
    # Deterministic lightweight fallback embedding for environments without API keys.
    dim = settings.embedding_dimensions
    vector = [0.0] * dim
    tokens = _tokenize(text)
    if not tokens:
        return vector

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for i in range(0, len(digest), 4):
            idx_seed = int.from_bytes(digest[i : i + 2], "big")
            sign_seed = digest[i + 2] if i + 2 < len(digest) else 0
            idx = idx_seed % dim
            sign = -1.0 if sign_seed % 2 else 1.0
            vector[idx] += sign
    return _l2_normalize(vector)


def embed_text(text: str) -> list[float]:
    clean = (text or "").strip()
    if not clean:
        return [0.0] * settings.embedding_dimensions

    if settings.embedding_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is required when EMBEDDING_PROVIDER=openai."
            )
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=clean,
        )
        vector = response.data[0].embedding
        if len(vector) != settings.embedding_dimensions:
            raise ValueError(
                f"Embedding dimension mismatch: expected {settings.embedding_dimensions}, got {len(vector)}"
            )
        return vector

    return _local_hash_embedding(clean)


def cosine_similarity(a: List[float] | None, b: List[float] | None) -> float:
    if not a or not b:
        return 0.0
    if len(a) != len(b):
        return 0.0

    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot_product / (norm_a * norm_b)))
