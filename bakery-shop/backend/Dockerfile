FROM ghcr.io/astral-sh/uv:python3.10-trixie-slim
WORKDIR /app

COPY pyproject.toml uv.lock ./

CMD uv sync --frozen --no-install-project

COPY . .

CMD uv sync --frozen

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]