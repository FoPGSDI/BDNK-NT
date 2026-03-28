"""Figure number to description mapping."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..chunking.section_chunker import Chunk


# Canonical figure info from the paper
FIGURE_CATALOG = {
    "fig1": {
        "title": "Bjorken flow",
        "pdf": "bjorken_plot.pdf",
        "generated": ["fig1_top.pdf", "fig1_bottom.pdf", "fig1_combined.pdf"],
        "code": "bjorken.wl",
        "test_section": "Test 2",
    },
    "fig2": {
        "title": "Steady-state shockwave profiles",
        "pdf": "shockwave_plot.pdf",
        "generated": ["fig2.pdf"],
        "code": "shockwave_steady.wl",
        "test_section": "Test 3",
    },
    "fig3": {
        "title": "Shockwave instability onset",
        "pdf": "shock_instability.pdf",
        "generated": ["fig3.pdf"],
        "code": "shockwave_dynamic.wl",
        "test_section": "Test 4",
    },
    "fig4": {
        "title": "Acausality instability for various frames",
        "pdf": "acaus_instab.pdf",
        "generated": ["fig4.pdf"],
        "code": "shockwave_dynamic.wl",
        "test_section": "Test 5",
    },
    "fig5": {
        "title": "Heat flow stationary test",
        "pdf": "heat_stationary.pdf",
        "generated": ["fig5.pdf"],
        "code": "heat_flow.wl",
        "test_section": "Test 6",
    },
    "fig6": {
        "title": "Telegrapher's equation behavior",
        "pdf": "telegraphers_plot.pdf",
        "generated": ["fig6.pdf"],
        "code": "heat_flow.wl",
        "test_section": "Test 7",
    },
    "fig7": {
        "title": "Convergence plot",
        "pdf": "conv_plot.pdf",
        "generated": ["fig7.pdf"],
        "code": "convergence.wl",
        "test_section": "Convergence analysis",
    },
}


class FigureIndex:
    """Maps figure numbers to descriptions and related chunks."""

    def __init__(self):
        self.figure_to_chunks: dict[str, list[str]] = {}
        self.figure_descriptions: dict[str, str] = {}
        self.catalog = dict(FIGURE_CATALOG)

    def build(self, chunks: list[Chunk], description_files: list[Path] | None = None) -> None:
        """Build the figure index from chunks and description files."""
        self.figure_to_chunks.clear()
        self.figure_descriptions.clear()

        # Collect chunks referencing each figure
        for chunk in chunks:
            for fig_ref in chunk.related_figures:
                fig_key = fig_ref.lower()
                if fig_key not in self.figure_to_chunks:
                    self.figure_to_chunks[fig_key] = []
                self.figure_to_chunks[fig_key].append(chunk.chunk_id)

            # Also scan text for figure references
            for m in re.finditer(r"Fig(?:ure)?\.?\s*(\d+)", chunk.text, re.IGNORECASE):
                fig_key = f"fig{m.group(1)}"
                if fig_key not in self.figure_to_chunks:
                    self.figure_to_chunks[fig_key] = []
                if chunk.chunk_id not in self.figure_to_chunks[fig_key]:
                    self.figure_to_chunks[fig_key].append(chunk.chunk_id)

        # Load descriptions from progress/figure-*.md files
        if description_files:
            for fpath in description_files:
                fig_num = re.search(r"figure-(\w+)", fpath.name)
                if fig_num:
                    text = fpath.read_text(encoding="utf-8")
                    # Map common names to figure numbers
                    name_to_fig = {
                        "bjorken": "fig1",
                        "shockwave": "fig2",
                        "shock-instability": "fig3",
                        "acaus-instab": "fig4",
                        "heat-stationary": "fig5",
                        "telegraphers": "fig6",
                        "convergence": "fig7",
                    }
                    fig_key = name_to_fig.get(fig_num.group(1), f"fig_{fig_num.group(1)}")
                    self.figure_descriptions[fig_key] = text[:2000]  # cap length

    def lookup(self, figure_ref: str) -> dict:
        """Look up a figure by reference (e.g., 'fig3', 'Figure 3', '3')."""
        # Normalize
        fig_num = re.search(r"(\d+)", figure_ref)
        if not fig_num:
            return {}

        fig_key = f"fig{fig_num.group(1)}"

        result = {}
        if fig_key in self.catalog:
            result["catalog"] = self.catalog[fig_key]
        if fig_key in self.figure_descriptions:
            result["description"] = self.figure_descriptions[fig_key]
        if fig_key in self.figure_to_chunks:
            result["chunk_ids"] = self.figure_to_chunks[fig_key]

        return result

    def save(self, path: Path) -> None:
        """Save index to JSON."""
        data = {
            "figure_to_chunks": self.figure_to_chunks,
            "figure_descriptions": {k: v[:500] for k, v in self.figure_descriptions.items()},
        }
        path.write_text(json.dumps(data, indent=2))

    def load(self, path: Path) -> None:
        """Load index from JSON."""
        data = json.loads(path.read_text())
        self.figure_to_chunks = data.get("figure_to_chunks", {})
        self.figure_descriptions = data.get("figure_descriptions", {})
