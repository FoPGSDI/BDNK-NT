"""FastAPI endpoint for the BDNK RAG system (optional web UI)."""

from __future__ import annotations

from .cli import RAGSystem


def create_app():
    """Create the FastAPI application."""
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
    except ImportError:
        raise ImportError("FastAPI not installed. Run: pip install fastapi uvicorn")

    app = FastAPI(
        title="BDNK RAG API",
        description="Retrieval-Augmented Generation for BDNK viscous relativistic hydrodynamics",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Singleton RAG system
    rag = RAGSystem()

    class QueryRequest(BaseModel):
        question: str
        top_k: int | None = None

    class QueryResponse(BaseModel):
        answer: str
        intent: str
        chunks_used: int

    @app.on_event("startup")
    async def startup():
        rag.initialize()

    @app.post("/query", response_model=QueryResponse)
    async def query_endpoint(request: QueryRequest):
        processed = rag.preprocessor.process(request.question)
        answer = rag.query(request.question, stream=False, top_k=request.top_k)
        return QueryResponse(
            answer=answer,
            intent=processed.intent.value,
            chunks_used=0,
        )

    @app.get("/health")
    async def health():
        return {"status": "ok", "chunks": len(rag.chunk_map)}

    return app


def main():
    """Run the API server."""
    try:
        import uvicorn
    except ImportError:
        raise ImportError("uvicorn not installed. Run: pip install uvicorn")

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
