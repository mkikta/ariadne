import os
import pytest
import chromadb
from dotenv import load_dotenv
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy


load_dotenv()

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
    ollama_data_path = os.path.join(current_dir, "ollama")
    serve_script_path = os.path.join(repo_root, "llm", "serve_model.sh")

    chroma = (
        DockerContainer("chromadb/chroma:1.5.9")
        .with_exposed_ports(8000)
    )

    ollama = (
        DockerContainer("ollama/ollama:0.31.0", entrypoint=["sh", "/serve_model.sh"])
        .with_exposed_ports(11434)
        .with_env("MODEL", os.getenv("MODEL", "qwen3-embedding:0.6b"))
        .with_volume_mapping(ollama_data_path, "/root/.ollama", mode="rw")
        .with_volume_mapping(serve_script_path, "/serve_model.sh", mode="rw")
        .waiting_for(LogMessageWaitStrategy("🟢 Done!"),)
    )

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
    os.environ["OLLAMA_HOST"] = ollama.get_container_host_ip()
    os.environ["OLLAMA_PORT"] = str(ollama.get_exposed_port(11434))

    client = chromadb.HttpClient(
        host=os.getenv("CHROMA_HOST"), port=int(os.getenv("CHROMA_PORT"))
    )
    client.create_collection("document")
    embedding_function =  OllamaEmbeddingFunction(
        url=f"http://{os.getenv("OLLAMA_HOST")}:{os.getenv("OLLAMA_PORT")}",
        model_name=os.getenv("MODEL"),
    )
    client.create_collection("chunks", embedding_function=embedding_function)

    doc_collection = client.get_collection("document")
    chunks_collection = client.get_collection("chunks")

    doc_collection.add(
        ids=["0"],
        documents=["Test 0 chunk 0 Test 0 chunk 1 Test 0 chunk 2"],
        metadatas=[{"name": "Test 0"}]
    )

    chunks_collection.add(
        ids=["0","1","2"],
        documents=["Test 0 chunk 0", "Test 0 chunk 1", "Test 0 chunk 2"],
        metadatas=[{"document_id": "0", "chunk_idx": 0}, {"document_id": "0", "chunk_idx": 1}, {"document_id": "0", "chunk_idx": 2}]
    )
