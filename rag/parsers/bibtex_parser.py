"""BibTeX parser for reference files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BibEntry:
    """A parsed bibliography entry."""

    key: str
    entry_type: str  # article, book, inproceedings, etc.
    title: str
    authors: str
    year: str
    journal: str = ""
    raw: str = ""


class BibTeXParser:
    """Parse BibTeX files into structured records."""

    ENTRY_RE = re.compile(
        r"@(\w+)\{([^,]+),\s*([\s\S]*?)\n\}", re.MULTILINE
    )
    FIELD_RE = re.compile(
        r"(\w+)\s*=\s*\{([^}]*)\}", re.MULTILINE
    )

    def parse_file(self, file_path: Path) -> list[BibEntry]:
        """Parse a .bib file into entries."""
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        return self.parse_text(text)

    def parse_text(self, text: str) -> list[BibEntry]:
        """Parse BibTeX text into entries."""
        entries: list[BibEntry] = []

        for m in self.ENTRY_RE.finditer(text):
            entry_type = m.group(1).lower()
            key = m.group(2).strip()
            body = m.group(3)

            fields: dict[str, str] = {}
            for fm in self.FIELD_RE.finditer(body):
                fields[fm.group(1).lower()] = fm.group(2).strip()

            entries.append(
                BibEntry(
                    key=key,
                    entry_type=entry_type,
                    title=fields.get("title", ""),
                    authors=fields.get("author", ""),
                    year=fields.get("year", ""),
                    journal=fields.get("journal", fields.get("booktitle", "")),
                    raw=m.group(0),
                )
            )

        return entries

    def entries_to_text(self, entries: list[BibEntry]) -> list[str]:
        """Convert entries to searchable text chunks."""
        chunks = []
        for e in entries:
            text = f"[{e.key}] {e.authors} ({e.year}). {e.title}. {e.journal}."
            chunks.append(text.strip())
        return chunks
