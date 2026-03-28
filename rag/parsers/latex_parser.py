"""LaTeX parser for paper.tex — extracts sections and equations."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LaTeXSection:
    """A parsed section from a LaTeX document."""

    title: str
    level: str  # "section", "subsection", "appendix"
    content: str
    section_path: list[str]
    source_file: str
    start_line: int
    end_line: int
    labels: list[str] = field(default_factory=list)


@dataclass
class LaTeXEquation:
    """An extracted equation with label and context."""

    label: str
    content: str  # raw LaTeX of the equation
    equation_number: str | None = None  # compiled eq number if known
    context: str = ""  # surrounding text
    section: str = ""


class LaTeXParser:
    """Parse LaTeX files into sections and extract equations."""

    SECTION_RE = re.compile(
        r"\\(section|subsection|subsubsection|appendix)\{([^}]+)\}", re.MULTILINE
    )
    LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
    EQUATION_ENV_RE = re.compile(
        r"\\begin\{(equation|align|eqnarray|gather|multline)\*?\}([\s\S]*?)"
        r"\\end\{\1\*?\}",
        re.MULTILINE,
    )
    INLINE_EQ_RE = re.compile(r"\\\((.*?)\\\)", re.DOTALL)
    REF_RE = re.compile(r"\\(?:eq)?ref\{([^}]+)\}")
    CITE_RE = re.compile(r"\\cite\{([^}]+)\}")

    # Commands to strip for plain text extraction
    STRIP_COMMANDS = re.compile(
        r"\\(?:textbf|textit|emph|textrm|mathrm|text)\{([^}]*)\}"
    )
    COMMENT_RE = re.compile(r"(?<!\\)%.*$", re.MULTILINE)

    def parse_file(self, file_path: Path) -> list[LaTeXSection]:
        """Parse a LaTeX file into sections."""
        text = file_path.read_text(encoding="utf-8")
        return self.parse_text(text, source_file=str(file_path.name))

    def parse_text(self, text: str, source_file: str = "") -> list[LaTeXSection]:
        """Parse LaTeX text into sections."""
        # Strip comments
        text_clean = self.COMMENT_RE.sub("", text)
        lines = text_clean.split("\n")

        sections: list[LaTeXSection] = []
        heading_positions: list[tuple[int, str, str]] = []  # (line_idx, level, title)

        for i, line in enumerate(lines):
            m = self.SECTION_RE.search(line)
            if m:
                heading_positions.append((i, m.group(1), m.group(2)))

        if not heading_positions:
            return [
                LaTeXSection(
                    title=source_file,
                    level="document",
                    content=text_clean.strip(),
                    section_path=[source_file],
                    source_file=source_file,
                    start_line=1,
                    end_line=len(lines),
                    labels=self.LABEL_RE.findall(text_clean),
                )
            ]

        path_stack: list[tuple[str, str]] = []
        level_order = ["section", "subsection", "subsubsection", "appendix"]

        for idx, (line_idx, level, title) in enumerate(heading_positions):
            start = line_idx + 1
            end = heading_positions[idx + 1][0] if idx + 1 < len(heading_positions) else len(lines)
            content = "\n".join(lines[start:end]).strip()

            level_rank = level_order.index(level) if level in level_order else 0
            while path_stack and level_order.index(path_stack[-1][0]) >= level_rank:
                path_stack.pop()
            path_stack.append((level, title))
            section_path = [t for _, t in path_stack]

            labels = self.LABEL_RE.findall(content)

            sections.append(
                LaTeXSection(
                    title=title,
                    level=level,
                    content=content,
                    section_path=section_path,
                    source_file=source_file,
                    start_line=line_idx + 1,
                    end_line=end,
                    labels=labels,
                )
            )

        return sections

    def extract_equations(self, text: str) -> list[LaTeXEquation]:
        """Extract all equations from LaTeX text."""
        equations: list[LaTeXEquation] = []

        for m in self.EQUATION_ENV_RE.finditer(text):
            env_type = m.group(1)
            eq_content = m.group(2).strip()

            labels = self.LABEL_RE.findall(eq_content)
            label = labels[0] if labels else f"unlabeled_{m.start()}"

            # Get surrounding context (100 chars before/after)
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(text), m.end() + 200)
            context = text[ctx_start : ctx_end]

            equations.append(
                LaTeXEquation(
                    label=label,
                    content=eq_content,
                    context=self._clean_text(context),
                )
            )

        return equations

    def build_label_map(self, file_path: Path) -> dict[str, str]:
        """Build a mapping from \\label{key} to equation number (from .aux if available)."""
        aux_path = file_path.with_suffix(".aux")
        label_map: dict[str, str] = {}
        if aux_path.exists():
            aux_text = aux_path.read_text(encoding="utf-8", errors="ignore")
            # Pattern: \newlabel{key}{{number}{page}...}
            for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", aux_text):
                label_map[m.group(1)] = m.group(2)
        return label_map

    def _clean_text(self, text: str) -> str:
        """Strip LaTeX commands for plain text representation."""
        text = self.STRIP_COMMANDS.sub(r"\1", text)
        text = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", text)
        text = re.sub(r"\\[a-zA-Z]+", " ", text)
        text = re.sub(r"[{}]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
