"""Section-aware markdown parser that preserves LaTeX math blocks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MarkdownSection:
    """A parsed section from a markdown document."""

    title: str
    level: int  # heading level (1-6)
    content: str  # raw content including LaTeX
    section_path: list[str]  # e.g. ["5. Hydrodynamic frame", "5.2 Characteristic speeds"]
    source_file: str
    start_line: int
    end_line: int
    confidence: str | None = None  # [SOLID], [PRELIMINARY], [HYPOTHESIS]
    markers: list[str] = field(default_factory=list)  # [BLOCKING], [FUTURE], etc.
    equations_referenced: list[str] = field(default_factory=list)  # paper Eq. refs


class MarkdownParser:
    """Parse markdown files into hierarchical sections preserving LaTeX."""

    # Regex patterns
    HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    CONFIDENCE_RE = re.compile(r"\[(SOLID|PRELIMINARY|HYPOTHESIS)\]")
    MARKER_RE = re.compile(r"\[(BLOCKING[^\]]*|FUTURE[^\]]*)\]")
    EQUATION_REF_RE = re.compile(
        r"\(ref:\s*paper\s+Eq\.?\s*([^)]+)\)|"
        r"(?:paper\s+)?[Ee]q(?:uation)?s?\.?\s*\(?([A-Z]?\d+(?:\s*[-–]\s*[A-Z]?\d+)?)\)?"
    )
    LATEX_BLOCK_RE = re.compile(r"\$\$[\s\S]*?\$\$", re.MULTILINE)
    LATEX_INLINE_RE = re.compile(r"\$[^$\n]+?\$")

    def parse_file(self, file_path: Path) -> list[MarkdownSection]:
        """Parse a markdown file into sections."""
        text = file_path.read_text(encoding="utf-8")
        return self.parse_text(text, source_file=str(file_path.name))

    def parse_text(self, text: str, source_file: str = "") -> list[MarkdownSection]:
        """Parse markdown text into sections."""
        lines = text.split("\n")
        sections: list[MarkdownSection] = []
        heading_positions: list[tuple[int, int, str]] = []  # (line_idx, level, title)

        # Find all headings
        for i, line in enumerate(lines):
            m = self.HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                heading_positions.append((i, level, title))

        if not heading_positions:
            # No headings — treat entire file as one section
            content = text.strip()
            if content:
                section = self._build_section(
                    title=source_file,
                    level=0,
                    content=content,
                    section_path=[source_file],
                    source_file=source_file,
                    start_line=1,
                    end_line=len(lines),
                )
                sections.append(section)
            return sections

        # Extract preamble before first heading
        if heading_positions[0][0] > 0:
            preamble = "\n".join(lines[: heading_positions[0][0]]).strip()
            if preamble:
                section = self._build_section(
                    title="Preamble",
                    level=0,
                    content=preamble,
                    section_path=["Preamble"],
                    source_file=source_file,
                    start_line=1,
                    end_line=heading_positions[0][0],
                )
                sections.append(section)

        # Build section path stack
        path_stack: list[tuple[int, str]] = []  # (level, title)

        for idx, (line_idx, level, title) in enumerate(heading_positions):
            # Determine content range
            start = line_idx + 1
            if idx + 1 < len(heading_positions):
                end = heading_positions[idx + 1][0]
            else:
                end = len(lines)

            content = "\n".join(lines[start:end]).strip()

            # Update path stack
            while path_stack and path_stack[-1][0] >= level:
                path_stack.pop()
            path_stack.append((level, title))
            section_path = [t for _, t in path_stack]

            section = self._build_section(
                title=title,
                level=level,
                content=content,
                section_path=section_path,
                source_file=source_file,
                start_line=line_idx + 1,
                end_line=end,
            )
            sections.append(section)

        return sections

    def _build_section(
        self,
        title: str,
        level: int,
        content: str,
        section_path: list[str],
        source_file: str,
        start_line: int,
        end_line: int,
    ) -> MarkdownSection:
        """Build a MarkdownSection with extracted metadata."""
        # Extract confidence markers
        confidence = None
        conf_match = self.CONFIDENCE_RE.search(content)
        if conf_match:
            confidence = conf_match.group(1)

        # Extract other markers
        markers = [m.group(0) for m in self.MARKER_RE.finditer(content)]

        # Extract equation references
        eq_refs: list[str] = []
        for m in self.EQUATION_REF_RE.finditer(content):
            ref = m.group(1) or m.group(2)
            if ref:
                eq_refs.append(ref.strip())

        return MarkdownSection(
            title=title,
            level=level,
            content=content,
            section_path=section_path,
            source_file=source_file,
            start_line=start_line,
            end_line=end_line,
            confidence=confidence,
            markers=markers,
            equations_referenced=list(set(eq_refs)),
        )

    def extract_latex_blocks(self, text: str) -> list[str]:
        """Extract all LaTeX math blocks (both display and inline)."""
        blocks = self.LATEX_BLOCK_RE.findall(text)
        inlines = self.LATEX_INLINE_RE.findall(text)
        return blocks + inlines

    def has_derivation_chain(self, content: str) -> bool:
        """Detect if content contains a derivation chain (multiple display equations)."""
        display_blocks = self.LATEX_BLOCK_RE.findall(content)
        return len(display_blocks) >= 2
