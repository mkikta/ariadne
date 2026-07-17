import os
import pytest
import asyncio
from processing import utils
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy

chroma = (
    DockerContainer("chromadb/chroma:1.5.9")
    .with_exposed_ports(8000)
)

current_dir = os.path.abspath(os.path.dirname(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
ollama_data_path = os.path.join(current_dir, "ollama")
serve_script_path = os.path.join(repo_root, "llm", "serve_model.sh")

ollama = (
    DockerContainer("ollama/ollama:0.31.0", entrypoint=["sh", "/serve_model.sh"])
    .with_exposed_ports(11434)
    .with_env("MODEL", os.getenv("MODEL", "qwen3-embedding:0.6b"))
    .with_volume_mapping(ollama_data_path, "/root/.ollama", mode="rw")
    .with_volume_mapping(serve_script_path, "/serve_model.sh", mode="rw")
    .waiting_for(LogMessageWaitStrategy("🟢 Done!"),)
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
