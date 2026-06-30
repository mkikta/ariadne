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
    instructions=os.getenv("BASE_INSTRUCTIONS") + (os.getenv("CUSTOM_INSTRUCTIONS") or ""),
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
    description="Search vector database.",
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
    description="Fetch document.",
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
