import pytest
from mcp_server.server import mcp
from fastmcp import Client

@pytest.mark.asyncio
async def test_integration_fetch_document_by_name():
    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"name": "Test 0"})

    assert result.content[0].text == '["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2",{"name":"Test 0"}]'

@pytest.mark.asyncio
async def test_integration_fetch_document_by_id():
    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"document_id": "0"})

    assert result.content[0].text == '["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2",{"name":"Test 0"}]'

@pytest.mark.asyncio
async def test_integration_fetch_document_by_name_no_results():
    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"document_id": "1"})

    assert result.content == []

@pytest.mark.asyncio
async def test_integration_fetch_document_by_id_no_results():
    async with Client(mcp) as client:
        result =  await client.call_tool("fetch_document", {"document_id": "1"})

    assert result.content == []
