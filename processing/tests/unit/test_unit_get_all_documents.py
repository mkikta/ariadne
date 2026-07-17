import pytest
from unittest.mock import AsyncMock
from processing import utils
from chromadb.api.types import GetResult

@pytest.mark.asyncio
async def test_unit_success_get_all_documents(mocker):
    fake_collection = AsyncMock()
    fake_collection.get.return_value = GetResult(
        ids=[[0, 1, 2]],
        embeddings=[[[0.0] * 1024, [1.0] * 1024, [2.0] * 1024]],
        documents=[["test document 0", "test document 1", "test document 2"]],
        metadatas=[[{"name": "doc0"}, {"name": "doc1"}, {"name": "doc2"}]],
    )

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "processing.utils.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    result = await utils.get_all_documents("document")

    assert result["ids"] == [[0, 1, 2]]
    assert result["embeddings"]==[[[0.0] * 1024, [1.0] * 1024, [2.0] * 1024]]
    assert result["documents"]==[["test document 0", "test document 1", "test document 2"]]
    assert result["metadatas"]==[[{"name": "doc0"}, {"name": "doc1"}, {"name": "doc2"}]]
    fake_client.get_collection.assert_awaited_once_with(name="document")
    fake_collection.get.assert_awaited_once_with()
    
