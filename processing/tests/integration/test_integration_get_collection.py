import re
import pytest
from chromadb.api.models.AsyncCollection import AsyncCollection
from processing import utils

@pytest.mark.asyncio
async def test_integration_success_get_collection(mocker):
    result = await utils.get_collection("document")
    assert isinstance(result, AsyncCollection)
    assert result.name == "document"

@pytest.mark.asyncio
async def test_integration_failure_get_collection():
    with pytest.raises(Exception, match=re.escape("Collection [typo] does not exist")):
        await utils.get_collection("typo")
