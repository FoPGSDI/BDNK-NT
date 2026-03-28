"""Query preprocessor: intent classification, entity extraction, math normalization."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class QueryIntent(Enum):
    """Classified query intent."""

    DERIVATION = "derivation"       # "Derive X", "Show the derivation of..."
    ALGORITHM = "algorithm"         # "How is X implemented?", "What numerical method..."
    CODE = "code"                   # "Show the code for...", function names
    INTERPRETATION = "interpretation"  # "What does Fig N show?", "Why does..."
    LOOKUP = "lookup"               # "What parameters...", "What is the value of..."
    CONCEPTUAL = "conceptual"       # "What is the difference between...", "Explain..."
    FIGURE = "figure"               # "Figure 3", "Fig. 5"
    EQUATION = "equation"           # "Eq. 29", "Equation A26"


@dataclass
class ProcessedQuery:
    """A preprocessed query with extracted metadata."""

    original: str
    normalized: str  # math symbols normalized
    intent: QueryIntent
    entities: dict = field(default_factory=dict)
    # Extracted references
    equation_refs: list[str] = field(default_factory=list)
    figure_refs: list[str] = field(default_factory=list)
    function_refs: list[str] = field(default_factory=list)
    parameter_refs: list[str] = field(default_factory=list)


# Intent classification patterns
INTENT_PATTERNS: list[tuple[re.Pattern, QueryIntent]] = [
    (re.compile(r"\bderiv(?:e|ation|ing)\b", re.I), QueryIntent.DERIVATION),
    (re.compile(r"\bshow\s+(?:the\s+)?(?:derivation|proof|steps)\b", re.I), QueryIntent.DERIVATION),
    (re.compile(r"\b(?:numerical|algorithm|method|discretiz|solver|scheme)\b", re.I), QueryIntent.ALGORITHM),
    (re.compile(r"\b(?:implement|pseudocode|how\s+is\s+.+\s+(?:solved|computed|calculated))\b", re.I), QueryIntent.ALGORITHM),
    (re.compile(r"\b(?:code|function|script|\.wl)\b", re.I), QueryIntent.CODE),
    (re.compile(r"\b(?:transportCoeffs|charSpeeds|pressure|enthalpy|soundSpeed|bdnkTab)\b"), QueryIntent.CODE),
    (re.compile(r"\bFig(?:ure)?\.?\s*\d+\b", re.I), QueryIntent.FIGURE),
    (re.compile(r"\b(?:what\s+does\s+fig|plot|panel|axes|shows?)\b", re.I), QueryIntent.INTERPRETATION),
    (re.compile(r"\bEq(?:uation)?s?\.?\s*\(?[A-Z]?\d+", re.I), QueryIntent.EQUATION),
    (re.compile(r"\b(?:parameter|value\s+of|table\s+II|Γ|gamma|σ̂|τ̂)\b", re.I), QueryIntent.LOOKUP),
    (re.compile(r"\b(?:what\s+is|what\s+are|explain|difference|compare|why)\b", re.I), QueryIntent.CONCEPTUAL),
]

# Entity extraction patterns
EQ_REF_RE = re.compile(r"[Ee]q(?:uation)?s?\.?\s*\(?([A-Z]?\d+(?:\s*[-–,]\s*[A-Z]?\d+)*)\)?")
FIG_REF_RE = re.compile(r"Fig(?:ure)?\.?\s*(\d+)", re.I)
FUNC_REF_RE = re.compile(r"\b(transportCoeffs|charSpeeds|pressure|enthalpy|soundSpeed(?:Sq)?|bdnkTab|temperature|solveRankineHugoniot|applyOutflowBC|minmod)\b")
PARAM_RE = re.compile(r"(σ̂|τ̂|V̂|\\hat\{\\sigma\}|\\hat\{\\tau\}|\\hat\{V\}|hat_sigma|hat_tau|hat_V|Γ|Gamma|gamma)\b", re.I)

# Math symbol normalization
MATH_NORMALIZATIONS = [
    (r"sigma[- ]?hat", r"\\hat{\\sigma}"),
    (r"tau[- ]?hat", r"\\hat{\\tau}"),
    (r"v[- ]?hat", r"\\hat{V}"),
    (r"c[- ]?plus|c_\+|c\+", r"c_+"),
    (r"c[- ]?minus|c_\-|c-", r"c_-"),
    (r"sound speed", r"c_s"),
    (r"energy density", r"\\epsilon"),
    (r"enthalpy density", r"\\rho"),
    (r"stress[- ]?energy", r"T^{ab}"),
    (r"heat flux", r"Q^a"),
    (r"baryon current", r"J^a"),
]


class QueryPreprocessor:
    """Preprocess user queries for retrieval."""

    def process(self, query: str) -> ProcessedQuery:
        """Analyze and preprocess a query."""
        # Classify intent
        intent = self._classify_intent(query)

        # Normalize math symbols
        normalized = self._normalize_math(query)

        # Extract entities
        equation_refs = [m.group(1) for m in EQ_REF_RE.finditer(query)]
        figure_refs = [m.group(1) for m in FIG_REF_RE.finditer(query)]
        function_refs = [m.group(1) for m in FUNC_REF_RE.finditer(query)]
        parameter_refs = [m.group(1) for m in PARAM_RE.finditer(query)]

        return ProcessedQuery(
            original=query,
            normalized=normalized,
            intent=intent,
            equation_refs=equation_refs,
            figure_refs=figure_refs,
            function_refs=function_refs,
            parameter_refs=parameter_refs,
        )

    def _classify_intent(self, query: str) -> QueryIntent:
        """Classify the query intent using pattern matching."""
        for pattern, intent in INTENT_PATTERNS:
            if pattern.search(query):
                return intent
        return QueryIntent.CONCEPTUAL  # default

    def _normalize_math(self, query: str) -> str:
        """Normalize math symbols in the query."""
        normalized = query
        for pattern, replacement in MATH_NORMALIZATIONS:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        return normalized
