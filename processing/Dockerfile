FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

# Docling Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-install-project

COPY utils.py .
COPY server.py .

CMD ["uv", "run", "fastapi", "run", "server.py", "--port", "3100"]
