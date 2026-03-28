"""Metadata extraction and cross-reference indexing."""

from .equation_index import EquationIndex
from .cross_ref_graph import CrossRefGraph
from .figure_index import FigureIndex

__all__ = ["EquationIndex", "CrossRefGraph", "FigureIndex"]
