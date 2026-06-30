# 🧶 Ariadne

[![Lint](https://img.shields.io/github/actions/workflow/status/mkikta/ariadne/ci.yml?label=lint&job=lint)](https://github.com/mkikta/ariadne/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/github/actions/workflow/status/mkikta/ariadne/ci.yml?label=docker&job=docker)](https://github.com/mkikta/ariadne/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Ariadne, daughter of King Minos, helped Theseus escape from the Minotaur with a thread through the Labyrinth.

Ariadne, the MCP server, helps your agents escape from the complex maze of your unstructured data.

> [!WARNING]
> This repository is a work-in-progress.

## 🌟 Highlights

Ariadne is an end-to-end utility for delivering unstructured data to your agents.

Features:
- Upload any documents, to be later made available to your agents.
- Documents are chunked, enriched, and stored in a vector database.
- MCP clients can connect to the MCP server, which exposes tools for retrieving chunks and whole documents.

## ℹ️ Overview

Ariadne consists of a few main components:

* A management server that interacts with the [ChromaDB](https://www.trychroma.com) database.
* A processing server that uses [Docling](https://www.docling.ai), to convert, serialize, chunk, and enrich documents before inserting them into the ChromaDB database.
* A ChromaDB database, that stores the serialized and chunked documents, using [Ollama](https://ollama.com) to serve the embedding model.
* A [FastMCP](https://gofastmcp.com/getting-started/welcome) server that MCP clients can connect to to query the database for full documents by id or to query for document chunks by semantic meaning.


## ⬇️ Setup

1. Install [Docker](https://www.docker.com) on your machine.
2. Start the Docker daemon.
3. Install [Git](https://git-scm.com) on your machine.
4. Git clone this repo: `git clone https://github.com/mkikta/ariadne.git`
5. Navigate to the repository: `cd ariadne`
6. Copy `.env.example` to `.env`. Optionally, add custom instructions to the MCP server by setting CUSTOM_INSTRUCTIONS and change the embedding model to any Ollama-supported embedding model.
7. Run Ariadne: `docker compose up --build`
The management API will be hosted at http://localhost:3000, the MCP server will be hosted at http://localhost:8080/mcp, and if you use the out-of-the-box configuration, [qwen3-embedding:0.6b](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) will be used for embeddings. 

> [!WARNING]
> Once you set a model, you must continue to use the same model to use the same persisted ChromaDB database.

> [!NOTE]
> It is recommended to use a machine with at least 16GB RAM to run Ariadne, in order to accomodate both the default embedding model and Docling.

## 🚀 Usage

Ensure Ariadne is running, as in [Setup](#️-setup).

First, we must upload some documents to the Ariadne database. Right now, there is a python setup script to do this. (In the near future a dashboard for document uploads will be added, followed by integrations to common data sources.) To upload documents:

1. Navigate to `scripts`: `cd scripts`.
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
3. Synchronize your environment: `uv sync`
4. Run the upload script: `uv run upload.py --paths DIRECTORIES_AND_OR_FILES` Replace DIRECTORY_AND_OR_FILES with a space-separated list of any number of paths to directories and/or files you wish to upload to Ariadne.


The Ariadne MCP server is compatible with any non-web-based MCP client, such as [OpenCode](http://opencode.ai), [Hermes Agent](https://hermes-agent.nousresearch.com), [Claude Code](https://code.claude.com/docs/en/overview), or [OpenClaw](https://openclaw.ai). Check your MCP client documentation for how to connect. Most MCP clients have a prompted MCP connection guide to follow. For OpenCode, this process is:
1. Run `opencode mcp add`.
2. Select `Global` or `Project` location.
3. Name the mcp server `ariadne`.
4. Select MCP server type `Remote`.
5. Enter MCP server URL `http://localhost:8080/mcp`.
6. Select `No` for authentication required.

## 🗺️ Roadmap

- [ ] Enhance the Docling processing pipeline to include image annotation; code, figure, and formula enrichment; table header repetition; smarter chunking; and possibly entity recognition.

- [ ] Add a user-friendly dashboard for document upload.

- [ ] Add integrations to common data sources, including Google Drive, Microsoft 365, Notion, etc.

- [ ] Add more model backends.

### ✍️ Author

I'm [Mark Kikta](https://mkikta.com), and I am creating Ariadne to be a modular, end-to-end solution to the common problem of sharing a collection of unstructured data with your agents.


## 🤝 Feedback and Contributing

I encourage you to start a [Discussion](https://github.com/mkikta/ariadne/discussions) if you find this project useful or exciting! I would greatly appreciate feedback and any issues regaring bugs or feature requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and pull request guidelines.
