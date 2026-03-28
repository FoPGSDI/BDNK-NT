# RAG System Plan — BDNK Viscous Relativistic Hydrodynamics

## 1. Objective

Transform this research workspace into a **Retrieval-Augmented Generation (RAG)** system that enables:

- Natural language Q&A over the full corpus (derivations, numerics, tests, code, paper)
- Cross-referencing between mathematical theory, numerical implementation, and test validation
- Equation-aware retrieval (query by physics concept → retrieve relevant LaTeX derivations)
- Code-grounded answers (query about a method → retrieve both the math and the Mathematica implementation)
- Provenance tracking (every generated answer cites source document, section, and equation numbers)

---

## 2. Corpus Inventory

### 2.1 Document Classes

| Class | Files | Size | Content Type | Chunking Challenge |
|-------|-------|------|--------------|-------------------|
| **Research notes** | `mathematical-derivations.md` (121 KB), `numerical-implementations.md` (43 KB), `test-results.md` (65 KB) | ~230 KB | Markdown + LaTeX math | Long derivation chains; must preserve equation continuity |
| **Original paper** | `paper.tex` (123 KB) | 123 KB | LaTeX | Dense cross-refs; equation labels |
| **Mathematica code** | 8 `.wl` files in `mathematica/` (~3800 lines) | ~140 KB | Wolfram Language | Function dependencies across files; inline comments reference paper eqs |
| **Progress/verification** | 35 files in `progress/` | ~150 KB | Markdown | Mostly procedural; valuable for "why" questions |
| **Project config** | `CLAUDE.md`, `RESEARCH_NOTE.md`, `input-*.md` | ~10 KB | Markdown | Small, load fully |
| **Figures** | 7 original PDFs + 11 generated PDFs | ~1.2 MB | PDF (vector graphics) | Visual content; needs caption/description metadata |
| **Bibliography** | `references.bib`, `paperNotes.bib` | ~69 KB | BibTeX | Structured data; parse into records |

### 2.2 Total Corpus

- **Text corpus:** ~650 KB across ~50 files
- **Figures:** 18 PDFs (visual, not text-indexed — use descriptions from `test-results.md` and `progress/figure-*.md`)
- **Estimated chunks** (at ~500 token target): ~800–1200 chunks

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User Query                        │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Query Preprocessor                      │
│  - Detect math symbols → normalize to LaTeX         │
│  - Classify intent: derivation / numerical /        │
│    code / test / conceptual                         │
│  - Extract key entities: equation refs, parameters, │
│    figure numbers, function names                   │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
┌─────────────────┐    ┌─────────────────────────────┐
│ Semantic Search  │    │  Structured Lookup          │
│ (Vector DB)      │    │  - Eq ref → section map     │
│                  │    │  - Figure → description map  │
│ Dense embeddings │    │  - Function → file:line map  │
│ over all chunks  │    │  - Parameter → Table II row  │
└────────┬────────┘    └──────────────┬───────────────┘
         │                            │
         └────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                 Re-ranker                            │
