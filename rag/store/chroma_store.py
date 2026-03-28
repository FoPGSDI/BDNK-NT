"""ChromaDB vector store for chunk embeddings."""

from __future__ import annotations

from pathlib import Path

from ..chunking.section_chunker import Chunk
from ..config import config, CHROMA_DIR


class ChromaStore:
    """Manages ChromaDB collection for semantic search."""

    def __init__(
        self,
        collection_name: str | None = None,
        persist_dir: Path | None = None,
    ):
        self.collection_name = collection_name or config.chroma_collection
        self.persist_dir = persist_dir or CHROMA_DIR
        self._client = None
        self._collection = None

    def _init_client(self):
        """Lazy-initialize ChromaDB client."""
        if self._client is not None:
            return

        import chromadb

        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.persist_dir))

    def _get_collection(self):
        """Get or create the collection."""
        if self._collection is not None:
            return self._collection

        self._init_client()
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        return self._collection

    def add_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
        verbalized_embeddings: list[list[float]] | None = None,
    ) -> None:
        """Add chunks with their embeddings to the store."""
        collection = self._get_collection()

        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = [
            {
                "source_file": c.source_file,
                "section": c.section,
                "section_path": "|".join(c.section_path),
                "chunk_type": c.chunk_type,
                "confidence": c.confidence or "unknown",
                "equations": ",".join(c.equations_referenced[:10]),
                "figures": ",".join(c.related_figures[:5]),
                "token_estimate": c.token_estimate,
            }
            for c in chunks
        ]

        # Add primary embeddings
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        # Add verbalized embeddings as separate entries with prefix
        if verbalized_embeddings:
            verb_collection = self._client.get_or_create_collection(
                name=f"{self.collection_name}_verbalized",
                metadata={"hnsw:space": "cosine"},
            )
            verb_collection.add(
                ids=[f"verb_{cid}" for cid in ids],
                embeddings=verbalized_embeddings,
                documents=documents,
                metadatas=metadatas,
            )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 10,
        where: dict | None = None,
    ) -> list[dict]:
        """Search for similar chunks.

        Returns list of {chunk_id, text, metadata, distance}.
        """
        collection = self._get_collection()

        kwargs: dict = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = collection.query(**kwargs)

        hits: list[dict] = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                hits.append({
                    "chunk_id": chunk_id,
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })

        return hits

    def search_verbalized(
        self,
        query_embedding: list[float],
        top_k: int = 10,
    ) -> list[dict]:
        """Search the verbalized-math collection."""
        self._init_client()
        try:
            verb_collection = self._client.get_collection(
                name=f"{self.collection_name}_verbalized"
            )
        except Exception:
            return []

        results = verb_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        hits: list[dict] = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                # Strip verb_ prefix to get original chunk_id
                original_id = chunk_id.removeprefix("verb_")
                hits.append({
                    "chunk_id": original_id,
                    "text": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })

        return hits

    def delete_collection(self) -> None:
        """Delete the collection (for re-indexing)."""
        self._init_client()
        try:
            self._client.delete_collection(self.collection_name)
        except Exception:
            pass
        try:
            self._client.delete_collection(f"{self.collection_name}_verbalized")
        except Exception:
            pass
        self._collection = None

    def count(self) -> int:
        """Return number of items in collection."""
        collection = self._get_collection()
        return collection.count()
