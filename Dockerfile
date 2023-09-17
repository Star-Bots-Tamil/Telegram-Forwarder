FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

CMD ["poetry", "run", "forwarder"]
