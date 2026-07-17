import requests
import pytest
from testcontainers.compose import DockerCompose
from testcontainers.core.wait_strategies import CompositeWaitStrategy, LogMessageWaitStrategy

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    compose = DockerCompose("..", compose_file_name="docker-compose.yaml").waiting_for({
        "ollama": LogMessageWaitStrategy("🟢 Done!"),
        "processing-server": CompositeWaitStrategy(
            LogMessageWaitStrategy("Collections initialized successfully"),
            LogMessageWaitStrategy("Uvicorn running on http://0.0.0.0:3000")
        ),
        "mcp-server": LogMessageWaitStrategy("Uvicorn running on http://0.0.0.0:8080")
    })
    compose.start()

    def remove_compose():
        compose.stop()
    
    request.addfinalizer(remove_compose)

    requests.post(
        "http://localhost:3000/add_documents/",
        json={
            "collection_name": "document",
            "documents": ["This is a document about AI infrastructure."],
            "ids": ["0"],
            "metadatas": [{"name":"AI Infra"}]
        }
    )

    requests.post(
        "http://localhost:3000/add_documents/",
        json={
            "collection_name": "chunks",
            "documents": ["This is", "a document about", "AI infrastructure."],
            "ids": ["0", "1", "2"],
            "metadatas": [
                {"document_id": "0", "chunk_idx":0},
                {"document_id": "0", "chunk_idx":1},
                {"document_id": "0", "chunk_idx":2}
            ],
        }
    )
    