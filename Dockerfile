FROM python:3.7

ARG GITLAB_USERNAME
ARG GITLAB_TOKEN

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install git+https://${GITLAB_USERNAME}:${GITLAB_TOKEN}@bbpgitlab.epfl.ch/dke/apps/kg-inference

COPY ./api /app/api

EXPOSE 8080:8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]