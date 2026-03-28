"""Derivation-chain-aware chunker for mathematical content."""

from __future__ import annotations

import re

from .section_chunker import Chunk, estimate_tokens


# Display math block: $$...$$ or \begin{align}...\end{align}
DISPLAY_MATH_RE = re.compile(
    r"(\$\$[\s\S]*?\$\$|\\begin\{(?:align|equation|gather|multline)\*?\}[\s\S]*?"
    r"\\end\{(?:align|equation|gather|multline)\*?\})",
    re.MULTILINE,
)

# Connective text between equations (should be short: "where", "so that", "substituting")
CONNECTIVE_RE = re.compile(r"^(?:where|since|so\s+that|substituting|using|from|thus|hence|therefore|note\s+that|recall|this\s+gives|we\s+(?:get|have|find|obtain))\b", re.IGNORECASE)


class DerivationChunker:
    """Chunk derivation chains as coherent units."""

    def __init__(self, max_tokens: int = 2000, min_equations: int = 2):
        self.max_tokens = max_tokens
        self.min_equations = min_equations

    def extract_derivation_chains(
        self, text: str, source_file: str, section: str, section_path: list[str],
        chunk_id_prefix: str = "",
    ) -> list[Chunk]:
        """Identify and extract derivation chains from text content."""
        chains = self._find_chains(text)
        chunks: list[Chunk] = []

        for i, chain in enumerate(chains):
            chain_text = chain["text"]
            tokens = estimate_tokens(chain_text)

            if tokens < 30:
                continue

            chunk = Chunk(
                chunk_id=f"{chunk_id_prefix}deriv-{i}",
                text=chain_text,
                source_file=source_file,
                section=section,
                section_path=list(section_path),
                chunk_type="derivation",
                equations_referenced=chain.get("eq_refs", []),
                variables_introduced=chain.get("vars", []),
                start_line=0,
                end_line=0,
                token_estimate=tokens,
            )

            # Link chains sequentially
            if chunks:
                chunk.depends_on_chunks.append(chunks[-1].chunk_id)

            chunks.append(chunk)

        return chunks

    def _find_chains(self, text: str) -> list[dict]:
        """Find derivation chains: sequences of display math with connective text."""
        chains: list[dict] = []
        current_chain_parts: list[str] = []
        current_eq_refs: list[str] = []
        current_vars: list[str] = []

        # Split text into alternating segments: text and display math
        segments = DISPLAY_MATH_RE.split(text)
        math_matches = DISPLAY_MATH_RE.findall(text)

        # Interleave: segments[0], math[0], segments[1], math[1], ...
        seg_idx = 0
        math_idx = 0

        all_parts: list[tuple[str, bool]] = []  # (text, is_math)
        for i, seg in enumerate(segments):
            all_parts.append((seg, False))
            if math_idx < len(math_matches):
                all_parts.append((math_matches[math_idx], True))
                math_idx += 1

        # Walk through parts building chains
        in_chain = False
        for part_text, is_math in all_parts:
            if is_math:
                if not in_chain:
                    in_chain = True
                current_chain_parts.append(part_text)
                # Extract equation refs from math block
                refs = re.findall(r"\\label\{([^}]+)\}", part_text)
                current_eq_refs.extend(refs)
                # Extract variable definitions
                var_matches = re.findall(r"\\hat\{([a-zA-Z])\}", part_text)
                current_vars.extend(var_matches)
            elif in_chain:
                stripped = part_text.strip()
                if not stripped:
                    # Empty between equations — continue chain
                    current_chain_parts.append(part_text)
                elif (len(stripped) < 300 and
                      (CONNECTIVE_RE.match(stripped) or
                       stripped.startswith("(") or  # parenthetical note
                       len(stripped.split()) < 20)):
                    # Short connective text — continue chain
                    current_chain_parts.append(part_text)
                else:
                    # Substantial text — end chain, start new potential chain
                    if len([p for p in current_chain_parts if DISPLAY_MATH_RE.match(p)]) >= self.min_equations:
                        chain_text = "".join(current_chain_parts).strip()
                        if estimate_tokens(chain_text) <= self.max_tokens:
                            chains.append({
                                "text": chain_text,
                                "eq_refs": list(set(current_eq_refs)),
                                "vars": list(set(current_vars)),
                            })
                        else:
                            # Chain too large — split in half
                            midpoint = len(current_chain_parts) // 2
                            for half_parts in [
                                current_chain_parts[:midpoint],
                                current_chain_parts[midpoint:],
                            ]:
                                half_text = "".join(half_parts).strip()
                                if half_text:
                                    chains.append({
                                        "text": half_text,
                                        "eq_refs": list(set(current_eq_refs)),
                                        "vars": list(set(current_vars)),
                                    })

                    current_chain_parts = []
                    current_eq_refs = []
                    current_vars = []
                    in_chain = False

        # Flush remaining chain
        if in_chain and len([p for p in current_chain_parts if DISPLAY_MATH_RE.match(p)]) >= self.min_equations:
            chain_text = "".join(current_chain_parts).strip()
            if chain_text:
                chains.append({
                    "text": chain_text,
                    "eq_refs": list(set(current_eq_refs)),
                    "vars": list(set(current_vars)),
                })

        return chains

    def is_derivation_heavy(self, text: str) -> bool:
        """Check if text contains enough display math to warrant derivation chunking."""
        matches = DISPLAY_MATH_RE.findall(text)
        return len(matches) >= self.min_equations
