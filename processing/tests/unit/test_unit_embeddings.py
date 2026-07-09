from chromadb.api.types import EmbeddingFunction
from processing.embeddings import EmbeddingFunctionFactory

def test_success_get_embedding_function():
    ef = EmbeddingFunctionFactory.get_embedding_function(
        "ollama",
        "qwen3-embedding:0.6b",
        "",
        ""
    )

    assert isinstance(ef, EmbeddingFunction)

def test_failure_get_embedding_function(mocker):
    ef = EmbeddingFunctionFactory.get_embedding_function(
        "vllm",
        "qwen3-embedding:0.6b",
        "",
        ""
    )

    assert ef is None
