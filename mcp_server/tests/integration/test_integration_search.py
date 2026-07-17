import pytest
import ast
from mcp_server.server import mcp
from fastmcp import Client

@pytest.mark.asyncio
async def test_integration_search():

    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk"})
    
    chunks, metadata = ast.literal_eval(result.content[0].text)
    chunks = set(chunks)
    metadata = set([(m["document_id"], m["chunk_idx"]) for m in metadata])
                   
    assert "Test 0 chunk 0" in chunks
    assert "Test 0 chunk 1" in chunks
    assert "Test 0 chunk 2" in chunks

    assert ("0",0) in metadata
    assert ("0",1) in metadata
    assert ("0",2) in metadata
    
@pytest.mark.asyncio
async def test_integration_search_filtered():
    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk", "document_id": "0"})
    
    chunks, metadata = ast.literal_eval(result.content[0].text)
    chunks = set(chunks)
    metadata = set([(m["document_id"], m["chunk_idx"]) for m in metadata])
                   
    assert "Test 0 chunk 0" in chunks
    assert "Test 0 chunk 1" in chunks
    assert "Test 0 chunk 2" in chunks

    assert ("0",0) in metadata
    assert ("0",1) in metadata
    assert ("0",2) in metadata

    
@pytest.mark.asyncio
async def test_integration_search_filtered_no_results():
    async with Client(mcp) as client:
        result =  await client.call_tool("search", {"query": "chunk", "document_id": "1"})

    assert result.content[0].text == "[[],[]]"
