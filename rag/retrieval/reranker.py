"""Re-ranker: cross-encoder scoring with domain-specific boosts."""

from __future__ import annotations

from ..chunking.section_chunker import Chunk
from ..config import config
from .query_preprocessor import ProcessedQuery, QueryIntent


class Reranker:
    """Re-rank retrieved chunks using cross-encoder and domain heuristics."""

    def __init__(self, chunk_map: dict[str, Chunk], use_cross_encoder: bool = True):
        self.chunk_map = chunk_map
        self.use_cross_encoder = use_cross_encoder
        self._model = None

    def _get_model(self):
        """Lazy-load cross-encoder model."""
        if self._model is not None:
            return self._model

        if not self.use_cross_encoder:
            return None

        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
        except ImportError:
            self._model = None

        return self._model

    def rerank(
        self,
        query: ProcessedQuery,
        candidates: list[dict],
        top_n: int | None = None,
    ) -> list[dict]:
        """Re-rank candidates and return top_n results."""
        top_n = top_n or config.retrieval.rerank_top_n

        # Score each candidate
        scored = []
        for candidate in candidates:
            cid = candidate["chunk_id"]
            chunk = self.chunk_map.get(cid)
            if not chunk:
                continue

            # Base score from retrieval
            base_score = candidate.get("rrf_score", 0.0)

            # Cross-encoder score
            ce_score = self._cross_encoder_score(query.original, chunk.text)

            # Domain-specific boosts
            boost = self._compute_boost(query, chunk, candidate)

            final_score = base_score + ce_score * 0.3 + boost
            scored.append({
                **candidate,
                "final_score": final_score,
                "base_score": base_score,
                "ce_score": ce_score,
                "boost": boost,
            })

        # Sort by final score
        scored.sort(key=lambda x: x["final_score"], reverse=True)

        return scored[:top_n]

    def _cross_encoder_score(self, query: str, text: str) -> float:
        """Score query-document pair with cross-encoder."""
        model = self._get_model()
        if model is None:
            return 0.0

        # Truncate text to avoid model limits
        truncated = text[:512]
        score = model.predict([(query, truncated)])
        return float(score[0]) if hasattr(score, '__iter__') else float(score)

    def _compute_boost(self, query: ProcessedQuery, chunk: Chunk, candidate: dict) -> float:
        """Compute domain-specific scoring boosts."""
        boost = 0.0

        # Boost for matching source document to intent
        intent_source_affinity = {
            QueryIntent.DERIVATION: {"mathematical-derivations.md": 0.3},
            QueryIntent.ALGORITHM: {"numerical-implementations.md": 0.3},
            QueryIntent.CODE: {".wl": 0.3},
            QueryIntent.FIGURE: {"test-results.md": 0.2, "figure-": 0.3},
            QueryIntent.INTERPRETATION: {"test-results.md": 0.3},
            QueryIntent.LOOKUP: {"numerical-implementations.md": 0.2, "test-results.md": 0.2},
            QueryIntent.CONCEPTUAL: {"mathematical-derivations.md": 0.2},
        }

        affinities = intent_source_affinity.get(query.intent, {})
        for source_pattern, bonus in affinities.items():
            if source_pattern in chunk.source_file:
                boost += bonus

        # Boost for SOLID confidence over PRELIMINARY
        if chunk.confidence == "SOLID":
            boost += 0.1
        elif chunk.confidence == "PRELIMINARY":
            boost -= 0.05

        # Boost for multi-source retrieval (found by multiple methods)
        sources = candidate.get("sources", [])
        if len(sources) > 1:
            boost += 0.1 * (len(sources) - 1)

        # Boost for chunks from same section as other top candidates
        if "structured" in sources:
            boost += 0.2

        # Penalty for very small chunks (likely noise)
        if chunk.token_estimate < 50:
            boost -= 0.2

        return boost
