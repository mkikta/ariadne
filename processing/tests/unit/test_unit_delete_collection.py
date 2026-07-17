import re
import pytest
from unittest.mock import AsyncMock
from processing import utils

@pytest.mark.asyncio
async def test_unit_success_delete_collection(mocker):
    fake_client = AsyncMock()
    fake_client.delete_collection.return_value = None

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.delete_collection("document")

    assert result is None
    fake_client.delete_collection.assert_awaited_once_with(name="document")

@pytest.mark.asyncio
async def test_unit_failure_delete_collection(mocker):
    fake_client = AsyncMock()
    fake_client.delete_collection.side_effect = RuntimeError("Collection [typo] does not exist")

    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=AsyncMock(return_value=fake_client),
    )

    with pytest.raises(RuntimeError, match=re.escape("Collection [typo] does not exist")):
        await utils.delete_collection("typo")

    fake_client.delete_collection.assert_awaited_once_with(name="typo")
