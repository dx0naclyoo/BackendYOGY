FROM python:3.12

WORKDIR /src

RUN apt-get update && \
    apt install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker -bind 0.0.0.0:8000


