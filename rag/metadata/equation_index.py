"""Build and query an equation-number-to-chunk mapping."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..chunking.section_chunker import Chunk


class EquationIndex:
    """Maps paper equation numbers/labels to chunks that reference them."""

    def __init__(self):
        self.eq_to_chunks: dict[str, list[str]] = {}  # eq_ref -> [chunk_ids]
        self.chunk_to_eqs: dict[str, list[str]] = {}  # chunk_id -> [eq_refs]

    def build(self, chunks: list[Chunk]) -> None:
        """Build the index from a list of chunks."""
        self.eq_to_chunks.clear()
        self.chunk_to_eqs.clear()

        for chunk in chunks:
            eq_refs = chunk.equations_referenced
            # Also scan text for inline references
            text_refs = re.findall(
                r"(?:paper\s+)?[Ee]q(?:uation)?s?\.?\s*\(?([A-Z]?\d+)\)?",
                chunk.text,
            )
            all_refs = list(set(eq_refs + text_refs))

            self.chunk_to_eqs[chunk.chunk_id] = all_refs

            for ref in all_refs:
                normalized = self._normalize_ref(ref)
                if normalized not in self.eq_to_chunks:
                    self.eq_to_chunks[normalized] = []
                if chunk.chunk_id not in self.eq_to_chunks[normalized]:
                    self.eq_to_chunks[normalized].append(chunk.chunk_id)

    def lookup(self, equation_ref: str) -> list[str]:
        """Find chunk IDs that reference a given equation."""
        normalized = self._normalize_ref(equation_ref)
        return self.eq_to_chunks.get(normalized, [])

    def equations_for_chunk(self, chunk_id: str) -> list[str]:
        """Find equation refs associated with a chunk."""
        return self.chunk_to_eqs.get(chunk_id, [])

    def save(self, path: Path) -> None:
        """Save index to JSON."""
        data = {
            "eq_to_chunks": self.eq_to_chunks,
            "chunk_to_eqs": self.chunk_to_eqs,
        }
        path.write_text(json.dumps(data, indent=2))

    def load(self, path: Path) -> None:
        """Load index from JSON."""
        data = json.loads(path.read_text())
        self.eq_to_chunks = data["eq_to_chunks"]
        self.chunk_to_eqs = data["chunk_to_eqs"]

    @staticmethod
    def _normalize_ref(ref: str) -> str:
        """Normalize equation reference for matching."""
        ref = ref.strip().upper()
        # Remove parentheses, periods
        ref = re.sub(r"[().]", "", ref)
        # Collapse whitespace
        ref = re.sub(r"\s+", "", ref)
        return ref
