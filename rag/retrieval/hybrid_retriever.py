"""Hybrid retriever: combines semantic, keyword, and structured search."""

from __future__ import annotations

from collections import defaultdict

from ..chunking.section_chunker import Chunk
from ..config import config
from ..embedding.bm25_index import BM25Index
from ..embedding.embed import Embedder
from ..store.chroma_store import ChromaStore
from ..store.structured_index import StructuredIndex
from .query_preprocessor import ProcessedQuery, QueryIntent


class HybridRetriever:
    """Combine semantic, keyword, and structured retrieval with RRF fusion."""

    def __init__(
        self,
        chroma_store: ChromaStore,
        bm25_index: BM25Index,
        structured_index: StructuredIndex,
        embedder: Embedder,
    ):
        self.chroma = chroma_store
        self.bm25 = bm25_index
        self.structured = structured_index
        self.embedder = embedder
        self.rrf_k = config.retrieval.rrf_k

    def retrieve(
        self, query: ProcessedQuery, top_k: int | None = None
    ) -> list[dict]:
        """Run hybrid retrieval and return fused results.

        Returns list of {chunk_id, text, metadata, score, sources}.
        """
        top_k = top_k or config.retrieval.top_k_final
        k_per_source = max(top_k * 2, 15)

        # 1. Structured lookup (direct match — always highest priority)
        structured_hits = self._structured_search(query)

        # 2. Semantic search (dense embeddings)
        semantic_hits = self._semantic_search(query, k_per_source)

        # 3. Keyword search (BM25)
        keyword_hits = self._keyword_search(query, k_per_source)

        # 4. Fuse with RRF
        fused = self._rrf_fuse(
            ranked_lists={
                "structured": structured_hits,
                "semantic": semantic_hits,
                "keyword": keyword_hits,
            },
            weights=self._intent_weights(query.intent),
        )

        # Return top-k
        return fused[:top_k]

    def _semantic_search(self, query: ProcessedQuery, top_k: int) -> list[dict]:
        """Dense vector search."""
        raw_emb, verb_emb = self.embedder.embed_query(query.normalized)

        # Search both raw and verbalized collections
        raw_hits = self.chroma.search(raw_emb, top_k=top_k)
        verb_hits = self.chroma.search_verbalized(verb_emb, top_k=top_k)

        # Merge, preferring lower distance
        seen: dict[str, dict] = {}
        for hit in raw_hits + verb_hits:
            cid = hit["chunk_id"]
            if cid not in seen or hit["distance"] < seen[cid]["distance"]:
                seen[cid] = hit

        # Sort by distance (ascending = more similar)
        sorted_hits = sorted(seen.values(), key=lambda h: h["distance"])
        return sorted_hits[:top_k]

    def _keyword_search(self, query: ProcessedQuery, top_k: int) -> list[dict]:
        """BM25 keyword search."""
        results = self.bm25.search(query.original, top_k=top_k)
        return [{"chunk_id": cid, "score": score} for cid, score in results]

    def _structured_search(self, query: ProcessedQuery) -> list[dict]:
        """Direct structured lookup based on extracted entities."""
        hits: list[dict] = []

        # Equation references
        for ref in query.equation_refs:
            chunk_ids = self.structured.lookup_equation(ref)
            for cid in chunk_ids[:5]:
                hits.append({"chunk_id": cid, "match_type": "equation"})

        # Figure references
        for ref in query.figure_refs:
            fig_info = self.structured.lookup_figure(ref)
            for cid in fig_info.get("chunk_ids", [])[:5]:
                hits.append({"chunk_id": cid, "match_type": "figure"})

        # Function references
        for ref in query.function_refs:
            chunk_ids = self.structured.lookup_function(ref)
            for cid in chunk_ids[:3]:
                hits.append({"chunk_id": cid, "match_type": "function"})

        # Parameter queries
        if query.parameter_refs or query.intent == QueryIntent.LOOKUP:
            for cid in self.structured.lookup_parameters()[:3]:
                hits.append({"chunk_id": cid, "match_type": "parameter"})

        return hits

    def _intent_weights(self, intent: QueryIntent) -> dict[str, float]:
        """Adjust retrieval source weights based on query intent."""
        weights = {
            QueryIntent.DERIVATION: {"structured": 1.0, "semantic": 1.5, "keyword": 0.5},
            QueryIntent.ALGORITHM: {"structured": 0.8, "semantic": 1.2, "keyword": 1.0},
            QueryIntent.CODE: {"structured": 2.0, "semantic": 0.8, "keyword": 1.0},
            QueryIntent.FIGURE: {"structured": 2.5, "semantic": 0.5, "keyword": 0.5},
            QueryIntent.INTERPRETATION: {"structured": 1.0, "semantic": 1.5, "keyword": 0.8},
            QueryIntent.EQUATION: {"structured": 3.0, "semantic": 0.5, "keyword": 0.5},
            QueryIntent.LOOKUP: {"structured": 2.0, "semantic": 0.5, "keyword": 1.0},
            QueryIntent.CONCEPTUAL: {"structured": 0.5, "semantic": 1.5, "keyword": 1.0},
        }
        return weights.get(intent, {"structured": 1.0, "semantic": 1.0, "keyword": 1.0})

    def _rrf_fuse(
        self,
        ranked_lists: dict[str, list[dict]],
        weights: dict[str, float],
    ) -> list[dict]:
        """Reciprocal Rank Fusion across multiple ranked lists."""
        scores: dict[str, float] = defaultdict(float)
        sources: dict[str, list[str]] = defaultdict(list)
        chunk_data: dict[str, dict] = {}

        for source_name, hits in ranked_lists.items():
            weight = weights.get(source_name, 1.0)
            for rank, hit in enumerate(hits):
                cid = hit["chunk_id"]
                # RRF score: weight / (k + rank + 1)
                scores[cid] += weight / (self.rrf_k + rank + 1)
                sources[cid].append(source_name)
                if cid not in chunk_data:
                    chunk_data[cid] = hit

        # Sort by fused score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for cid, score in ranked:
            entry = dict(chunk_data.get(cid, {}))
            entry["chunk_id"] = cid
            entry["rrf_score"] = score
            entry["sources"] = sources[cid]
            results.append(entry)

        return results
