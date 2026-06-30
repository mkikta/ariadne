"""FastAPI server for document processing.

This module provides endpoints for monitoring system health and 
queuing documents for processing through the document pipeline. 
All processing is performed asynchronously using background tasks.
"""

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Form
import utils

app = FastAPI()


@app.get("/health/")
async def health():
    """Health check endpoint.

    Returns a simple response indicating the service is operational.

    Returns:
        dict: A dictionary with a health message.
    """
    return {"message": "Healthy!"}


@app.post("/process_document/")
async def process_document(
    document_collection_name: str = Form(...),
    chunks_collection_name: str = Form(...),
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    """Queue a document for processing in the background.

    Accepts a document file and queues it for processing through the document pipeline.
    The actual processing is performed asynchronously in the background.

    Args:
        document_collection_name: Name of the ChromaDB collection for documents.
        chunks_collection_name: Name of the ChromaDB collection for chunks.
        file: The document file to process.
        background_tasks: FastAPI background tasks object for managing asynchronous operations.

    Returns:
        dict: A dictionary with status 'accepted' and a confirmation message.
    """
    file_bytes: bytes = await file.read()
    filename = file.filename or "untitled"
    if background_tasks:
        background_tasks.add_task(
            utils.run_pipeline,
            document_collection_name,
            chunks_collection_name,
            filename,
            file_bytes,
        )
    return {
        "status": "accepted",
        "message": f"Document '{filename}' queued for processing",
    }
