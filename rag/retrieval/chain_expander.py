"""Derivation chain expander: pulls in prerequisite chunks for coherent math."""

from __future__ import annotations

from ..chunking.section_chunker import Chunk
from ..metadata.cross_ref_graph import CrossRefGraph
from ..config import config


class ChainExpander:
    """Expand retrieved set to include derivation chain prerequisites."""

    def __init__(
        self,
        chunk_map: dict[str, Chunk],
        cross_ref_graph: CrossRefGraph,
        max_depth: int | None = None,
    ):
        self.chunk_map = chunk_map
        self.graph = cross_ref_graph
        self.max_depth = max_depth or config.retrieval.chain_expansion_depth

    def expand(
        self,
        retrieved_chunk_ids: list[str],
        budget_tokens: int | None = None,
    ) -> list[str]:
        """Expand retrieved set with prerequisite chunks.

        Returns ordered list of chunk_ids (dependencies first, then originals).
        """
        budget = budget_tokens or config.generation.context_budget_tokens
        expanded: set[str] = set(retrieved_chunk_ids)
        deps_to_add: list[str] = []

        # For each retrieved chunk, walk dependency chain
        for cid in retrieved_chunk_ids:
            chunk = self.chunk_map.get(cid)
            if not chunk:
                continue

            # Only expand derivation-type chunks
            if chunk.chunk_type != "derivation" and not chunk.depends_on_chunks:
                continue

            # Walk backwards through depends_on_chunks
            chain = self._walk_dependencies(cid)
            for dep_id in chain:
                if dep_id not in expanded:
                    deps_to_add.append(dep_id)
                    expanded.add(dep_id)

        # Also pull in cross-reference neighbors for multi-document coverage
        for cid in list(retrieved_chunk_ids):
            neighbors = self.graph.neighbors(cid, edge_type="equation_ref")
            for n in neighbors[:2]:  # Limit cross-doc expansion
                if n not in expanded:
                    dep_chunk = self.chunk_map.get(n)
                    if dep_chunk and dep_chunk.source_file != self.chunk_map.get(cid, dep_chunk).source_file:
                        deps_to_add.append(n)
                        expanded.add(n)

        # Order: dependencies first, then originals (preserving input order)
        ordered = []
        total_tokens = 0

        # Add dependencies (in chain order)
        for dep_id in deps_to_add:
            chunk = self.chunk_map.get(dep_id)
            if chunk and total_tokens + chunk.token_estimate <= budget:
                ordered.append(dep_id)
                total_tokens += chunk.token_estimate

        # Add original retrieved chunks
        for cid in retrieved_chunk_ids:
            if cid not in ordered:
                chunk = self.chunk_map.get(cid)
                if chunk and total_tokens + chunk.token_estimate <= budget:
                    ordered.append(cid)
                    total_tokens += chunk.token_estimate

        return ordered

    def _walk_dependencies(self, chunk_id: str, depth: int = 0) -> list[str]:
        """Recursively walk dependency chain backwards."""
        if depth >= self.max_depth:
            return []

        chunk = self.chunk_map.get(chunk_id)
        if not chunk or not chunk.depends_on_chunks:
            return []

        chain: list[str] = []
        for dep_id in chunk.depends_on_chunks:
            # Recurse into dependency's dependencies
            sub_chain = self._walk_dependencies(dep_id, depth + 1)
            chain.extend(sub_chain)
            chain.append(dep_id)

        return chain
