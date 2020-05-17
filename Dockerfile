FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /sap
WORKDIR /sap

ADD requirements.txt /sap
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /sap/
