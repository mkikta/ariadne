import pytest
from fastmcp import Client

ENDPOINT = "http://localhost:8080/mcp/"


@pytest.mark.asyncio
async def test_mcp_fetch_document_by_name():
    async with Client(ENDPOINT) as client:
        result = await client.call_tool("fetch_document", {"name": "AI Infra"})
        assert result.content[0].text == '["This is a document about AI infrastructure.",{"name":"AI Infra"}]'


@pytest.mark.asyncio
async def test_mcp_search_document_by_id():
    async with Client(ENDPOINT) as client:
        result = await client.call_tool("fetch_document", {"document_id": "0"})
        assert result.content[0].text == '["This is a document about AI infrastructure.",{"name":"AI Infra"}]'

@pytest.mark.asyncio
async def test_mcp_search_document_by_name_and_id():
    async with Client(ENDPOINT) as client:
        result = await client.call_tool("fetch_document", {"name": "AI Infra", "document_id": "0"})
        assert result.content[0].text == "Exactly one of name and document_id is required."


@pytest.mark.asyncio
async def test_mcp_search_document_by_neither_name_nor_id():
    async with Client(ENDPOINT) as client:
        result = await client.call_tool("fetch_document", {})
        assert result.content[0].text == "Exactly one of name and document_id is required."

