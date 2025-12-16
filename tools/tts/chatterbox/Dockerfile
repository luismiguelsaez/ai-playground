FROM python:3.11.14-trixie

RUN apt -y update && apt -y install git

RUN mkdir /app
WORKDIR /app

RUN git clone https://github.com/resemble-ai/chatterbox

RUN cd chatterbox \
  && python -m pip install -e .
