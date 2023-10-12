FROM python:3.8

ARG GITLAB_USERNAME
ARG GITLAB_TOKEN

WORKDIR /code
COPY ./api /code/api
COPY version.py /code

RUN pip install -e ./api

EXPOSE 8080:8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api/api"

CMD gunicorn main:app --workers 5 --threads 1 --bind 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker --timeout 250
