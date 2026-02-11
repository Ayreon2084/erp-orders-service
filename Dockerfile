FROM python:3.13-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

WORKDIR /app

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install --only main --no-interaction --no-ansi

COPY . .

RUN chmod +x entrypoint.sh
CMD ["/bin/bash", "./entrypoint.sh"]