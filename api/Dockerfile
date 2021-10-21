FROM python:3.9

ENV PYTHONPATH /ultimate_procrastination

WORKDIR /Phone_number_api

COPY api /Phone_number_api/api
COPY database.py /Phone_number_api/
COPY requirements.txt /Phone_number_api/
COPY alembic /Phone_number_api/alembic
COPY alembic.ini /Phone_number_api/alembic.ini

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install -r /Phone_number_api/requirements.txt