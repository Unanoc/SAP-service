FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /SAP-service
WORKDIR /SAP-service

ADD requirements.txt /SAP-service/
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /SAP-service/
