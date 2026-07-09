import os
import re
import pytest
import asyncio
from testcontainers.core.container import DockerContainer
from chromadb.api.models.AsyncCollection import AsyncCollection
from processing import utils


container = (
    DockerContainer("chromadb/chroma:latest")
    .with_exposed_ports(8000)
)


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    container.start()

    def remove_container():
        container.stop()

    request.addfinalizer(remove_container)
    os.environ["CHROMA_HOST"] = container.get_container_host_ip()
    os.environ["CHROMA_PORT"] = str(container.get_exposed_port(8000))
    asyncio.run(utils.create_collection("document"))


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    pass

@pytest.mark.asyncio
async def test_integration_success_get_collection(mocker):
    result = await utils.get_collection("document")
    assert isinstance(result, AsyncCollection)
    assert result.name == "document"

@pytest.mark.asyncio
async def test_integration_failure_get_collection():
    with pytest.raises(Exception, match=re.escape("Collection [typo] does not exist")):
        await utils.get_collection("typo")
