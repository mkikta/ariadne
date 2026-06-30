FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-install-project

COPY server.py .

CMD ["uv", "run", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
