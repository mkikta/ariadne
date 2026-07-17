"""Script to initialize document and chunks collections."""

import asyncio
import logging
import os
from . import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def initialize_collections():
    """Initialize ChromaDB collections on startup.

    Waits for ChromaDB to become available, then creates the document
    collection (no embeddings) and the chunks collection (with Ollama
    embeddings).

    Raises:
        Exception: If ChromaDB remains unreachable after all retries.
    """
    max_retries = 10
    for attempt in range(max_retries):
        try:
            async with utils.get_client() as client:
                await client.heartbeat()
            break
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(
                    "ChromaDB not reachable after %d attempts", max_retries
                )
                raise
            logger.warning(
                "ChromaDB not ready (attempt %d/%d): %s",
                attempt + 1,
                max_retries,
                e,
            )
            await asyncio.sleep(2**attempt)

    await utils.create_collection(os.getenv("DOCUMENT_COLLECTION"))
    await utils.create_collection(
        os.getenv("CHUNKS_COLLECTION"),
        embedding_backend="ollama",
        model_name=os.getenv("MODEL"),
        embedding_host=os.getenv("OLLAMA_HOST"),
        embedding_port=os.getenv("OLLAMA_PORT"),
    )
    logger.info("Collections initialized successfully")

if __name__ == "__main__":
    asyncio.run(initialize_collections())