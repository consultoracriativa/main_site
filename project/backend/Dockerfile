FROM python:3.10-alpine

# Packages required for Pillow
RUN apk update && \
    apk upgrade && \
    apk add --no-cache jpeg-dev zlib-dev && \
    apk add --no-cache --virtual .build-deps build-base linux-headers

WORKDIR workdir

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./project/ ./project
COPY ./scripts/ ./scripts


