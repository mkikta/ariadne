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
    })
    compose.start()

    def remove_compose():
        compose.stop()

    request.addfinalizer(remove_compose)
