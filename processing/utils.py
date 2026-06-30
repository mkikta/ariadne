"""Utilities for document processing and storage.

This module provides functions for:
- Connecting to ChromaDB for document storage
- Converting documents to markdown and extracting chunks
- Running the full document processing pipeline
"""

from io import BytesIO
import os
import logging
from uuid import uuid4
import asyncio
from contextlib import asynccontextmanager
import chromadb
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from docling.chunking import HybridChunker

logger = logging.getLogger(__name__)
_converter = DocumentConverter()

@asynccontextmanager
async def get_client():
    """Context manager to create and yield a ChromaDB async client.

    Returns:
        AsyncHttpClient: A connected ChromaDB client instance.
    """
    client = await chromadb.AsyncHttpClient(
        host=os.getenv("CHROMA_HOST"), port=int(os.getenv("CHROMA_PORT"))
    )
    yield client


async def get_collection(name: str):
    """Get a ChromaDB collection by name.

    Args:
        name: The name of the collection to retrieve.

    Returns:
        Collection: The ChromaDB collection object.
    """
    async with get_client() as client:
        collection = await client.get_collection(name=name)
        return collection


async def add_documents(
    collection_name: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict] | None = None,
):
    """Add document data to a ChromaDB collection.

    Args:
        collection_name: Name of the ChromaDB collection to add documents to.
        ids: List of document IDs for the documents.
        documents: List of document strings/text content.
        metadatas: Optional list of metadata dictionaries for each document.

    Raises:
        ValueError: If the number of IDs doesn't match the number of documents.
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


def process_document(filename: str, file_bytes: bytes):
    """Convert a document file to markdown and extract chunks.

    This function uses Docling to convert a document from its binary format
    to markdown, and then uses HybridChunker to split the document into
    smaller chunks for better processing.

    Args:
        filename: Name of the document file (used for processing context).
        file_bytes: The binary content of the document file to process.

    Returns:
        tuple: A tuple containing:
            - document_markdown: The full document converted to markdown format (str)
            - chunks: A list of contextualized text chunks (list[str])
    """
    stream = BytesIO(file_bytes)
    source = DocumentStream(name=filename, stream=stream)
    dl_doc = _converter.convert(source).document

    chunker = HybridChunker()
    chunk_iter = chunker.chunk(dl_doc=dl_doc)

    chunks = [chunker.contextualize(chunk=chunk) for chunk in chunk_iter]

    return dl_doc.export_to_markdown(), chunks


async def _pipeline(
    document_collection_name: str,
    chunks_collection_name: str,
    filename: str,
    file_bytes: bytes,
):
    """Internal pipeline function that processes a document and stores results.

    This function:
    1. Converts the document to markdown
    2. Stores the full document in the document collection
    3. Extracts and stores text chunks in the chunks collection

    Args:
        document_collection_name: Name of the ChromaDB collection for full documents.
        chunks_collection_name: Name of the ChromaDB collection for text chunks.
        filename: Name of the document file being processed.
        file_bytes: The binary content of the document file.
    """
    document, chunks = await asyncio.to_thread(process_document, filename, file_bytes)
    document_id = str(uuid4())
    await add_documents(
        document_collection_name,
        [document_id],
        [document],
        metadatas=[{"name": filename}],
    )
    await add_documents(
        chunks_collection_name,
        [str(uuid4()) for _ in chunks],
        chunks,
        metadatas=[
            {"document_id": document_id, "chunk_idx": i} for i in range(len(chunks))
        ],
    )


async def run_pipeline(
    document_collection_name: str,
    chunks_collection_name: str,
    filename: str,
    file_bytes: bytes,
):
    """Run the full document processing pipeline.

    This is the main entry point for document processing. It executes the
    internal pipeline and logs the result of the operation.

    Args:
        document_collection_name: Name of the ChromaDB collection for documents.
        chunks_collection_name: Name of the ChromaDB collection for chunks.
        filename: Name of the document file being processed.
        file_bytes: The binary content of the document file.
    """
    try:
        await _pipeline(
            document_collection_name,
            chunks_collection_name,
            filename,
            file_bytes,
        )
        logger.info("Processed %s successfully", filename)
    except Exception as e:
        logger.error("Failed to process %s: %s", filename, e)
