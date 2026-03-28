"""Configuration for the BDNK RAG system."""

from dataclasses import dataclass, field
from pathlib import Path


# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAG_ROOT = Path(__file__).resolve().parent
DATA_DIR = RAG_ROOT / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Corpus source directories
CORPUS_PATHS = {
    "research_notes": [
        PROJECT_ROOT / "mathematical-derivations.md",
        PROJECT_ROOT / "numerical-implementations.md",
        PROJECT_ROOT / "test-results.md",
    ],
    "paper": [PROJECT_ROOT / "paper.tex"],
    "code": list((PROJECT_ROOT / "mathematica").glob("*.wl"))
    if (PROJECT_ROOT / "mathematica").exists()
    else [],
    "progress": list((PROJECT_ROOT / "progress").glob("*.md"))
    if (PROJECT_ROOT / "progress").exists()
    else [],
    "config": [
        PROJECT_ROOT / "CLAUDE.md",
        PROJECT_ROOT / "RESEARCH_NOTE.md",
    ],
    "bibliography": [
        PROJECT_ROOT / "references.bib",
        PROJECT_ROOT / "paperNotes.bib",
    ],
}

# Figure description sources (text descriptions of PDF figures)
FIGURE_DESCRIPTION_SOURCES = list(
    (PROJECT_ROOT / "progress").glob("figure-*.md")
) if (PROJECT_ROOT / "progress").exists() else []


@dataclass
class EmbeddingConfig:
    """Embedding model configuration."""

    provider: str = "voyage"  # "voyage" | "openai" | "local"
    model_name: str = "voyage-3"
    openai_model: str = "text-embedding-3-large"
    local_model: str = "nomic-ai/nomic-embed-text-v1.5"
    batch_size: int = 32
    dimensions: int = 1024


@dataclass
class ChunkingConfig:
    """Chunking parameters."""

    max_tokens: int = 800
    target_tokens: int = 500
    min_tokens: int = 50
    overlap_sentences: int = 2
    max_derivation_tokens: int = 2000


@dataclass
class RetrievalConfig:
    """Retrieval parameters."""

    top_k_semantic: int = 10
    top_k_bm25: int = 10
    top_k_final: int = 8
    rrf_k: int = 60
    chain_expansion_depth: int = 3
    rerank_top_n: int = 15


@dataclass
class GenerationConfig:
    """LLM generation configuration."""

    model: str = "claude-sonnet-4-6-20250514"
    max_tokens: int = 4096
    temperature: float = 0.1
    context_budget_tokens: int = 8000


@dataclass
class RAGConfig:
    """Top-level RAG configuration."""

    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    chroma_collection: str = "bdnk_corpus"


# Singleton config
config = RAGConfig()
