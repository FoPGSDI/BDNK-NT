"""Code-aware chunker for Wolfram Language files."""

from __future__ import annotations

from ..parsers.wolfram_parser import WolframBlock
from .section_chunker import Chunk, estimate_tokens


class CodeChunker:
    """Chunk Wolfram Language code into function-level units."""

    def __init__(self, max_tokens: int = 800, min_tokens: int = 30):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens

    def chunk_wolfram_blocks(
        self, blocks: list[WolframBlock], file_id: str = ""
    ) -> list[Chunk]:
        """Convert parsed Wolfram blocks into chunks."""
        chunks: list[Chunk] = []

        for block in blocks:
            tokens = estimate_tokens(block.content)

            if tokens < self.min_tokens:
                continue

            # Build a rich text representation: docstring + code
            parts = []
            if block.docstring:
                parts.append(f"Documentation:\n{block.docstring}")
            parts.append(f"Code ({block.source_file}):\n{block.content}")
            text = "\n\n".join(parts)

            safe_name = block.name.replace(" ", "-").replace("/", "-")[:40]
            chunk_id = f"{file_id}-{safe_name}" if file_id else safe_name

            chunk = Chunk(
                chunk_id=chunk_id,
                text=text,
                source_file=block.source_file,
                section=block.name,
                section_path=[block.source_file, block.name],
                chunk_type="code",
                equations_referenced=block.paper_refs,
                related_code=block.dependencies,
                start_line=block.start_line,
                end_line=block.end_line,
                token_estimate=estimate_tokens(text),
            )

            # If too large, split at blank-line boundaries
            if chunk.token_estimate > self.max_tokens:
                sub_chunks = self._split_large_block(chunk, block)
                chunks.extend(sub_chunks)
            else:
                chunks.append(chunk)

        return chunks

    def _split_large_block(self, parent_chunk: Chunk, block: WolframBlock) -> list[Chunk]:
        """Split a large code block at logical boundaries."""
        lines = block.content.split("\n")
        sub_chunks: list[Chunk] = []
        current_lines: list[str] = []
        idx = 0

        for line in lines:
            current_lines.append(line)
            current_text = "\n".join(current_lines)

            if estimate_tokens(current_text) > self.max_tokens and len(current_lines) > 5:
                # Emit chunk
                chunk = Chunk(
                    chunk_id=f"{parent_chunk.chunk_id}-{idx}",
                    text=f"Code ({block.source_file}, {block.name} part {idx + 1}):\n{current_text}",
                    source_file=block.source_file,
                    section=f"{block.name} (part {idx + 1})",
                    section_path=parent_chunk.section_path,
                    chunk_type="code",
                    equations_referenced=block.paper_refs,
                    related_code=block.dependencies,
                    start_line=block.start_line,
                    end_line=block.end_line,
                    token_estimate=estimate_tokens(current_text),
                )
                if sub_chunks:
                    chunk.depends_on_chunks.append(sub_chunks[-1].chunk_id)
                sub_chunks.append(chunk)
                current_lines = []
                idx += 1

        # Flush remaining
        if current_lines:
            current_text = "\n".join(current_lines)
            if estimate_tokens(current_text) >= self.min_tokens:
                chunk = Chunk(
                    chunk_id=f"{parent_chunk.chunk_id}-{idx}",
                    text=f"Code ({block.source_file}, {block.name} part {idx + 1}):\n{current_text}",
                    source_file=block.source_file,
                    section=f"{block.name} (part {idx + 1})",
                    section_path=parent_chunk.section_path,
                    chunk_type="code",
                    equations_referenced=block.paper_refs,
                    related_code=block.dependencies,
                    start_line=block.start_line,
                    end_line=block.end_line,
                    token_estimate=estimate_tokens(current_text),
                )
                if sub_chunks:
                    chunk.depends_on_chunks.append(sub_chunks[-1].chunk_id)
                sub_chunks.append(chunk)

        return sub_chunks if sub_chunks else [parent_chunk]
