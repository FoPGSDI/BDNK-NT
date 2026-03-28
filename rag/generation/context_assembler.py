"""Assemble retrieved chunks into LLM prompt context."""

from __future__ import annotations

from ..chunking.section_chunker import Chunk
from ..config import config
from ..retrieval.query_preprocessor import ProcessedQuery, QueryIntent


# Notation conventions (loaded from progress/conventions.md summary)
CONVENTIONS_PREAMBLE = """
Notation conventions for BDNK viscous relativistic hydrodynamics:
- $u^a$: fluid 4-velocity (timelike, $u^a u_a = -1$)
- $\\epsilon$: energy density, $n$: baryon number density, $P$: pressure
- $\\rho = \\epsilon + P$: enthalpy density
- $T$: temperature ($T = P/n$ for ideal gas)
- $\\Gamma$: adiabatic index ($1 < \\Gamma < 2$), $m$: rest mass per baryon
- EOS: $P = (\\Gamma - 1)(\\epsilon - mn)$ (gamma-law ideal gas)
- $c_s^2 = \\Gamma P / \\rho$: sound speed squared
- $\\Delta^{ab} = g^{ab} + u^a u^b$: spatial projector
- $T^{ab}$: stress-energy tensor, $J^a$: baryon current
- $Q^a$: heat flux vector (spatial: $Q^a u_a = 0$)
- Transport: $V$ (viscosity), $\\sigma$ (heat conductivity), $\\tau_\\epsilon, \\tau_P, \\tau_Q$ (relaxation times)
- Dimensionless: $\\hat{V}, \\hat{\\sigma}, \\hat{\\tau}$ (hatted = scaled by $\\rho$)
- $\\beta_\\epsilon, \\beta_n$: BDNK heat flux coefficients
- Characteristic speeds: $c_+, c_-, c_1$ (from Eqs. A26-A27)
- Stability: $\\hat{\\sigma} \\leq 1/3$; Causality: $|c_\\pm| < 1$
- Confidence markers: [SOLID], [PRELIMINARY], [HYPOTHESIS]
""".strip()

# System prompt for the LLM
SYSTEM_PROMPT_TEMPLATE = """You are a research assistant specializing in BDNK viscous relativistic hydrodynamics \
(Pandya, Most, Pretorius 2022). You answer questions using retrieved context from the research corpus.

{conventions}

Rules:
- Use LaTeX math notation with $...$ delimiters for inline and $$...$$ for display
- Cite sources as [source_file, Section X.Y] after claims
- Mark confidence: [SOLID] for verified results, [PRELIMINARY] for partial, [HYPOTHESIS] for conjectured
- Reference paper equations as (ref: paper Eq. XX)
- When showing derivations, show every step — no step-skipping
- If the retrieved context is insufficient to answer, say so explicitly
- Do not fabricate equations or results not supported by the context
"""


class ContextAssembler:
    """Assemble retrieved chunks into a structured prompt context."""

    def __init__(self, chunk_map: dict[str, Chunk]):
        self.chunk_map = chunk_map

    def assemble(
        self,
        query: ProcessedQuery,
        chunk_ids: list[str],
        max_tokens: int | None = None,
    ) -> dict:
        """Assemble the full prompt components.

        Returns dict with keys: system_prompt, context_blocks, user_message.
        """
        budget = max_tokens or config.generation.context_budget_tokens

        # Build system prompt
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(conventions=CONVENTIONS_PREAMBLE)

        # Build context blocks from chunks, respecting budget
        context_blocks: list[str] = []
        total_tokens = 0

        for cid in chunk_ids:
            chunk = self.chunk_map.get(cid)
            if not chunk:
                continue

            if total_tokens + chunk.token_estimate > budget:
                break

            block = self._format_chunk_block(chunk)
            context_blocks.append(block)
            total_tokens += chunk.token_estimate

        # Build user message with intent hint
        user_message = self._format_user_message(query)

        return {
            "system_prompt": system_prompt,
            "context_blocks": context_blocks,
            "context_text": "\n\n---\n\n".join(context_blocks),
            "user_message": user_message,
            "token_estimate": total_tokens + len(system_prompt) // 4,
        }

    def _format_chunk_block(self, chunk: Chunk) -> str:
        """Format a single chunk as a context block with metadata header."""
        header_parts = [f"Source: {chunk.source_file}"]
        if chunk.section:
            header_parts.append(f"Section: {chunk.section}")
        if chunk.chunk_type:
            header_parts.append(f"Type: {chunk.chunk_type}")
        if chunk.confidence:
            header_parts.append(f"Confidence: [{chunk.confidence}]")
        if chunk.equations_referenced:
            header_parts.append(f"Equations: {', '.join(chunk.equations_referenced[:5])}")

        header = " | ".join(header_parts)
        return f"[{header}]\n{chunk.text}"

    def _format_user_message(self, query: ProcessedQuery) -> str:
        """Format the user message with the original query."""
        intent_hints = {
            QueryIntent.DERIVATION: "Please show the derivation step by step.",
            QueryIntent.ALGORITHM: "Describe the numerical method and algorithm.",
            QueryIntent.CODE: "Show relevant code and explain the implementation.",
            QueryIntent.FIGURE: "Describe what this figure shows and its significance.",
            QueryIntent.INTERPRETATION: "Provide physical interpretation with references.",
            QueryIntent.EQUATION: "Explain this equation in context.",
            QueryIntent.LOOKUP: "Provide the specific value or parameter requested.",
            QueryIntent.CONCEPTUAL: "Explain the concept clearly with context.",
        }

        hint = intent_hints.get(query.intent, "")
        if hint:
            return f"{query.original}\n\n({hint})"
        return query.original
