FROM python:3.12

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/db/alembic alembic
COPY app/db/alembic.ini alembic.ini

COPY template template

COPY pyproject.toml .

COPY app ./app

COPY tests ./tests
