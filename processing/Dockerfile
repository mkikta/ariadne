FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

# Docling Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-install-project

RUN mkdir -p /app/processing
COPY __init__.py utils.py embeddings.py init_collections.py server.py /app/processing/

CMD ["sh", "-c", "uv run fastapi run processing/server.py --port 3000 & uv run python -m processing.init_collections && wait"]
