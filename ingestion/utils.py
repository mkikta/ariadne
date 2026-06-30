"""
Utility functions for ChromaDB client interactions and document management.
"""

import os
from contextlib import asynccontextmanager
import chromadb
from embeddings import EmbeddingFunctionFactory


@asynccontextmanager
async def get_client():
    """Async context manager for creating and managing ChromaDB client connections.

    Yields:
        chromadb.AsyncHttpClient: ChromaDB client instance with configured host and port
    """
    client = await chromadb.AsyncHttpClient(
        host=os.getenv("CHROMA_HOST"), port=int(os.getenv("CHROMA_PORT"))
    )
    yield client


async def create_collection(
    name: str,
    embedding_backend: str | None = None,
    model_name: str | None = None,
    embedding_host: str | None = None,
    embedding_port: str | None = None,
):
    """Create a new ChromaDB collection with optional embedding function.

    Args:
        name: Name of the collection to create
        embedding_backend: Backend for embedding generation (e.g., "ollama")
        model_name: Name of the embedding model to use
        embedding_host: Host for the embedding backend
        embedding_port: Port for the embedding backend

    Raises:
        Exception: If collection creation fails
    """
    if embedding_backend:
        embedding_function = EmbeddingFunctionFactory.get_embedding_function(
            embedding_backend,
            model_name,
            embedding_host,
            embedding_port,
        )
        async with get_client() as client:
            await client.get_or_create_collection(
                name=name, embedding_function=embedding_function
            )
    else:
        async with get_client() as client:
            await client.get_or_create_collection(
                name=name,
                embedding_function=None,
            )


async def get_collection(name: str):
    """Retrieve a collection by its name.

    Args:
        name: Name of the collection to retrieve

    Returns:
        chromadb.Collection: The retrieved collection object

    Raises:
        Exception: If collection retrieval fails
    """
    async with get_client() as client:
        collection = await client.get_collection(name=name)
        return collection


async def delete_collection(name: str):
    """Delete a collection by its name.

    Args:
        name: Name of the collection to delete

    Raises:
        Exception: If collection deletion fails
    """
    async with get_client() as client:
        await client.delete_collection(name=name)


async def add_documents(
    collection_name: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict] | None = None,
):
    """Add documents to a collection.

    Args:
        collection_name: Name of the target collection
        ids: List of document IDs to add
        documents: List of document content strings
        metadatas: Optional list of metadata dictionaries for each document

    Raises:
        ValueError: If the length of IDs doesn't match the length of documents
        Exception: If document addition fails
    """
    if len(ids) != len(documents):
        raise ValueError("ids and documents must have the same length")
    collection = await get_collection(collection_name)
    if metadatas:
        await collection.add(ids=ids, documents=documents, metadatas=metadatas)
    else:
        await collection.add(
            ids=ids,
            documents=documents,
        )


async def delete_documents(collection_name: str, ids: list[str]):
    """Delete documents from a collection.

    Args:
        collection_name: Name of the target collection
        ids: List of document IDs to delete

    Raises:
        Exception: If document deletion fails
    """
    collection = await get_collection(collection_name)
    await collection.delete(ids=ids)


async def get_all_documents(collection_name: str):
    """Get all documents from a collection.

    Args:
        collection_name: Name of the collection to retrieve documents from

    Returns:
        dict: Query results containing all documents in the collection

    Raises:
        Exception: If document retrieval fails
    """
    collection = await get_collection(collection_name)
    results = await collection.get()
    return results
