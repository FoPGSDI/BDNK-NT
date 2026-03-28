"""Evaluation framework: measure retrieval and generation quality."""

from __future__ import annotations

import json
from pathlib import Path

from ..config import DATA_DIR
from ..interface.cli import RAGSystem
from ..retrieval.query_preprocessor import QueryPreprocessor


def load_test_queries(path: Path | None = None) -> list[dict]:
    """Load the benchmark test queries."""
    path = path or Path(__file__).parent / "test_queries.json"
    return json.loads(path.read_text())


def evaluate_retrieval(rag: RAGSystem, test_queries: list[dict]) -> dict:
    """Evaluate retrieval quality: source precision and section recall."""
    rag.initialize()
    preprocessor = QueryPreprocessor()

    results = []
    total_source_hits = 0
    total_source_expected = 0
    total_keyword_hits = 0
    total_keyword_expected = 0

    for tq in test_queries:
        query = tq["query"]
        expected_sources = tq.get("expected_sources", [])
        expected_keywords = tq.get("expected_answer_contains", [])

        # Run retrieval only (no generation)
        processed = preprocessor.process(query)

        from ..retrieval.hybrid_retriever import HybridRetriever
        from ..retrieval.reranker import Reranker

        retriever = HybridRetriever(
            rag.chroma, rag.bm25, rag.structured, rag.embedder
        )
        candidates = retriever.retrieve(processed, top_k=10)
        reranker = Reranker(rag.chunk_map, use_cross_encoder=False)
        ranked = reranker.rerank(processed, candidates, top_n=8)

        # Check if expected sources appear in retrieved chunks
        retrieved_sources = set()
        retrieved_text = ""
        for r in ranked:
            cid = r["chunk_id"]
            chunk = rag.chunk_map.get(cid)
            if chunk:
                retrieved_sources.add(chunk.source_file)
                retrieved_text += " " + chunk.text

        source_hits = sum(
            1 for s in expected_sources
            if any(s in rs for rs in retrieved_sources)
        )
        total_source_hits += source_hits
        total_source_expected += len(expected_sources)

        # Check if expected keywords appear in retrieved text
        keyword_hits = sum(
            1 for kw in expected_keywords
            if kw.lower() in retrieved_text.lower()
        )
        total_keyword_hits += keyword_hits
        total_keyword_expected += len(expected_keywords)

        results.append({
            "id": tq["id"],
            "query": query,
            "intent": processed.intent.value,
            "source_precision": source_hits / max(len(expected_sources), 1),
            "keyword_recall": keyword_hits / max(len(expected_keywords), 1),
            "retrieved_sources": list(retrieved_sources),
            "num_chunks": len(ranked),
        })

    summary = {
        "total_queries": len(test_queries),
        "avg_source_precision": total_source_hits / max(total_source_expected, 1),
        "avg_keyword_recall": total_keyword_hits / max(total_keyword_expected, 1),
        "per_query": results,
    }

    return summary


def print_eval_report(summary: dict) -> None:
    """Pretty-print the evaluation report."""
    print("=" * 60)
    print("BDNK RAG Evaluation Report")
    print("=" * 60)
    print(f"\nTotal queries: {summary['total_queries']}")
    print(f"Avg source precision: {summary['avg_source_precision']:.2%}")
    print(f"Avg keyword recall:   {summary['avg_keyword_recall']:.2%}")
    print("\nPer-query results:")
    print("-" * 60)

    for r in summary["per_query"]:
        status = "PASS" if r["source_precision"] >= 0.5 and r["keyword_recall"] >= 0.5 else "FAIL"
        print(f"  [{status}] Q{r['id']}: {r['query'][:50]}...")
        print(f"         Intent: {r['intent']}, Sources: {r['source_precision']:.0%}, Keywords: {r['keyword_recall']:.0%}")
        print(f"         Retrieved from: {', '.join(r['retrieved_sources'][:3])}")

    print("\n" + "=" * 60)


def main():
    """Run the evaluation."""
    test_queries = load_test_queries()
    rag = RAGSystem()
    summary = evaluate_retrieval(rag, test_queries)
    print_eval_report(summary)

    # Save results
    output_path = DATA_DIR / "eval_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2))
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
