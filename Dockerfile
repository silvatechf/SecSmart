FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false && poetry install --only main

FROM python:3.11-slim
RUN useradd -m seclabs
USER seclabs
WORKDIR /app
COPY --from=builder /app /app
CMD ["python", "-m", "src.main"]
