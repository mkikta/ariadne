"""
FastAPI server providing endpoints for document management and processing.
"""

import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import utils

app = FastAPI()


class AddDocumentsPayload(BaseModel):
    """Payload model for adding documents to a collection.

    Args:
        collection_name: Name of the target collection
        ids: List of document IDs to add
        documents: List of document content strings
        metadatas: Optional list of metadata dictionaries for each document
    """

    collection_name: str
    ids: list[str]
    documents: list[str]
    metadatas: list[dict[str, str]] | None = None


class DeleteDocumentsPayload(BaseModel):
    """Payload model for deleting documents from a collection.

    Args:
        collection_name: Name of the target collection
        ids: List of document IDs to delete
    """

    collection_name: str
    ids: list[str]


@app.get("/health/")
async def health():
    """Health check endpoint.

    Returns:
        Dictionary with health status message
    """
    return {"message": "Healthy!"}


@app.post("/create_collection/")
async def create_collection(name: str, embeddings: bool = False):
    """Create a new collection with optional embeddings.

    Args:
        name: Name of the collection to create
        embeddings: Whether to use embedding generation for the collection

    Raises:
        HTTPException: If collection creation fails
    """
    try:
        if embeddings:
            await utils.create_collection(
                name,
                embedding_backend="ollama",
                model_name=os.getenv("MODEL"),
                embedding_host=os.getenv("OLLAMA_HOST"),
                embedding_port=os.getenv("OLLAMA_PORT"),
            )
        else:
            await utils.create_collection(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_collection/")
async def get_collection(name: str):
    """Get collection details by name.

    Args:
        name: Name of the collection to retrieve

    Returns:
        Dictionary with collection name

    Raises:
        HTTPException: If collection retrieval fails
    """
    try:
        collection = await utils.get_collection(name)
        return {"name": collection.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete_collection/")
async def delete_collection(name: str):
    """Delete a collection.

    Args:
        name: Name of the collection to delete

    Raises:
        HTTPException: If collection deletion fails
    """
    try:
        await utils.delete_collection(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_documents/")
async def add_documents(payload: AddDocumentsPayload):
    """Add documents to a collection.

    Args:
        payload: Document payload containing collection name, IDs, documents, and optional metadata

    Raises:
        HTTPException: If document addition fails
    """
    try:
        await utils.add_documents(
            payload.collection_name, payload.ids, payload.documents, payload.metadatas
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete_documents/")
async def delete_documents(payload: DeleteDocumentsPayload):
    """Delete documents from a collection.

    Args:
        payload: Document payload containing collection name and document IDs to delete

    Raises:
        HTTPException: If document deletion fails
    """
    try:
        await utils.delete_documents(payload.collection_name, payload.ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_all_documents/")
async def get_all_documents(collection_name: str):
    """Get all documents from a collection.

    Args:
        collection_name: Name of the collection to retrieve documents from

    Returns:
        Results dictionary containing all documents in the collection

    Raises:
        HTTPException: If document retrieval fails
    """
    try:
        results = await utils.get_all_documents(collection_name)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
