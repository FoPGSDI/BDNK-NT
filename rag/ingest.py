"""Main ingestion script: parse → chunk → embed → index all documents."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .config import (
    config,
    DATA_DIR,
    CORPUS_PATHS,
    FIGURE_DESCRIPTION_SOURCES,
    PROJECT_ROOT,
)
from .parsers.markdown_parser import MarkdownParser
from .parsers.latex_parser import LaTeXParser
from .parsers.wolfram_parser import WolframParser
from .parsers.bibtex_parser import BibTeXParser
from .chunking.section_chunker import SectionChunker, Chunk
from .chunking.derivation_chunker import DerivationChunker
from .chunking.code_chunker import CodeChunker
from .embedding.bm25_index import BM25Index
from .metadata.equation_index import EquationIndex
from .metadata.cross_ref_graph import CrossRefGraph
from .metadata.figure_index import FigureIndex
from .store.structured_index import StructuredIndex


def parse_and_chunk() -> list[Chunk]:
    """Parse all documents and produce chunks."""
    md_parser = MarkdownParser()
    tex_parser = LaTeXParser()
    wl_parser = WolframParser()
    bib_parser = BibTeXParser()

    section_chunker = SectionChunker(
        max_tokens=config.chunking.max_tokens,
        min_tokens=config.chunking.min_tokens,
        overlap_sentences=config.chunking.overlap_sentences,
    )
    deriv_chunker = DerivationChunker(
        max_tokens=config.chunking.max_derivation_tokens,
    )
    code_chunker = CodeChunker(
        max_tokens=config.chunking.max_tokens,
    )

    all_chunks: list[Chunk] = []

    # --- 1. Research notes (markdown + LaTeX math) ---
    print("Parsing research notes...")
    for fpath in CORPUS_PATHS.get("research_notes", []):
        if not fpath.exists():
            print(f"  SKIP (not found): {fpath.name}")
            continue

        file_id = fpath.stem
        sections = md_parser.parse_file(fpath)
        print(f"  {fpath.name}: {len(sections)} sections")

        # Section-level chunks
        sec_chunks = section_chunker.chunk_markdown_sections(sections, file_id=file_id)

        # Derivation-chain chunks (for math-heavy files)
        deriv_chunks = []
        for sec in sections:
            if deriv_chunker.is_derivation_heavy(sec.content):
                chains = deriv_chunker.extract_derivation_chains(
                    text=sec.content,
                    source_file=sec.source_file,
                    section=sec.title,
                    section_path=sec.section_path,
                    chunk_id_prefix=f"{file_id}-{sec.title[:20]}-",
                )
                deriv_chunks.extend(chains)

        all_chunks.extend(sec_chunks)
        all_chunks.extend(deriv_chunks)
        print(f"    → {len(sec_chunks)} section chunks + {len(deriv_chunks)} derivation chains")

    # --- 2. Original paper (LaTeX) ---
    print("Parsing paper.tex...")
    for fpath in CORPUS_PATHS.get("paper", []):
        if not fpath.exists():
            print(f"  SKIP (not found): {fpath.name}")
            continue

        file_id = "paper"
        sections = tex_parser.parse_file(fpath)
        sec_chunks = section_chunker.chunk_latex_sections(sections, file_id=file_id)
        all_chunks.extend(sec_chunks)
        print(f"  {fpath.name}: {len(sections)} sections → {len(sec_chunks)} chunks")

    # --- 3. Mathematica code ---
    print("Parsing Mathematica code...")
    for fpath in CORPUS_PATHS.get("code", []):
        if not fpath.exists():
            continue

        file_id = fpath.stem
        blocks = wl_parser.parse_file(fpath)
        code_chunks = code_chunker.chunk_wolfram_blocks(blocks, file_id=file_id)
        all_chunks.extend(code_chunks)
        print(f"  {fpath.name}: {len(blocks)} blocks → {len(code_chunks)} chunks")

    # --- 4. Progress/verification docs ---
    print("Parsing progress documents...")
    progress_count = 0
    for fpath in CORPUS_PATHS.get("progress", []):
        if not fpath.exists():
            continue

        file_id = f"progress-{fpath.stem}"
        sections = md_parser.parse_file(fpath)
        sec_chunks = section_chunker.chunk_markdown_sections(sections, file_id=file_id)
        all_chunks.extend(sec_chunks)
        progress_count += len(sec_chunks)

    print(f"  {len(CORPUS_PATHS.get('progress', []))} files → {progress_count} chunks")

    # --- 5. Config docs ---
    print("Parsing config documents...")
    for fpath in CORPUS_PATHS.get("config", []):
        if not fpath.exists():
            continue

        file_id = fpath.stem.lower()
        sections = md_parser.parse_file(fpath)
        sec_chunks = section_chunker.chunk_markdown_sections(sections, file_id=file_id)
        all_chunks.extend(sec_chunks)
        print(f"  {fpath.name}: {len(sec_chunks)} chunks")

    # --- 6. Bibliography ---
    print("Parsing bibliography...")
    for fpath in CORPUS_PATHS.get("bibliography", []):
        if not fpath.exists():
            continue

        entries = bib_parser.parse_file(fpath)
        texts = bib_parser.entries_to_text(entries)
        for i, text in enumerate(texts):
            chunk = Chunk(
                chunk_id=f"bib-{fpath.stem}-{i}",
                text=text,
                source_file=fpath.name,
                section=f"Reference {i+1}",
                section_path=[fpath.name],
                chunk_type="reference",
                token_estimate=len(text) // 4,
            )
            all_chunks.append(chunk)
        print(f"  {fpath.name}: {len(entries)} entries")

    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


def build_indices(chunks: list[Chunk]) -> None:
    """Build all indices: BM25, equation, figure, cross-ref, structured."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save chunks
    print("Saving chunks...")
    chunks_path = DATA_DIR / "chunks.jsonl"
    with open(chunks_path, "w") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk.to_dict()) + "\n")
    print(f"  Saved {len(chunks)} chunks to {chunks_path}")

    # BM25 index
    print("Building BM25 index...")
    bm25 = BM25Index()
    bm25.build(chunks)
    bm25.save(DATA_DIR / "bm25_index.json")
    print(f"  BM25 index: {len(bm25.chunk_ids)} documents")

    # Structured indices
    print("Building structured indices...")
    structured = StructuredIndex()
    structured.build(chunks, figure_description_files=FIGURE_DESCRIPTION_SOURCES)
    structured.save(DATA_DIR)
    print(f"  Equations indexed: {len(structured.equation_index.eq_to_chunks)} refs")
    print(f"  Functions indexed: {len(structured.function_index)} functions")
    print(f"  Parameter chunks: {len(structured.parameter_chunks)}")

    # Cross-reference graph
    print("Building cross-reference graph...")
    graph = CrossRefGraph()
    graph.build(chunks)
    graph.save(DATA_DIR / "cross_ref_graph.json")
    print(f"  Cross-ref graph: {len(graph.edges)} nodes, {len(graph.edge_types)} edges")