│  - Cross-encoder scoring                            │
│  - Boost: same-section chunks (derivation chains)   │
│  - Boost: code + math co-occurrence                 │
│  - Deduplicate overlapping chunks                   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Context Assembly                        │
│  - Top-k chunks (k=5–10)                            │
│  - Expand to include adjacent chunks when           │
│    derivation chain is detected                     │
│  - Attach metadata: source file, section, eqs       │
│  - Include conventions.md as system context         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              LLM Generation                          │
│  - System prompt: notation conventions, markers     │
│  - Retrieved context injected                       │
│  - Instruction: cite sources, use LaTeX, flag       │
│    [PRELIMINARY] vs [SOLID] confidence              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Response + Citations                     │
└─────────────────────────────────────────────────────┘
```

---

## 4. Document Processing Pipeline

### 4.1 Parsing

| Source | Parser | Output |
|--------|--------|--------|
| `.md` files | Custom markdown parser preserving LaTeX `$...$` and `$$...$$` blocks intact | Structured sections with metadata |
| `paper.tex` | LaTeX parser (e.g., `tex2txt` + custom equation extractor) | Text + equation index |
| `.wl` files | Line-based parser; detect `(* comment *)` blocks, function definitions, `Get[]` imports | Code chunks with docstrings |
| `.bib` files | BibTeX parser → structured records | Author/title/year tuples |
| `.pdf` figures | Skip OCR; use existing text descriptions from `progress/figure-*.md` and `test-results.md` | Caption + description text |

### 4.2 Chunking Strategy

The central challenge: **mathematical derivations are sequential chains where context from earlier steps is essential to understand later steps.** Naive fixed-size chunking destroys this.

#### Strategy: Hierarchical Section-Aware Chunking

**Level 1 — Section chunks** (primary retrieval unit):
- Split on `## ` and `### ` headers in markdown
- Each section becomes one chunk (typical size: 200–800 tokens)
- Sections exceeding 1000 tokens → split at paragraph boundaries, with 2-sentence overlap

**Level 2 — Derivation-chain chunks** (for `mathematical-derivations.md`):
- Identify derivation blocks: sequences of `$$...$$` separated by connective text
- Keep each derivation chain as a single chunk (may be 500–2000 tokens)
- Tag with: starting equation, ending equation, variables introduced
- Store parent section ID for chain expansion

**Level 3 — Code function chunks** (for `.wl` files):
- Split at function definitions (detect `funcName[args_] := ...`)
- Include preceding comment block as chunk header
- Tag with: function name, paper equation reference (from comments), dependencies

**Level 4 — Cross-reference overlay**:
- Build a graph linking chunks by:
  - Equation references: `(ref: paper Eq. XX)` → link to paper section
  - Function calls: `transportCoeffs[]` in code → link to `bdnk_common.wl` definition
  - Figure references: `Fig. N` → link to figure description chunk
  - Parameter references: `σ̂`, `τ̂` → link to parameter table chunk

### 4.3 Metadata per Chunk

```json
{
  "chunk_id": "math-deriv-sec5.2-chunk3",
  "source_file": "mathematical-derivations.md",
  "section": "5.2 Characteristic speeds",
  "section_path": ["5. Hydrodynamic frame", "5.2 Characteristic speeds"],
  "confidence": "SOLID",
  "equations_referenced": ["A26", "A27", "29"],
  "variables_introduced": ["c_+", "c_-", "c_1"],
  "depends_on_chunks": ["math-deriv-sec5.1-chunk2"],
  "related_code": ["bdnk_common.wl:charSpeeds"],
  "related_tests": ["test-results-sec5"],
  "related_figures": ["fig4"],
  "chunk_type": "derivation",
  "token_count": 650
}
```

---

## 5. Embedding & Indexing

### 5.1 Embedding Model

**Recommended:** `text-embedding-3-large` (OpenAI) or `voyage-3` (Voyage AI)

**Why:** Both handle mixed natural language + LaTeX math well. Voyage-3 has shown strong performance on scientific text retrieval.

**Fallback/local:** `nomic-embed-text-v1.5` (open-source, runs locally, 8192 token context)

### 5.2 Special Handling for Math

LaTeX equations are semantically dense but lexically unusual for general embeddings. Mitigation:

1. **Dual representation:** Each chunk containing math gets embedded twice:
   - Raw form (LaTeX preserved): for users who query with math notation
   - Verbalized form: `$c_+^2 = ...$` → "the square of the positive characteristic speed c-plus equals..." for natural language queries

2. **Equation index:** Separate lookup table mapping equation numbers (paper Eq. 14, Eq. A26, etc.) directly to chunks — bypasses embedding entirely for reference queries.

### 5.3 Vector Store

**Recommended:** ChromaDB (local, lightweight, Python) or Qdrant (if scaling needed)

**Index structure:**
- Primary collection: all chunks with dense embeddings
- Metadata filters: `source_file`, `chunk_type`, `confidence`, `section_path`
- Payload: full chunk text + metadata JSON

