FROM python:3.9

WORKDIR /Phone_number_api

COPY . .

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip3 install -r /Phone_number_api/requirements.txt