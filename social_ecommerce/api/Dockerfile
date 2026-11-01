FROM python:3.13-slim
LABEL authors="silence-suzuka"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv

RUN uv pip install --system --no-cache .

COPY app/ ./app/

EXPOSE 3000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]