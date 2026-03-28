"""Section-aware chunker for markdown and LaTeX documents."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..parsers.markdown_parser import MarkdownSection
from ..parsers.latex_parser import LaTeXSection


@dataclass
class Chunk:
    """A retrieval unit with metadata."""

    chunk_id: str
    text: str
    source_file: str
    section: str
    section_path: list[str]
    chunk_type: str  # "section", "derivation", "code", "reference", "preamble"
    confidence: str | None = None
    equations_referenced: list[str] = field(default_factory=list)
    markers: list[str] = field(default_factory=list)
    variables_introduced: list[str] = field(default_factory=list)
    depends_on_chunks: list[str] = field(default_factory=list)
    related_code: list[str] = field(default_factory=list)
    related_tests: list[str] = field(default_factory=list)
    related_figures: list[str] = field(default_factory=list)
    start_line: int = 0
    end_line: int = 0
    token_estimate: int = 0

    def to_dict(self) -> dict:
        """Serialize to dict for JSON storage."""
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source_file": self.source_file,
            "section": self.section,
            "section_path": self.section_path,
            "chunk_type": self.chunk_type,
            "confidence": self.confidence,
            "equations_referenced": self.equations_referenced,
            "markers": self.markers,
            "variables_introduced": self.variables_introduced,
            "depends_on_chunks": self.depends_on_chunks,
            "related_code": self.related_code,
            "related_tests": self.related_tests,
            "related_figures": self.related_figures,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "token_estimate": self.token_estimate,
        }


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for mixed text/math."""
    return len(text) // 4


# Regex for figure references
FIGURE_REF_RE = re.compile(r"Fig(?:ure)?\.?\s*(\d+)", re.IGNORECASE)

# Regex for LaTeX variable definitions (heuristic)
VAR_DEF_RE = re.compile(
    r"\$\\?(?:hat\{)?([a-zA-Z](?:_[a-zA-Z0-9+\-]+)?)\}?\$\s*(?:=|\\equiv|\\leq|\\geq)"
)


class SectionChunker:
    """Chunk parsed sections respecting token limits."""

    def __init__(self, max_tokens: int = 800, min_tokens: int = 50, overlap_sentences: int = 2):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.overlap_sentences = overlap_sentences

    def chunk_markdown_sections(
        self, sections: list[MarkdownSection], file_id: str = ""
    ) -> list[Chunk]:
        """Convert parsed markdown sections into chunks."""
        chunks: list[Chunk] = []

        for sec in sections:
            sec_chunks = self._chunk_section_content(
                content=sec.content,
                title=sec.title,
                section_path=sec.section_path,
                source_file=sec.source_file,
                confidence=sec.confidence,
                markers=sec.markers,
                equations_referenced=sec.equations_referenced,
                start_line=sec.start_line,
                end_line=sec.end_line,
                file_id=file_id,
            )
            chunks.extend(sec_chunks)

        return chunks

    def chunk_latex_sections(
        self, sections: list[LaTeXSection], file_id: str = ""
    ) -> list[Chunk]:
        """Convert parsed LaTeX sections into chunks."""
        chunks: list[Chunk] = []

        for sec in sections:
            sec_chunks = self._chunk_section_content(
                content=sec.content,
                title=sec.title,
                section_path=sec.section_path,
                source_file=sec.source_file,
                confidence=None,
                markers=[],
                equations_referenced=sec.labels,
                start_line=sec.start_line,
                end_line=sec.end_line,
                file_id=file_id,
            )
            chunks.extend(sec_chunks)

        return chunks

    def _chunk_section_content(
        self,
        content: str,
        title: str,
        section_path: list[str],
        source_file: str,
        confidence: str | None,
        markers: list[str],
        equations_referenced: list[str],
        start_line: int,
        end_line: int,
        file_id: str,
    ) -> list[Chunk]:
        """Split a section's content into appropriately-sized chunks."""
        tokens = estimate_tokens(content)

        if tokens < self.min_tokens:
            return []  # Skip tiny sections

        # Build chunk ID prefix
        safe_title = re.sub(r"[^a-zA-Z0-9]", "-", title.lower())[:40]
        prefix = f"{file_id}-{safe_title}" if file_id else safe_title

        # Extract figure references
        fig_refs = [f"fig{m.group(1)}" for m in FIGURE_REF_RE.finditer(content)]

        # Extract variable definitions
        var_defs = [m.group(1) for m in VAR_DEF_RE.finditer(content)]

        if tokens <= self.max_tokens:
            # Fits in one chunk
            chunk = Chunk(
                chunk_id=f"{prefix}-0",
                text=f"## {title}\n\n{content}" if title else content,
                source_file=source_file,
                section=title,
                section_path=list(section_path),
                chunk_type="section",
                confidence=confidence,
                equations_referenced=equations_referenced,
                markers=markers,
                variables_introduced=var_defs,
                related_figures=fig_refs,
                start_line=start_line,
                end_line=end_line,
                token_estimate=tokens,
            )
            return [chunk]

        # Split at paragraph boundaries
        paragraphs = re.split(r"\n\n+", content)
        chunks: list[Chunk] = []
        current_text = ""
        chunk_idx = 0

        for para in paragraphs:
            para_tokens = estimate_tokens(para)

            if estimate_tokens(current_text) + para_tokens > self.max_tokens and current_text:
                # Emit current chunk
                chunk_text = f"## {title} (part {chunk_idx + 1})\n\n{current_text.strip()}"
                chunk = Chunk(
                    chunk_id=f"{prefix}-{chunk_idx}",
                    text=chunk_text,
                    source_file=source_file,
                    section=title,
                    section_path=list(section_path),
                    chunk_type="section",
                    confidence=confidence,
                    equations_referenced=[
                        r for r in equations_referenced
                        if r in current_text
                    ] or equations_referenced[:3],
                    markers=markers,
                    variables_introduced=[v for v in var_defs if v in current_text],
                    related_figures=[f for f in fig_refs if f in current_text],
                    start_line=start_line,
                    end_line=end_line,
                    token_estimate=estimate_tokens(chunk_text),
                )
                chunks.append(chunk)

                # Overlap: keep last overlap_sentences for context
                if self.overlap_sentences > 0:
                    sentences = re.split(r"(?<=[.!?])\s+", current_text)
                    overlap = " ".join(sentences[-self.overlap_sentences :])
                    current_text = overlap + "\n\n" + para
                else:
                    current_text = para
                chunk_idx += 1
            else:
                current_text = current_text + "\n\n" + para if current_text else para

        # Emit remaining
        if current_text.strip() and estimate_tokens(current_text) >= self.min_tokens:
            chunk_text = (
                f"## {title} (part {chunk_idx + 1})\n\n{current_text.strip()}"
                if chunk_idx > 0
                else f"## {title}\n\n{current_text.strip()}"
            )
            chunk = Chunk(
                chunk_id=f"{prefix}-{chunk_idx}",
                text=chunk_text,
                source_file=source_file,
                section=title,
                section_path=list(section_path),
                chunk_type="section",
                confidence=confidence,
                equations_referenced=equations_referenced,
                markers=markers,
                variables_introduced=[v for v in var_defs if v in current_text],
                related_figures=[f for f in fig_refs if f in current_text],
                start_line=start_line,
                end_line=end_line,
                token_estimate=estimate_tokens(chunk_text),
            )
            chunks.append(chunk)

        # Set dependencies between split chunks
        for i in range(1, len(chunks)):
            chunks[i].depends_on_chunks.append(chunks[i - 1].chunk_id)

        return chunks
