"""
Model Context Protocol (MCP) server for Ariadne.

This module provides FastMCP tools for interacting with ChromaDB collections,
including document search and retrieval capabilities.
"""

import os
from contextlib import asynccontextmanager
from fastmcp import FastMCP
from starlette.responses import JSONResponse
import chromadb

mcp = FastMCP(
    "Ariadne",
    instructions=(
        "You are Ariadne, a document retrieval assistant. You have access to "
        "two tools:\n"
        "\n"
        "1. search(query, document_id?): semantic similarity search over document "
        "chunks. Chunks are small text fragments extracted from ingested documents "
        "and indexed with embeddings. Use this when the user asks questions about "
        "document content. You can scope results to a single document by passing "
        "its document_id (a UUID). Results are (chunks, metadata) pairs; each "
        "metadata entry contains 'document_id' and 'chunk_idx'.\n"
        "\n"
        "2. fetch_document(name?, document_id?): retrieve a complete document as "
        "Markdown from the document collection. Use this when the user wants the "
        "full text rather than snippets, or to obtain a document_id for a "
        "follow-up search. Provide exactly one of 'name' (original filename, "
        "exact match) or 'document_id' (UUID assigned during ingestion).\n"
        "\n"
        "When a user asks about specific content, first use search to find "
        "relevant chunks. If they need the broader context, follow up with "
        "fetch_document using the document_id from search results."
    ) + (os.getenv("CUSTOM_INSTRUCTIONS") or ""),
)


@asynccontextmanager
async def get_client():
    """Async context manager for creating and managing ChromaDB client connections.

    Yields:
        chromadb.AsyncHttpClient: ChromaDB client instance with configured host and port

    Returns:
        AsyncContextManager: Async context manager for ChromaDB client connections
    """
    client = await chromadb.AsyncHttpClient(
        host=os.getenv("CHROMA_HOST"), port=int(os.getenv("CHROMA_PORT"))
    )
    yield client


@mcp.tool(
    name="search",
    description="Perform semantic (vector) similarity search over document chunks. "
    "Returns text fragments most relevant to the query. Use this when the user "
    "asks questions about the content of ingested documents, needs to find "
    "specific information, or wants to retrieve relevant passages. "
    "Optionally pass a document_id (UUID returned by fetch_document) to scope "
    "the search to a single document. Results include both the chunk text and "
    "its metadata (document_id, chunk_idx).",
    annotations={
        "title": "Search",
        "readOnlyHint": True,
    },
)
async def search(query: str, document_id: str | None = None):
    """Search vector database for query. Optionally filter by document_id.

    Args:
        query: The search query text to find similar documents
        document_id: Optional document ID to filter results

    Returns:
        tuple: A tuple containing (documents, metadatas) from the search results

    Raises:
        Exception: If ChromaDB connection or query fails
    """
    async with get_client() as client:
        collection = await client.get_collection(name=os.getenv("CHUNKS_COLLECTION"))
        if document_id:
            results = await collection.query(
                query_texts=[query], n_results=10, where= {"document_id": document_id}
            )
        else:
            results = await collection.query(
                query_texts=[query],
                n_results=10,
            )

    return results["documents"][0], results["metadatas"][0]


@mcp.tool(
    name="fetch_document",
    description="Retrieve a complete document by its original filename (name) or "
    "document_id (UUID). Use this when the user wants the full text of a "
    "document rather than just relevant snippets, or when you need the "
    "document_id to scope a follow-up search. Exactly one of 'name' or "
    "'document_id' must be provided. Returns the full Markdown content and "
    "metadata. 'name' is the original filename (e.g., 'report.pdf') and works "
    "as an exact match. 'document_id' is the UUID assigned during ingestion.",
    annotations={
        "title": "Fetch Document",
        "readOnlyHint": True,
    },
)
async def fetch_document(name: str | None = None, document_id: str | None = None):
    """Fetch document by name or document_id from the document collection.

    Args:
        name: Optional document name to fetch
        document_id: Optional document ID to fetch

    Returns:
        tuple: A tuple containing (documents, metadatas) from the fetched document

    Raises:
        Exception: If ChromaDB connection or document fetch fails
    """
    if name and document_id or not (name or document_id):
        return "Exactly one of name and document_id is required."
    async with get_client() as client:
        collection = await client.get_collection(name=os.getenv("DOCUMENT_COLLECTION"))
        if document_id:
            results = await collection.get(ids=[document_id])
        if name:
            results = await collection.get(where={"name": name})

    return results["documents"][0], results["metadatas"][0]


@mcp.custom_route("/health", methods=["GET"])
async def health_check():
    """Health check endpoint for MCP server status.

    Returns:
        JSONResponse: Health status response with service information

    Raises:
        Exception: If JSONResponse creation fails
    """
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


app = mcp.http_app()
