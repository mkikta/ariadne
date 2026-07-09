# Ariadne — Agent Guide

Multi-service MCP stack for document processing and vector retrieval.

## Project structure

```
processing/    FastAPI server (port 3000) — Docling convert/chunk/enrich, stores to ChromaDB
mcp_server/    FastMCP server (port 8080) — tools: search (semantic), fetch_document
scripts/       upload.py — CLI to batch-upload files to processing
llm/           serve_model.sh — pulls embedding model in Ollama container
chromadb/      persisted vector database (gitignored)
ollama/        persisted model data (gitignored)
data/          sample documents
```

Each service has its own `pyproject.toml` + `uv.lock`. All target **Python ≥3.12**.

## Commands

```sh
# Sync dependencies for one or more services
uv sync --directory processing
uv sync --directory mcp_server
uv sync --directory scripts

# Lint (ruff is the sole linter; no formatter configured)
uv run --directory processing ruff check .
uv run --directory mcp_server ruff check .
uv run --directory scripts ruff check .

# Auto-fix lint issues
uv run --directory <service> ruff check --fix .

# Run full stack
cp .env.example .env          # first time
docker compose up --build

# Upload documents (requires running stack)
uv run --directory scripts upload.py --paths dir1 file2 ...
```

## CI

Four jobs: `lint` (ruff on all 3 packages), `processing-unit-tests`, `processing-integration-tests`, and `docker` (`docker compose build`). Runs on every push and PR.

## Tests

- **Unit tests**: `processing/tests/unit/` — run with `uv run --directory processing pytest tests/unit -v`
- **Integration tests**: `processing/tests/integration/` — run with `uv run --directory processing pytest tests/integration -v` (uses testcontainers for ChromaDB)
- Top-level `tests/` has scaffolding for future contract and end-to-end tests

## Architecture notes

- **Processing** accepts uploads via `POST /process_document/` and runs the Docling pipeline.
- **Processing** uses Docling (`DocumentConverter` + `HybridChunker`) to produce markdown and contextualized chunks, stores both in ChromaDB.
- **MCP server** exposes `search(query, document_id?)` and `fetch_document(name?, document_id?)`. Has a custom health endpoint at `GET /health`.
- ChromaDB uses **qwen3-embedding:0.6b** by default (via Ollama). Once a model is set, you must continue using it — changing models invalidates persisted embeddings.
- Collections are auto-created on processing container startup (`init_collections.py`): `document` (no embeddings) and `chunks` (with Ollama embeddings).

## Style

- Python 3.12+ syntax, type hints required
- Google-style docstrings (`Args:`, `Returns:`, `Raises:`)
- Double quotes for strings, module-level docstrings
- Private helpers prefixed with `_`
- No formatter — only `ruff check` for linting (default ruleset, no pyproject.toml overrides)
