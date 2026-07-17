import os
import pytest
from unittest.mock import AsyncMock
from fastmcp import Client
from mcp_server.server import mcp
from chromadb.api.types import QueryResult

@pytest.mark.asyncio
async def test_unit_search(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.query.return_value = QueryResult(
        ids=[["0"]],
        documents=[["Test 0 chunk 0"]],
        metadatas=[[{"document_id": "0", "chunk_idx": 0}]]
    )

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "mcp_server.server.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk"})

    assert result.content[0].text == '[["Test 0 chunk 0"],[{"document_id":"0","chunk_idx":0}]]'
    fake_client.get_collection.assert_awaited_once_with(name=os.getenv("CHUNKS_COLLECTION"))
    fake_collection.query.assert_awaited_once_with(
        query_texts=["chunk"],
        n_results=10,
    )

@pytest.mark.asyncio
async def test_unit_search_multiple(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.query.return_value = QueryResult(
        ids=[["0","1","2"]],
        documents=[["Test 0 chunk 0", "Test 0 chunk 1", "Test 0 chunk 2"]],
        metadatas=[[{"document_id": "0", "chunk_idx": 0}, {"document_id": "0", "chunk_idx": 1}, {"document_id": "0", "chunk_idx": 2}]]
    )

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "mcp_server.server.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk"})

    assert result.content[0].text == '[["Test 0 chunk 0","Test 0 chunk 1","Test 0 chunk 2"],[{"document_id":"0","chunk_idx":0},{"document_id":"0","chunk_idx":1},{"document_id":"0","chunk_idx":2}]]'
    fake_client.get_collection.assert_awaited_once_with(name=os.getenv("CHUNKS_COLLECTION"))
    fake_collection.query.assert_awaited_once_with(
        query_texts=["chunk"],
        n_results=10,
    )

@pytest.mark.asyncio
async def test_unit_search_filtered(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.query.return_value = QueryResult(
        ids=[["0"]],
        documents=[["Test 0 chunk 0"]],
        metadatas=[[{"document_id": "0", "chunk_idx": 0}]]
    )

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "mcp_server.server.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk", "document_id": "0"})

    assert result.content[0].text == '[["Test 0 chunk 0"],[{"document_id":"0","chunk_idx":0}]]'
    fake_client.get_collection.assert_awaited_once_with(name=os.getenv("CHUNKS_COLLECTION"))
    fake_collection.query.assert_awaited_once_with(
        query_texts=["chunk"],
        n_results=10,
        where= {"document_id": "0"},
    )

@pytest.mark.asyncio
async def test_unit_search_filtered_no_results(mocker):
    fake_collection = AsyncMock()

    fake_client = AsyncMock()
    fake_client.get_collection.return_value = fake_collection
    fake_collection.query.return_value = QueryResult(
        ids=[[]],
        documents=[[]],
        metadatas=[[]]
    )

    async_http_client = AsyncMock(return_value=fake_client)
    mocker.patch(
        "mcp_server.server.chromadb.AsyncHttpClient",
        new=async_http_client,
    )

    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk", "document_id": "1"})

    assert result.content[0].text == '[[],[]]'
    fake_client.get_collection.assert_awaited_once_with(name=os.getenv("CHUNKS_COLLECTION"))
    fake_collection.query.assert_awaited_once_with(
        query_texts=["chunk"],
        n_results=10,
        where= {"document_id": "1"},
    )
