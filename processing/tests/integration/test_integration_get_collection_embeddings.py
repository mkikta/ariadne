import os
import re
import pytest
import asyncio
from testcontainers.core.container import DockerContainer
from chromadb.api.models.AsyncCollection import AsyncCollection
from processing import utils

chroma = (
    DockerContainer("chromadb/chroma:latest")
    .with_exposed_ports(8000)
)

current_dir = os.path.abspath(os.path.dirname(__file__))
ollama_data_path = os.path.join(current_dir, "ollama")
serve_script_path = os.path.join(current_dir, "llm", "serve_model.sh")

ollama = (
        DockerContainer("ollama/ollama:0.31.0")
        .with_exposed_ports(11434)
        .with_env("MODEL", os.getenv("MODEL", "qwen3-embedding:0.6b")) 
        .with_bind_ports(11434, 11434) 
        .with_volume_mapping(ollama_data_path, "/root/.ollama", mode="rw")
        .with_volume_mapping(serve_script_path, "/serve_model.sh", mode="rw")
    )
    

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    chroma.start()
    ollama.start()

    def remove_chroma():
        chroma.stop()

    def remove_ollama():
        ollama.stop()

    request.addfinalizer(remove_chroma)
    request.addfinalizer(remove_ollama)

    os.environ["CHROMA_HOST"] = chroma.get_container_host_ip()
    os.environ["CHROMA_PORT"] = str(chroma.get_exposed_port(8000))
    asyncio.run(utils.create_collection("document"))
    asyncio.run(utils.create_collection(
        "chunks",
        embedding_backend="ollama",
        model_name="qwen3-embedding:0.6b",
        embedding_host=ollama.get_container_host_ip(),
        embedding_port=str(ollama.get_exposed_port(11434)),
    ))

@pytest.fixture(scope="function", autouse=True)
def setup_data():
    pass

@pytest.mark.asyncio
async def test_integration_success_get_collection():
    result = await utils.get_collection("document")
    assert isinstance(result, AsyncCollection)
    assert result.name == "document"

@pytest.mark.asyncio
async def test_integration_failure_get_collection():
    with pytest.raises(Exception, match=re.escape("Collection [typo] does not exist")):
        await utils.get_collection("typo")
