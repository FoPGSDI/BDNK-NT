"""Embedding pipeline: dense vector embeddings for all chunks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from ..chunking.section_chunker import Chunk
from ..config import config


# LaTeX symbol to English verbalization map
LATEX_VERBALIZATIONS = {
    r"\hat{\sigma}": "sigma-hat",
    r"\hat{\tau}": "tau-hat",
    r"\hat{V}": "V-hat",
    r"\hat{B}": "B-hat",
    r"\hat{C}": "C-hat",
    r"\hat{D}": "D-hat",
    r"\hat{E}": "E-hat",
    r"\Gamma": "Gamma",
    r"\epsilon": "epsilon (energy density)",
    r"\rho": "rho (enthalpy density)",
    r"\Delta^{ab}": "projection tensor Delta",
    r"c_+": "positive characteristic speed c-plus",
    r"c_-": "negative characteristic speed c-minus",
    r"c_1": "baryon characteristic speed c-one",
    r"c_s": "sound speed",
    r"\beta_\epsilon": "beta-epsilon (heat flux coefficient)",
    r"\beta_n": "beta-n (baryon heat flux coefficient)",
    r"\tau_\epsilon": "tau-epsilon (energy relaxation time)",
    r"\tau_P": "tau-P (pressure relaxation time)",
    r"\tau_Q": "tau-Q (heat flux relaxation time)",
    r"T^{ab}": "stress-energy tensor",
    r"J^a": "baryon current",
    r"Q^a": "heat flux vector",
    r"\leq": "is less than or equal to",
    r"\geq": "is greater than or equal to",
    r"\equiv": "is defined as",
    r"\partial": "partial derivative",
    r"\nabla": "covariant derivative",
}


def verbalize_latex(text: str) -> str:
    """Convert LaTeX math expressions to natural language for embedding."""
    verbalized = text
    for latex, english in LATEX_VERBALIZATIONS.items():
        verbalized = verbalized.replace(latex, english)

    # Strip remaining LaTeX commands
    verbalized = re.sub(r"\$\$?", "", verbalized)
    verbalized = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", verbalized)
    verbalized = re.sub(r"\\[a-zA-Z]+", " ", verbalized)
    verbalized = re.sub(r"[{}^_]", " ", verbalized)
    verbalized = re.sub(r"\s+", " ", verbalized).strip()
    return verbalized


def chunk_hash(text: str) -> str:
    """Deterministic hash for dedup and change detection."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


class Embedder:
    """Manage dense embeddings for chunks."""

    def __init__(self, provider: str | None = None, model_name: str | None = None):
        self.provider = provider or config.embedding.provider
        self.model_name = model_name or config.embedding.model_name
        self.batch_size = config.embedding.batch_size
        self._client = None

    def _get_client(self):
        """Lazy-initialize the embedding client."""
        if self._client is not None:
            return self._client

        if self.provider == "voyage":
            import voyageai
            self._client = voyageai.Client()
        elif self.provider == "openai":
            import openai
            self._client = openai.OpenAI()
        elif self.provider == "local":
            from sentence_transformers import SentenceTransformer
            self._client = SentenceTransformer(self.model_name)
        else:
            raise ValueError(f"Unknown embedding provider: {self.provider}")

        return self._client

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts, returning vectors."""
        client = self._get_client()
        all_embeddings: list[list[float]] = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]

            if self.provider == "voyage":
                result = client.embed(batch, model=self.model_name)
                all_embeddings.extend(result.embeddings)
            elif self.provider == "openai":
                result = client.embeddings.create(input=batch, model=self.model_name)
                all_embeddings.extend([d.embedding for d in result.data])
            elif self.provider == "local":
                vectors = client.encode(batch, show_progress_bar=False)
                all_embeddings.extend(vectors.tolist())

        return all_embeddings

    def embed_chunks(self, chunks: list[Chunk]) -> list[dict]:
        """Embed all chunks, producing both raw and verbalized embeddings.

        Returns list of dicts: {chunk_id, text_hash, embedding, verbalized_embedding}
        """
        raw_texts = [c.text for c in chunks]
        verbalized_texts = [verbalize_latex(c.text) for c in chunks]

        raw_embeddings = self.embed_texts(raw_texts)
        verbalized_embeddings = self.embed_texts(verbalized_texts)

        results = []
        for chunk, raw_emb, verb_emb in zip(chunks, raw_embeddings, verbalized_embeddings):
            results.append({
                "chunk_id": chunk.chunk_id,
                "text_hash": chunk_hash(chunk.text),
                "embedding": raw_emb,
                "verbalized_embedding": verb_emb,
            })

        return results

    def embed_query(self, query: str) -> tuple[list[float], list[float]]:
        """Embed a query in both raw and verbalized forms."""
        raw = self.embed_texts([query])[0]
        verbalized = self.embed_texts([verbalize_latex(query)])[0]
        return raw, verbalized


class EmbeddingCache:
    """File-based cache to avoid re-embedding unchanged chunks."""

    def __init__(self, cache_path: Path):
        self.cache_path = cache_path
        self._cache: dict[str, dict] = {}
        if cache_path.exists():
            self._cache = json.loads(cache_path.read_text())

    def get(self, chunk_id: str, text_hash: str) -> dict | None:
        """Return cached embedding if hash matches."""
        entry = self._cache.get(chunk_id)
        if entry and entry.get("text_hash") == text_hash:
            return entry
        return None

    def put(self, chunk_id: str, data: dict) -> None:
        """Cache an embedding result."""
        self._cache[chunk_id] = data

    def save(self) -> None:
        """Persist cache to disk."""
        self.cache_path.write_text(json.dumps(self._cache))
