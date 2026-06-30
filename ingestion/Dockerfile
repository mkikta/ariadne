FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-install-project

COPY utils.py .
COPY server.py .
COPY embeddings.py .

# Collection creation on startup.
COPY init_collections.py .

CMD ["sh", "-c", "uv run fastapi run server.py --port 3000 & uv run python init_collections.py && wait"]
