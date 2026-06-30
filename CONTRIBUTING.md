# Contributing to Ariadne

Thank you for your interest in contributing to Ariadne! This document outlines the development workflow and standards for this project.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Running Linting](#running-linting)
- [Running Tests](#running-tests)
- [Docker Compose](#docker-compose)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Project Structure

Ariadne is a multi-service application composed of three services, each in its own directory:

| Directory | Service | Description |
|---|---|---|
| `management/` | Management Server | FastAPI server for ChromaDB collection management |
| `processing/` | Processing Server | FastAPI server using Docling to convert, chunk, and enrich documents, and insert them into ChromaDB |
| `mcp_server/` | MCP Server | FastMCP server exposing `search` and `fetch_document` tools |

Each service has its own `pyproject.toml`, dependency declarations, and `uv.lock` lockfile.

There is also a `scripts` folder, which currently includes a script for uploading files to the processing server.

## Prerequisites

- **Python 3.12** — all services target Python 3.12 only.
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — the Python package and project manager used across the project.
- **Docker** — required for running the full stack (vector database, embedding model) via Docker Compose.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mkikta/ariadne.git
   cd ariadne
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Sync dependencies for the service you want to work on:
   ```bash
   uv sync --directory management
   uv sync --directory processing
   uv sync --directory mcp_server
   uv sync --directory scripts
   ```

   Each service is independently managed. You only need to sync the directories relevant to your changes.

4. Activate the service's virtual environment (or use `uv run`):
   ```bash
   source management/.venv/bin/activate
   ```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b my-feature-branch
   ```

2. Make your changes, following the [coding standards](#coding-standards) below.

3. Run linting:

   ```bash
   uv run --directory management ruff check .
   ```

   Repeat for `processing`, `mcp_server`, and `scripts` as needed.

4. If running the full stack is required, start Docker Compose:

   ```bash
   docker compose up --build
   ```

5. Commit your changes with a descriptive message and open a pull request against `main`.

## Coding Standards

### Python & Style

- **Python 3.12+** syntax throughout.
- **Type hints** are required on all function signatures. Use Python 3.10+ syntax:
  - `list[str]` instead of `List[str]`
  - `dict[str, str]` instead of `Dict[str, str]`
  - `X | None` instead of `Optional[X]`
- **Docstrings** follow the Google-style format with `Args:`, `Returns:`, and `Raises:` sections where applicable.
- **Double quotes** for strings (`"` rather than `'`).
- **Module-level docstrings** at the top of every Python file.
- **Snake case** for functions and modules, **PascalCase** for classes, **UPPER_CASE** for constants.
- **Private helpers** prefixed with a single underscore (`_pipeline`).

### Linting

We use **[ruff](https://docs.astral.sh/ruff/)** as the sole linter. It is configured with default settings (no custom `pyproject.toml` overrides). Before submitting changes, ensure your code passes:

```bash
uv run --directory <service> ruff check .
```

## Running Linting

CI runs `ruff check .` on all four service directories. You can run the same checks locally:

```bash
uv run --directory management ruff check .
uv run --directory processing ruff check .
uv run --directory mcp_server ruff check .
uv run --directory scripts ruff check .
```

There is currently no auto-formatter configured. Run `ruff check --fix` to apply automatic fixes where supported.

## Running Tests

Tests are not yet implemented. `pytest` is available as a dependency in the `management` and `processing` services and can be used when writing tests:

```bash
uv run --directory management pytest
```

Contributions that add test coverage are especially welcome.

## Docker Compose

To test the full integration of your changes, build and run all services:

```bash
docker compose up --build
```

The services will be available at:
- **Management API**: `http://localhost:3000`
- **MCP Server**: `http://localhost:8080/mcp`
- **ChromaDB**: internal (port `8000`)
- **Ollama**: internal (port `11434`)

## Pull Request Process

1. Ensure your branch is up to date with `main`.
2. Ensure all CI checks pass (linting + Docker build).
3. Open a pull request against `main` with a clear title and description.
4. Keep changes focused. If a change touches multiple services, consider splitting into separate PRs.
5. A maintainer will review your PR and may request changes.

## Reporting Issues

Report bugs and request features via [GitHub Issues](https://github.com/mkikta/ariadne/issues). For questions and discussion, use [GitHub Discussions](https://github.com/mkikta/ariadne/discussions).

---

Ariadne is licensed under the [MIT License](LICENSE).
