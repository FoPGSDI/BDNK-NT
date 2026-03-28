"""Command-line interface for the BDNK RAG system."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ..config import config, DATA_DIR
from ..chunking.section_chunker import Chunk
from ..embedding.embed import Embedder
from ..embedding.bm25_index import BM25Index
from ..store.chroma_store import ChromaStore
from ..store.structured_index import StructuredIndex
from ..metadata.cross_ref_graph import CrossRefGraph
from ..retrieval.query_preprocessor import QueryPreprocessor
from ..retrieval.hybrid_retriever import HybridRetriever
from ..retrieval.chain_expander import ChainExpander
from ..retrieval.reranker import Reranker
from ..generation.context_assembler import ContextAssembler
from ..generation.generator import Generator


class RAGSystem:
    """Full RAG pipeline: query -> retrieve -> generate."""

    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or DATA_DIR
        self._initialized = False

        # Components (lazy-loaded)
        self.chunk_map: dict[str, Chunk] = {}
        self.embedder: Embedder | None = None
        self.chroma: ChromaStore | None = None
        self.bm25: BM25Index | None = None
        self.structured: StructuredIndex | None = None
        self.cross_ref: CrossRefGraph | None = None
        self.preprocessor = QueryPreprocessor()
        self.generator: Generator | None = None

    def initialize(self) -> None:
        """Load all indices and initialize components."""
        if self._initialized:
            return

        print("Loading RAG system...")

        # Load chunks
        chunks_path = self.data_dir / "chunks.jsonl"
        if chunks_path.exists():
            self.chunk_map = {}
            for line in chunks_path.read_text().strip().split("\n"):
                if line:
                    data = json.loads(line)
                    chunk = Chunk(**{k: v for k, v in data.items() if k != "to_dict"})
                    self.chunk_map[chunk.chunk_id] = chunk
            print(f"  Loaded {len(self.chunk_map)} chunks")
        else:
            print(f"  WARNING: No chunks found at {chunks_path}. Run ingest.py first.")
            return

        # Load embedder
        self.embedder = Embedder()

        # Load ChromaDB
        self.chroma = ChromaStore()
        count = self.chroma.count()
        print(f"  ChromaDB: {count} vectors")

        # Load BM25
        self.bm25 = BM25Index()
        bm25_path = self.data_dir / "bm25_index.json"
        if bm25_path.exists():
            self.bm25.load(bm25_path)
            print(f"  BM25: {len(self.bm25.chunk_ids)} documents")

        # Load structured indices
        self.structured = StructuredIndex()
        self.structured.load(self.data_dir)
        print("  Structured indices loaded")

        # Load cross-ref graph
        self.cross_ref = CrossRefGraph()
        graph_path = self.data_dir / "cross_ref_graph.json"
        if graph_path.exists():
            self.cross_ref.load(graph_path)
            print(f"  Cross-ref graph: {len(self.cross_ref.edges)} nodes")

        # Initialize generator
        self.generator = Generator()

        self._initialized = True
        print("RAG system ready.\n")

    def query(self, question: str, stream: bool = True, top_k: int | None = None) -> str:
        """Run the full RAG pipeline on a question."""
        self.initialize()

        if not self.chunk_map:
            return "Error: No chunks loaded. Run `python -m rag.ingest` first."

        # 1. Preprocess query
        processed = self.preprocessor.process(question)
        print(f"Intent: {processed.intent.value}")
        if processed.equation_refs:
            print(f"Equations: {processed.equation_refs}")
        if processed.figure_refs:
            print(f"Figures: {processed.figure_refs}")

        # 2. Hybrid retrieval
        retriever = HybridRetriever(
            self.chroma, self.bm25, self.structured, self.embedder
        )
        candidates = retriever.retrieve(processed, top_k=(top_k or config.retrieval.top_k_final) * 2)

        # 3. Re-rank
        reranker = Reranker(self.chunk_map, use_cross_encoder=False)
        ranked = reranker.rerank(processed, candidates)

        # 4. Chain expansion
        expander = ChainExpander(self.chunk_map, self.cross_ref)
        expanded_ids = expander.expand([r["chunk_id"] for r in ranked[:top_k or config.retrieval.top_k_final]])

        print(f"Retrieved {len(expanded_ids)} chunks (after expansion)\n")

        # 5. Assemble context
        assembler = ContextAssembler(self.chunk_map)
        prompt_data = assembler.assemble(processed, expanded_ids)

        # 6. Generate
        response = self.generator.generate(
            system_prompt=prompt_data["system_prompt"],
            context_text=prompt_data["context_text"],
            user_message=prompt_data["user_message"],
            stream=stream,
        )

        return response or ""


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="BDNK RAG System")
    parser.add_argument("query", nargs="?", help="Question to ask")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--top-k", type=int, default=None, help="Number of chunks to retrieve")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming output")
    args = parser.parse_args()

    rag = RAGSystem()

    if args.interactive or not args.query:
        print("BDNK RAG System — Interactive Mode")
        print("Type your question, or 'quit' to exit.\n")

        rag.initialize()

        while True:
            try:
                question = input("Q: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye.")
                break

            if not question or question.lower() in ("quit", "exit", "q"):
                break

            print()
            rag.query(question, stream=not args.no_stream, top_k=args.top_k)
            print("\n" + "=" * 60 + "\n")
    else:
        rag.query(args.query, stream=not args.no_stream, top_k=args.top_k)


if __name__ == "__main__":
    main()
