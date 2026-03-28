"""Cross-reference graph linking chunks across document classes."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from ..chunking.section_chunker import Chunk


class CrossRefGraph:
    """Graph of inter-chunk references: equation, figure, code, and dependency links."""

    def __init__(self):
        # Adjacency lists: chunk_id -> set of related chunk_ids
        self.edges: dict[str, set[str]] = defaultdict(set)
        self.edge_types: dict[tuple[str, str], str] = {}  # (src, dst) -> type

    def build(self, chunks: list[Chunk]) -> None:
        """Build the cross-reference graph from chunk metadata."""
        self.edges.clear()
        self.edge_types.clear()

        # Index chunks by various keys for cross-referencing
        by_id: dict[str, Chunk] = {c.chunk_id: c for c in chunks}
        by_source: dict[str, list[Chunk]] = defaultdict(list)
        by_section: dict[str, list[Chunk]] = defaultdict(list)
        by_equation: dict[str, list[Chunk]] = defaultdict(list)
        by_figure: dict[str, list[Chunk]] = defaultdict(list)
        code_chunks: dict[str, Chunk] = {}  # function_name -> chunk

        for c in chunks:
            by_source[c.source_file].append(c)
            by_section[c.section.lower()].append(c)

            for eq in c.equations_referenced:
                by_equation[eq.upper()].append(c)

            for fig in c.related_figures:
                by_figure[fig.lower()].append(c)

            if c.chunk_type == "code":
                # Extract function name from section
                code_chunks[c.section.lower()] = c

        # 1. Explicit dependency edges
        for c in chunks:
            for dep_id in c.depends_on_chunks:
                if dep_id in by_id:
                    self._add_edge(c.chunk_id, dep_id, "dependency")

        # 2. Shared equation references
        for eq_ref, ref_chunks in by_equation.items():
            for i, c1 in enumerate(ref_chunks):
                for c2 in ref_chunks[i + 1:]:
                    if c1.source_file != c2.source_file:
                        self._add_edge(c1.chunk_id, c2.chunk_id, "equation_ref")

        # 3. Shared figure references
        for fig_ref, fig_chunks in by_figure.items():
            for i, c1 in enumerate(fig_chunks):
                for c2 in fig_chunks[i + 1:]:
                    self._add_edge(c1.chunk_id, c2.chunk_id, "figure_ref")

        # 4. Code <-> math links via related_code metadata
        for c in chunks:
            for code_ref in c.related_code:
                code_key = code_ref.lower()
                if code_key in code_chunks:
                    self._add_edge(c.chunk_id, code_chunks[code_key].chunk_id, "code_link")

        # 5. Cross-document section name similarity
        # Link sections with similar names across different source files
        for section_name, sec_chunks in by_section.items():
            if len(sec_chunks) > 1:
                sources = set(c.source_file for c in sec_chunks)
                if len(sources) > 1:
                    for i, c1 in enumerate(sec_chunks):
                        for c2 in sec_chunks[i + 1:]:
                            if c1.source_file != c2.source_file:
                                self._add_edge(c1.chunk_id, c2.chunk_id, "section_match")

    def _add_edge(self, src: str, dst: str, edge_type: str) -> None:
        """Add a bidirectional edge."""
        self.edges[src].add(dst)
        self.edges[dst].add(src)
        self.edge_types[(src, dst)] = edge_type
        self.edge_types[(dst, src)] = edge_type

    def neighbors(self, chunk_id: str, edge_type: str | None = None) -> list[str]:
        """Get neighboring chunk IDs, optionally filtered by edge type."""
        if edge_type is None:
            return list(self.edges.get(chunk_id, set()))
        return [
            n for n in self.edges.get(chunk_id, set())
            if self.edge_types.get((chunk_id, n)) == edge_type
        ]

    def get_connected_component(self, chunk_id: str, max_depth: int = 2) -> set[str]:
        """BFS to find connected chunks within max_depth hops."""
        visited: set[str] = set()
        frontier = {chunk_id}
        for _ in range(max_depth):
            next_frontier: set[str] = set()
            for node in frontier:
                if node not in visited:
                    visited.add(node)
                    next_frontier.update(self.edges.get(node, set()))
            frontier = next_frontier - visited
        visited.update(frontier)
        return visited

    def save(self, path: Path) -> None:
        """Save graph to JSON."""
        data = {
            "edges": {k: list(v) for k, v in self.edges.items()},
            "edge_types": {f"{k[0]}|{k[1]}": v for k, v in self.edge_types.items()},
        }
        path.write_text(json.dumps(data, indent=2))

    def load(self, path: Path) -> None:
        """Load graph from JSON."""
        data = json.loads(path.read_text())
        self.edges = defaultdict(set, {k: set(v) for k, v in data["edges"].items()})
        self.edge_types = {}
        for key_str, val in data["edge_types"].items():
            src, dst = key_str.split("|", 1)
            self.edge_types[(src, dst)] = val
