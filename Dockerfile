FROM python:3.12

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cashe-dir --upgrade -r requirements.txt



CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