def build_embeddings(chunks: list[Chunk]) -> None:
    """Build dense embeddings and populate ChromaDB."""
    from .embedding.embed import Embedder
    from .store.chroma_store import ChromaStore

    print("\nBuilding embeddings...")
    embedder = Embedder()

    try:
        results = embedder.embed_chunks(chunks)
    except Exception as e:
        print(f"  WARNING: Embedding failed ({e}). Skipping vector store.")
        print("  The system will work with BM25 + structured search only.")
        print("  Set VOYAGE_API_KEY or OPENAI_API_KEY to enable dense embeddings.")
        return

    print(f"  Embedded {len(results)} chunks")

    # Populate ChromaDB
    print("Populating ChromaDB...")
    store = ChromaStore()
    store.delete_collection()  # Clean slate

    embeddings = [r["embedding"] for r in results]
    verbalized = [r["verbalized_embedding"] for r in results]

    store.add_chunks(chunks, embeddings, verbalized)
    print(f"  ChromaDB: {store.count()} vectors stored")


def main(skip_embeddings: bool = False):
    """Run the full ingestion pipeline."""
    print("=" * 60)
    print("BDNK RAG Ingestion Pipeline")
    print("=" * 60 + "\n")

    # Step 1: Parse and chunk
    chunks = parse_and_chunk()

    # Step 2: Build indices (BM25, structured, cross-ref)
    build_indices(chunks)

    # Step 3: Build embeddings (optional — requires API key)
    if not skip_embeddings:
        build_embeddings(chunks)
    else:
        print("\nSkipping embeddings (--skip-embeddings flag).")

    print("\n" + "=" * 60)
    print("Ingestion complete!")
    print(f"Data directory: {DATA_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    skip = "--skip-embeddings" in sys.argv
    main(skip_embeddings=skip)
