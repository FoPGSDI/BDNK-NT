"""BM25 keyword search index over chunks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..chunking.section_chunker import Chunk


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric, keep LaTeX symbols."""
    # Preserve some LaTeX-specific tokens
    text = text.lower()
    # Replace LaTeX commands with readable tokens
    text = re.sub(r"\\hat\{(\w)\}", r"hat_\1", text)
    text = re.sub(r"\\(\w+)", r"\1", text)
    # Split on non-word chars but keep underscores
    tokens = re.findall(r"[a-z0-9_]+", text)
    # Filter stopwords
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "and", "but", "or",
        "not", "no", "if", "then", "else", "when", "where", "how", "what",
        "which", "who", "whom", "this", "that", "these", "those", "it", "its",
        "we", "our", "they", "their", "he", "she", "his", "her",
    }
    return [t for t in tokens if t not in stopwords and len(t) > 1]


class BM25Index:
    """BM25 keyword search over chunk corpus."""

    def __init__(self):
        self.chunk_ids: list[str] = []
        self.corpus: list[list[str]] = []  # tokenized documents
        self._bm25 = None

    def build(self, chunks: list[Chunk]) -> None:
        """Build the BM25 index from chunks."""
        self.chunk_ids = [c.chunk_id for c in chunks]
        self.corpus = [tokenize(c.text) for c in chunks]
        self._build_bm25()

    def _build_bm25(self) -> None:
        """Initialize the BM25 scorer."""
        try:
            from rank_bm25 import BM25Okapi
            self._bm25 = BM25Okapi(self.corpus)
        except ImportError:
            # Fallback: simple TF-IDF-like scoring
            self._bm25 = None

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search for chunks matching query. Returns (chunk_id, score) pairs."""
        query_tokens = tokenize(query)

        if not query_tokens:
            return []

        if self._bm25 is not None:
            scores = self._bm25.get_scores(query_tokens)
            # Get top-k indices
            ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
            return [(self.chunk_ids[i], float(scores[i])) for i in ranked if scores[i] > 0]

        # Fallback: simple term frequency matching
        return self._fallback_search(query_tokens, top_k)

    def _fallback_search(self, query_tokens: list[str], top_k: int) -> list[tuple[str, float]]:
        """Simple TF matching when rank_bm25 is not available."""
        query_set = set(query_tokens)
        scores: list[tuple[str, float]] = []

        for chunk_id, doc_tokens in zip(self.chunk_ids, self.corpus):
            doc_set = set(doc_tokens)
            overlap = len(query_set & doc_set)
            if overlap > 0:
                # Normalize by doc length
                score = overlap / (len(doc_set) ** 0.5)
                scores.append((chunk_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def save(self, path: Path) -> None:
        """Save the index data (not the BM25 object, which is rebuilt)."""
        data = {
            "chunk_ids": self.chunk_ids,
            "corpus": self.corpus,
        }
        path.write_text(json.dumps(data))

    def load(self, path: Path) -> None:
        """Load index data and rebuild BM25."""
        data = json.loads(path.read_text())
        self.chunk_ids = data["chunk_ids"]
        self.corpus = data["corpus"]
        self._build_bm25()
