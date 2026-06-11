FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app
COPY tests ./tests

RUN pip install --no-cache-dir .

CMD ["uvicorn", "app.entrypoints.public:app", "--host", "0.0.0.0", "--port", "8000"]
