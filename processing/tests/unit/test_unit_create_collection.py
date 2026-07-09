import pytest
from unittest.mock import AsyncMock
from processing import utils
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

class FakeEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self):
        pass

    def __call__(self, input: Documents) -> Embeddings:
        return [[0.0] * 1024 for _ in input]

@pytest.mark.asyncio
async def test_unit_success_create_collection_without_embeddings(mocker):
    fake_client = AsyncMock()
    fake_client.get_or_create_collection.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.create_collection("document")

    assert result is None
    fake_client.get_or_create_collection.assert_awaited_once_with(
        name="document",
        embedding_function=None
    )

@pytest.mark.asyncio
async def test_unit_success_create_collection_with_embeddings(mocker):
    fake_client = AsyncMock()
    fake_client.get_or_create_collection.return_value = None

    fake_ef = FakeEmbeddingFunction()

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    mocker.patch(
        "processing.embeddings.EmbeddingFunctionFactory.get_embedding_function",
        return_value=fake_ef,
    )

    result = await utils.create_collection(
        "chunks",
        embedding_backend="ollama",
        model_name="qwen3-embedding:0.6b",
        embedding_host="",
        embedding_port="",
    )

    assert result is None
    fake_client.get_or_create_collection.assert_awaited_once_with(
        name="chunks",
        embedding_function=fake_ef
    )
