FROM python:3.9

WORKDIR /code
COPY . /code/api

RUN pip install -e ./api

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api"

CMD gunicorn api.main:app --workers 5 --threads 1 --bind 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker --timeout 250
