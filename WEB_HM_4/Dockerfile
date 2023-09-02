FROM tiangolo/uvicorn-gunicorn:python3.10-slim AS build-env

WORKDIR /app/
# set envierment variables
ENV PYTHONDONTWRYTEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies


COPY . /app/



CMD ["python3", "main:app"]