---

## 6. Retrieval Strategy

### 6.1 Hybrid Retrieval

Combine three retrieval paths:

| Path | Method | Best For |
|------|--------|----------|
| **Semantic** | Dense vector similarity (cosine) | Conceptual questions ("What is the BDNK stability condition?") |
| **Keyword** | BM25 over chunk text | Specific terms ("Rankine-Hugoniot", "minmod limiter") |
| **Structured** | Direct lookup in metadata indices | Equation refs ("Eq. 29"), figure refs ("Fig. 4"), function names |

**Fusion:** Reciprocal Rank Fusion (RRF) to merge results from all three paths.

### 6.2 Derivation Chain Expansion

When a retrieved chunk is part of a derivation chain:
1. Check `depends_on_chunks` metadata
2. If the dependency is not already in retrieved set, pull it in
3. Order chunks by derivation sequence before injecting into context

This ensures the LLM sees the logical flow, not isolated equations.

### 6.3 Cross-Document Linking

When a query touches multiple document classes (e.g., "How is the shockwave ODE solved numerically?"):
1. Retrieve from `mathematical-derivations.md` (the ODE derivation)
2. Retrieve from `numerical-implementations.md` (the algorithm)
3. Retrieve from `mathematica/shockwave_steady.wl` (the code)
4. Retrieve from `test-results.md` (the validation)

The re-ranker boosts multi-class coverage to ensure comprehensive answers.

---

## 7. Generation Pipeline

### 7.1 System Prompt Template

```
You are a research assistant for BDNK viscous relativistic hydrodynamics.
You have access to retrieved context from the research corpus.

Notation conventions: (injected from progress/conventions.md)

Rules:
- Use LaTeX math notation with $...$ delimiters
- Cite sources as [source_file, Section X.Y]
- Mark confidence: [SOLID], [PRELIMINARY], or [HYPOTHESIS]
- If the retrieved context is insufficient, say so explicitly
- Reference paper equations as (ref: paper Eq. XX)
- When showing derivations, show every step — no skipping
```

### 7.2 Context Window Budget

Assuming Claude with 200K context:

| Component | Token Budget |
|-----------|-------------|
| System prompt + conventions | ~500 |
| Retrieved chunks (top-k) | ~4000–8000 |
| User query + history | ~1000 |
| Generation headroom | ~remaining |

At ~500 tokens per chunk, retrieve **k=8–15 chunks** depending on query complexity.

### 7.3 Answer Types

| Query Type | Retrieval Focus | Generation Style |
|------------|-----------------|------------------|
| "Derive X" | Derivation chain chunks | Step-by-step with LaTeX |
| "How is X implemented?" | Code + numerical-implementations chunks | Pseudocode + actual code snippets |
| "What does Fig N show?" | Figure description + test-results chunks | Structured interpretation |
| "What parameters for test X?" | Parameter table chunk | Tabular answer |
| "Why does X happen?" | Multiple document classes | Synthesized explanation with citations |

---

## 8. Implementation Plan

### Phase 1: Document Processing & Chunking (Core)

**Deliverables:**
- `rag/parsers/` — Parsers for each document type
  - `markdown_parser.py` — Section-aware markdown + LaTeX splitter
  - `latex_parser.py` — paper.tex equation extractor + section splitter
  - `wolfram_parser.py` — .wl function/comment block extractor
  - `bibtex_parser.py` — Bibliography record parser
- `rag/chunking/` — Chunking strategies
  - `section_chunker.py` — Hierarchical section-based chunking
  - `derivation_chunker.py` — Math derivation chain detection
  - `code_chunker.py` — Function-level code chunking
- `rag/metadata/` — Metadata extraction
  - `equation_index.py` — Build equation → chunk mapping
  - `cross_ref_graph.py` — Build inter-chunk reference graph
  - `figure_index.py` — Figure number → description mapping

