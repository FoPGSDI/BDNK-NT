"""Structured lookup indices for equations, figures, and functions."""

from __future__ import annotations

import json
from pathlib import Path

from ..chunking.section_chunker import Chunk
from ..metadata.equation_index import EquationIndex
from ..metadata.figure_index import FigureIndex


class StructuredIndex:
    """Unified structured lookup for direct-match queries."""

    def __init__(self):
        self.equation_index = EquationIndex()
        self.figure_index = FigureIndex()
        self.function_index: dict[str, list[str]] = {}  # func_name -> [chunk_ids]
        self.parameter_chunks: list[str] = []  # chunk_ids containing parameter tables
        self._chunk_map: dict[str, Chunk] = {}

    def build(
        self,
        chunks: list[Chunk],
        figure_description_files: list[Path] | None = None,
    ) -> None:
        """Build all structured indices from chunks."""
        self._chunk_map = {c.chunk_id: c for c in chunks}

        # Equation index
        self.equation_index.build(chunks)

        # Figure index
        self.figure_index.build(chunks, figure_description_files)

        # Function index: map Wolfram function names to code chunks
        self.function_index.clear()
        for c in chunks:
            if c.chunk_type == "code":
                func_name = c.section.lower().split("(")[0].strip()
                if func_name not in self.function_index:
                    self.function_index[func_name] = []
                self.function_index[func_name].append(c.chunk_id)

        # Parameter table detection
        self.parameter_chunks = [
            c.chunk_id for c in chunks
            if any(
                term in c.text.lower()
                for term in ["table ii", "parameter", "γ =", "gamma =", "σ̂", "τ̂", "hat_sigma"]
            )
        ]

    def lookup_equation(self, ref: str) -> list[str]:
        """Look up chunk IDs by equation reference."""
        return self.equation_index.lookup(ref)

    def lookup_figure(self, ref: str) -> dict:
        """Look up figure info by reference."""
        return self.figure_index.lookup(ref)

    def lookup_function(self, name: str) -> list[str]:
        """Look up chunk IDs by function name."""
        name_lower = name.lower()
        # Try exact match first
        if name_lower in self.function_index:
            return self.function_index[name_lower]
        # Try partial match
        for fn, chunk_ids in self.function_index.items():
            if name_lower in fn or fn in name_lower:
                return chunk_ids
        return []

    def lookup_parameters(self) -> list[str]:
        """Return chunk IDs containing parameter tables."""
        return self.parameter_chunks

    def get_chunk(self, chunk_id: str) -> Chunk | None:
        """Retrieve a chunk by ID."""
        return self._chunk_map.get(chunk_id)

    def save(self, data_dir: Path) -> None:
        """Save all indices to disk."""
        data_dir.mkdir(parents=True, exist_ok=True)
        self.equation_index.save(data_dir / "equation_index.json")
        self.figure_index.save(data_dir / "figure_index.json")

        func_data = self.function_index
        (data_dir / "function_index.json").write_text(json.dumps(func_data, indent=2))
        (data_dir / "parameter_chunks.json").write_text(json.dumps(self.parameter_chunks))

    def load(self, data_dir: Path) -> None:
        """Load all indices from disk."""
        eq_path = data_dir / "equation_index.json"
        if eq_path.exists():
            self.equation_index.load(eq_path)

        fig_path = data_dir / "figure_index.json"
        if fig_path.exists():
            self.figure_index.load(fig_path)

        func_path = data_dir / "function_index.json"
        if func_path.exists():
            self.function_index = json.loads(func_path.read_text())

        param_path = data_dir / "parameter_chunks.json"
        if param_path.exists():
            self.parameter_chunks = json.loads(param_path.read_text())
