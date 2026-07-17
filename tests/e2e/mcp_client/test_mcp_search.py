import pytest
import ast
from fastmcp import Client

ENDPOINT = "http://localhost:8080/mcp/"

@pytest.mark.asyncio
async def test_mcp_search():
    async with Client(ENDPOINT) as client:
        result = await client.call_tool("search", {"query": "AI"})
        
        chunks, metadata = ast.literal_eval(result.content[0].text)
        chunks = set(chunks)
        metadata = set([(m["document_id"], m["chunk_idx"]) for m in metadata])
                    
        assert "This is" in chunks
        assert "a document about" in chunks
        assert "AI infrastructure." in chunks

        assert ("0",0) in metadata
        assert ("0",1) in metadata
        assert ("0",2) in metadata


@pytest.mark.asyncio
async def test_mcp_search_filtered():
    async with Client(ENDPOINT) as client:
        result = await client.call_tool("search", {"query": "AI", "document_id": "0"})
        chunks, metadata = ast.literal_eval(result.content[0].text)
        chunks = set(chunks)
        metadata = set([(m["document_id"], m["chunk_idx"]) for m in metadata])
                    
        assert "This is" in chunks
        assert "a document about" in chunks
        assert "AI infrastructure." in chunks

        assert ("0",0) in metadata
        assert ("0",1) in metadata
        assert ("0",2) in metadata
