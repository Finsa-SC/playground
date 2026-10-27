FROM python:3.12-slim
LABEL authors="silence-suzuka"

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv pip install --system --no-cache .

COPY app/ ./app/

EXPOSE 8100

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100"]