**Output:** `rag/data/chunks.jsonl` — All chunks with metadata

### Phase 2: Embedding & Vector Store

**Deliverables:**
- `rag/embedding/` — Embedding pipeline
  - `embed.py` — Batch embed all chunks (dense + verbalized math variants)
  - `bm25_index.py` — Build BM25 keyword index
- `rag/store/` — Vector store setup
  - `chroma_store.py` — ChromaDB collection creation and population
  - `structured_index.py` — Equation/figure/function lookup tables

**Output:** Populated ChromaDB instance + keyword index + structured indices

### Phase 3: Retrieval Engine

**Deliverables:**
- `rag/retrieval/` — Retrieval pipeline
  - `query_preprocessor.py` — Intent classification, entity extraction, math normalization
  - `hybrid_retriever.py` — Semantic + BM25 + structured retrieval with RRF fusion
  - `chain_expander.py` — Derivation chain expansion logic
  - `reranker.py` — Cross-encoder re-ranking with domain-specific boosts

### Phase 4: Generation & Interface

**Deliverables:**
- `rag/generation/` — LLM generation pipeline
  - `context_assembler.py` — Assemble retrieved chunks into prompt context
  - `generator.py` — LLM call with system prompt, conventions, citations
- `rag/interface/` — User interface
  - `cli.py` — Command-line Q&A interface
  - `api.py` — FastAPI endpoint (optional, for web UI)

### Phase 5: Evaluation & Tuning

**Deliverables:**
- `rag/eval/` — Evaluation framework
  - `test_queries.json` — Benchmark questions with expected answers
  - `evaluate.py` — Retrieval precision/recall + generation quality scoring

---

## 9. Benchmark Query Set (for evaluation)

| # | Query | Expected Source | Type |
|---|-------|-----------------|------|
| 1 | "What is the stability constraint on σ̂?" | math-deriv Sec 6.2 | Derivation |
| 2 | "Show the Bjorken flow ODE derivation" | math-deriv Sec 8 | Derivation chain |
| 3 | "What numerical method is used for the shockwave PDE?" | numerical-impl Sec 4 | Algorithm |
| 4 | "What does Fig. 4 demonstrate about acausality?" | test-results Sec 8 | Interpretation |
| 5 | "What parameters does the heat flow test use?" | numerical-impl Table II | Lookup |
| 6 | "How does `transportCoeffs` compute β_ε?" | bdnk_common.wl | Code |
| 7 | "Why is σ̂ > 1/3 unstable?" | math-deriv Sec 6 + test-results Sec 10 | Cross-doc |
| 8 | "What is the convergence order of the PDE solver?" | test-results Sec 11 + convergence.wl | Cross-doc |
| 9 | "Derive the characteristic speed c₊²" | math-deriv Sec 5.2 | Derivation |
| 10 | "What is the difference between Eckart and BDNK frames?" | math-deriv Sec 4.4 + test-results Sec 4 | Conceptual |

---

## 10. Technology Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Language | Python 3.11+ | Ecosystem support |
| Embeddings | `voyage-3` or `text-embedding-3-large` | Best scientific text retrieval |
| Vector store | ChromaDB | Local, no infra needed, good for <10K chunks |
| BM25 | `rank_bm25` | Lightweight keyword search |
| Re-ranker | `cross-encoder/ms-marco-MiniLM-L-12-v2` | Fast, good accuracy |
| LLM | Claude API (claude-sonnet-4-6 or claude-opus-4-6) | Best math reasoning; already in-project |
| Markdown parsing | `mistune` or `markdown-it-py` | Preserves LaTeX blocks |
| LaTeX parsing | `pylatexenc` + custom | Equation extraction |
| CLI | `typer` or `click` | Simple interface |
| API (optional) | FastAPI | If web UI desired |

---

## 11. Directory Structure (Final)

