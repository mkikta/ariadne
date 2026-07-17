import pytest
from unittest.mock import AsyncMock
from processing import utils

@pytest.mark.asyncio
async def test_unit_success_delete_one_document(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.delete.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.delete_documents(
        collection_name="document",
        ids=[0],
    )

    assert result is None
    fake_client.get_collection.assert_awaited_once_with(
         name="document"
    )
    fake_collection.delete.assert_awaited_once_with(
        ids=[0],
    )

@pytest.mark.asyncio
async def test_unit_success_delete_multiple_documents(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.delete.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.delete_documents(
        collection_name="document",
        ids=[0, 1, 2],
    )

    assert result is None
    fake_client.get_collection.assert_awaited_once_with(
         name="document"
    )
    fake_collection.delete.assert_awaited_once_with(
        ids=[0, 1, 2],
    )

