"""Parser for Wolfram Language (.wl) source files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class WolframBlock:
    """A parsed block from a Wolfram Language file."""

    block_type: str  # "function", "section_comment", "module", "script_block"
    name: str
    content: str
    source_file: str
    start_line: int
    end_line: int
    docstring: str = ""  # from preceding comment block
    paper_refs: list[str] = field(default_factory=list)  # paper Eq. references
    dependencies: list[str] = field(default_factory=list)  # called functions


class WolframParser:
    """Parse Wolfram Language files into function/section blocks."""

    # Patterns
    SECTION_COMMENT_RE = re.compile(
        r"^\(\*\s*[-=]+\s*\n\s*(.+?)\s*\n\s*[-=]+\s*\*\)", re.MULTILINE
    )
    BLOCK_COMMENT_RE = re.compile(r"\(\*[\s\S]*?\*\)", re.MULTILINE)
    FUNC_DEF_RE = re.compile(
        r"^(\w+)\s*\[([^\]]*)\]\s*:=", re.MULTILINE
    )
    PAPER_REF_RE = re.compile(
        r"(?:paper|Eq\.?|Eqs\.?|equation)\s*\(?([A-Z]?\d+(?:\s*[-–,]\s*[A-Z]?\d+)*)\)?",
        re.IGNORECASE,
    )
    GET_RE = re.compile(r'Get\["([^"]+)"\]')
    FUNC_CALL_RE = re.compile(r"(\w{2,})\s*\[")

    def parse_file(self, file_path: Path) -> list[WolframBlock]:
        """Parse a .wl file into blocks."""
        text = file_path.read_text(encoding="utf-8")
        return self.parse_text(text, source_file=str(file_path.name))

    def parse_text(self, text: str, source_file: str = "") -> list[WolframBlock]:
        """Parse Wolfram Language text into blocks."""
        lines = text.split("\n")
        blocks: list[WolframBlock] = []

        # Strategy: find section comments and function definitions as split points
        split_points: list[tuple[int, str, str]] = []  # (line, type, name)

        # Find section-style comments: (* === Section Name === *)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r"^\(\*\s*[-=]{3,}", stripped):
                # Look for section title in next few lines
                title_lines = []
                j = i
                while j < len(lines) and "*)" not in lines[j]:
                    title_lines.append(lines[j])
                    j += 1
                if j < len(lines):
                    title_lines.append(lines[j])
                block_text = "\n".join(title_lines)
                # Extract title
                clean = re.sub(r"[\(\*\)=\-]", "", block_text).strip()
                title = clean.split("\n")[0].strip() if clean else f"Section at line {i+1}"
                if title:
                    split_points.append((i, "section_comment", title))

        # Find function definitions
        for i, line in enumerate(lines):
            m = self.FUNC_DEF_RE.match(line)
            if m:
                func_name = m.group(1)
                # Skip Mathematica built-ins and very short names
                if len(func_name) > 1 and func_name[0].islower():
                    split_points.append((i, "function", func_name))

        # Sort by line number
        split_points.sort(key=lambda x: x[0])

        if not split_points:
            # No structure found — return whole file as one block
            blocks.append(
                self._build_block(
                    block_type="script_block",
                    name=source_file,
                    content=text,
                    source_file=source_file,
                    start_line=1,
                    end_line=len(lines),
                    preceding_comment="",
                )
            )
            return blocks

        # Extract blocks between split points
        for idx, (line_idx, btype, name) in enumerate(split_points):
            end = split_points[idx + 1][0] if idx + 1 < len(split_points) else len(lines)
            content = "\n".join(lines[line_idx:end]).strip()

            # Look for preceding comment block (docstring)
            docstring = ""
            if line_idx > 0:
                doc_lines = []
                j = line_idx - 1
                while j >= 0 and (lines[j].strip().startswith("(*") or
                                   lines[j].strip().endswith("*)") or
                                   (doc_lines and not lines[j].strip())):
                    doc_lines.insert(0, lines[j])
                    if lines[j].strip().startswith("(*"):
                        break
                    j -= 1
                if doc_lines:
                    docstring = "\n".join(doc_lines).strip()

            blocks.append(
                self._build_block(
                    block_type=btype,
                    name=name,
                    content=content,
                    source_file=source_file,
                    start_line=line_idx + 1,
                    end_line=end,
                    preceding_comment=docstring,
                )
            )

        return blocks

    def _build_block(
        self,
        block_type: str,
        name: str,
        content: str,
        source_file: str,
        start_line: int,
        end_line: int,
        preceding_comment: str,
    ) -> WolframBlock:
        """Build a WolframBlock with extracted metadata."""
        # Extract paper references
        paper_refs = []
        for m in self.PAPER_REF_RE.finditer(content):
            paper_refs.append(m.group(1).strip())
        for m in self.PAPER_REF_RE.finditer(preceding_comment):
            paper_refs.append(m.group(1).strip())

        # Extract function calls (dependencies)
        # Remove comments first
        code_only = self.BLOCK_COMMENT_RE.sub("", content)
        called_funcs = set()
        for m in self.FUNC_CALL_RE.finditer(code_only):
            fn = m.group(1)
            # Filter out Mathematica builtins (capitalized) and self
            if fn[0].islower() and fn != name and len(fn) > 2:
                called_funcs.add(fn)

        return WolframBlock(
            block_type=block_type,
            name=name,
            content=content,
            source_file=source_file,
            start_line=start_line,
            end_line=end_line,
            docstring=preceding_comment,
            paper_refs=list(set(paper_refs)),
            dependencies=sorted(called_funcs),
        )

    def extract_imports(self, text: str) -> list[str]:
        """Extract Get[] imports from a file."""
        return self.GET_RE.findall(text)
