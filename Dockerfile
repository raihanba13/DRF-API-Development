FROM python:3.9.2

ENV PYTHONBUFFERED 1

WORKDIR /raihan_app

ADD .  /raihan_app

COPY ./requirements.txt /raihan_app/requirements.txt

RUN pip install -r requirements.txt 

COPY . /raihan_app