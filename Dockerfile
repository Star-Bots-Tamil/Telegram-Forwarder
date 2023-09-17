FROM python:3.10-slim-bullseye

WORKDIR /app

RUN pip install poetry && pip3 install pysocks
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

CMD ["poetry", "run", "forwarder"]
