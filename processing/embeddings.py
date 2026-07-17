"""
Embeddings module provides factory functions for creating embedding functions from various backends.
"""

from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from chromadb.utils.embedding_functions import EmbeddingFunction


class EmbeddingFunctionFactory:
    """Factory class for creating embedding function instances from different backends.

    This class provides a centralized way to instantiate embedding functions
    based on the specified backend, model, and connection parameters.
    """

    @staticmethod
    def get_embedding_function(
        backend: str,
        model_name: str,
        host: str | None = None,
        port: str | None = None,
    ) -> EmbeddingFunction | None:
        """Creates an embedding function instance for the specified backend.
        Note that ollama is currently the only supported backend.

        Args:
            backend: The embedding backend to use (e.g., "ollama")
            model_name: The name of the embedding model to use
            host: Backend host
            port: Backend port

        Returns:
            An embedding function instance, or None if backend is not supported
        """
        if backend == "ollama":
            return OllamaEmbeddingFunction(
                url=f"http://{host}:{port}",
                model_name=model_name,
            )

        print(f"Backend {backend} is not supported!")
        return None
