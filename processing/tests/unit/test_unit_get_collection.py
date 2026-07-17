import re
import pytest
from unittest.mock import AsyncMock
from processing import utils

@pytest.mark.asyncio
async def test_unit_success_get_collection(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.get_collection("document")

    assert result is fake_collection
    fake_client.get_collection.assert_awaited_once_with(name="document")

@pytest.mark.asyncio
async def test_unit_failure_get_collection(mocker):
    fake_client = AsyncMock()
    fake_client.get_collection.side_effect = RuntimeError("Collection [typo] does not exist")

    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=AsyncMock(return_value=fake_client),
    )

    with pytest.raises(RuntimeError, match=re.escape("Collection [typo] does not exist")):
        await utils.get_collection("typo")

    fake_client.get_collection.assert_awaited_once_with(name="typo")
