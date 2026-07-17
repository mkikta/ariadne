import pytest
from unittest.mock import AsyncMock
import processing.utils as utils

@pytest.mark.asyncio
async def test_unit_success_add_one_document(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.add.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.add_documents(
        collection_name="document",
        ids=[0],
        documents=["lorum ipsum"],
    )

    assert result is None
    fake_client.get_collection.assert_awaited_once_with(name="document")
    fake_collection.add.assert_awaited_once_with(
        ids=[0],
        documents=["lorum ipsum"],
    )

@pytest.mark.asyncio
async def test_unit_success_add_multiple_documents(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.add.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.add_documents(
        collection_name="document",
        ids=[0, 1, 2],
        documents=["test document 0", "test document 1", "test document 2"],
    )

    assert result is None
    fake_client.get_collection.assert_awaited_once_with(name="document")
    fake_collection.add.assert_awaited_once_with(
        ids=[0, 1, 2],
        documents=["test document 0", "test document 1", "test document 2"],
    )

@pytest.mark.asyncio
async def test_unit_success_add_documents_metadatas(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.add.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.add_documents(
        collection_name="document",
        ids=[0, 1, 2],
        documents=["test document 0", "test document 1", "test document 2"],
        metadatas=[{"name": "doc0"}, {"name": "doc1"}, {"name": "doc2"}],
    )

    assert result is None
    fake_client.get_collection.assert_awaited_once_with(name="document")
    fake_collection.add.assert_awaited_once_with(
        ids=[0, 1, 2],
        documents=["test document 0", "test document 1", "test document 2"],
         metadatas=[{"name": "doc0"}, {"name": "doc1"}, {"name": "doc2"}],
    )

@pytest.mark.asyncio
async def test_unit_failure_add_mismatched_documents(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.add.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    with pytest.raises(ValueError, match="ids and documents must have the same length"):
            await utils.add_documents(
                collection_name="document",
                ids=[0, 1, 2, 3, 4],
                documents=["test document 0", "test document 1", "test document 2"],
            )
