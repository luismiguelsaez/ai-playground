FROM python:3.11.14-trixie

RUN apt -y update && apt -y install git

RUN mkdir /app
WORKDIR /app

RUN pip install git+https://github.com/resemble-ai/chatterbox peft

