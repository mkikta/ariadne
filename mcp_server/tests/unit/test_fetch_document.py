import os
import pytest
from unittest.mock import AsyncMock
from fastmcp import Client
from mcp_server.server import mcp
from chromadb.api.types import GetResult

@pytest.mark.asyncio
async def test_unit_fetch_document_by_name(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.get.return_value = GetResult(
        ids=[["0"]],
        documents=[["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2"]],
        metadatas=[[{"name": "Test 0"}]]
    )

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "mcp_server.server.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"name": "Test 0"})

    assert result.content[0].text == '[["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2"],[{"name":"Test 0"}]]'
    fake_client.get_collection.assert_awaited_once_with(name=os.getenv("DOCUMENT_COLLECTION"))
    fake_collection.get.assert_awaited_once_with(
        where={"name": "Test 0"},
    )

@pytest.mark.asyncio
async def test_unit_fetch_document_by_id(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.get.return_value = GetResult(
        ids=[["0"]],
        documents=[["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2"]],
        metadatas=[[{"name": "Test 0"}]]
    )

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "mcp_server.server.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"document_id": "0"})

    assert result.content[0].text == '[["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2"],[{"name":"Test 0"}]]'
    fake_client.get_collection.assert_awaited_once_with(name=os.getenv("DOCUMENT_COLLECTION"))
    fake_collection.get.assert_awaited_once_with(
        ids=["0"]
    )

@pytest.mark.asyncio
async def test_unit_fetch_document_by_name_and_id():
    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"name":"Test 0", "document_id": "0"})
        
    assert result.content[0].text == "Exactly one of name and document_id is required."

@pytest.mark.asyncio
async def test_unit_fetch_document_by_neither_name_nor_id():
    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {})
        
    assert result.content[0].text == "Exactly one of name and document_id is required."