```
rag/
├── __init__.py
├── config.py                    # API keys, model names, paths
├── parsers/
│   ├── __init__.py
│   ├── markdown_parser.py
│   ├── latex_parser.py
│   ├── wolfram_parser.py
│   └── bibtex_parser.py
├── chunking/
│   ├── __init__.py
│   ├── section_chunker.py
│   ├── derivation_chunker.py
│   └── code_chunker.py
├── metadata/
│   ├── __init__.py
│   ├── equation_index.py
│   ├── cross_ref_graph.py
│   └── figure_index.py
├── embedding/
│   ├── __init__.py
│   ├── embed.py
│   └── bm25_index.py
├── store/
│   ├── __init__.py
│   ├── chroma_store.py
│   └── structured_index.py
├── retrieval/
│   ├── __init__.py
│   ├── query_preprocessor.py
│   ├── hybrid_retriever.py
│   ├── chain_expander.py
│   └── reranker.py
├── generation/
│   ├── __init__.py
│   ├── context_assembler.py
│   └── generator.py
├── interface/
│   ├── __init__.py
│   ├── cli.py
│   └── api.py
├── eval/
│   ├── __init__.py
│   ├── test_queries.json
│   └── evaluate.py
├── data/
│   ├── chunks.jsonl             # Processed chunks
│   ├── equation_index.json      # Eq number → chunk mapping
│   ├── figure_index.json        # Fig number → description
│   ├── function_index.json      # Function → file:line
│   └── chroma_db/               # Vector store data
├── ingest.py                    # Main ingestion script
├── query.py                     # Main query entry point
└── requirements.txt
```

---

## 12. Key Design Decisions

### Why not just dump everything into context?

The full corpus is ~650 KB of text (~160K tokens). This fits in a large context window but:
- **Cost:** Every query pays for 160K input tokens
- **Noise:** Irrelevant sections dilute attention
- **Latency:** Full-context queries are slow
- **Scalability:** If the corpus grows (more tests, papers, implementations), full-context breaks

RAG retrieves only the ~4K–8K most relevant tokens per query: **20–40x cost reduction** with better precision.

### Why hybrid retrieval (not just vector search)?

- **Equation references** ("Eq. 29") are exact strings — vector search may miss; keyword/structured lookup hits perfectly
- **Function names** ("charSpeeds") are domain-specific tokens that embeddings may not cluster well
- **Conceptual queries** ("stability") need semantic understanding — vector search excels here
- Hybrid covers all query types

### Why derivation chain expansion?

Mathematical derivations are **sequential proofs**. Retrieving step 7 of a derivation without steps 1–6 produces hallucination risk. Chain expansion ensures the LLM has the logical foundation.

### Why dual math representation?

`$\hat{\sigma} \leq 1/3$` and "sigma-hat must be at most one-third" are the same statement. Users may query either way. Embedding both representations covers both retrieval paths.

---

## 13. Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| LaTeX math poorly embedded | Missed retrieval for math queries | Dual representation + equation index fallback |
| Derivation chains broken by chunking | Hallucinated intermediate steps | Chain-aware chunking + expansion |
| Wolfram Language not well-understood by embeddings | Poor code retrieval | Enrich code chunks with natural language summaries from comments |
| Stale chunks after document updates | Wrong answers | Re-ingestion script; hash-based change detection |
| Small corpus makes embedding quality less critical | Over-engineering | Start with simple chunking; add complexity only where eval shows gaps |

---

## 14. Execution Priority

1. **Phase 1** (chunking) — highest value; determines retrieval quality
2. **Phase 3** (retrieval) — enables querying immediately with simple generation
3. **Phase 2** (embedding) — mechanical; standard tooling
4. **Phase 4** (generation) — thin wrapper over Claude API
5. **Phase 5** (eval) — validates and tunes the system

**Estimated effort:** Phase 1–4 can be implemented in a single focused session. Phase 5 is ongoing.

---

## 15. Quick-Start Command

Once built:

```bash
# Ingest all documents
python rag/ingest.py

# Query the system
python rag/query.py "What is the stability constraint on sigma-hat?"

# Or interactive mode
python rag/query.py --interactive
```
