FROM python:3.7

ARG GITLAB_USERNAME
ARG GITLAB_TOKEN

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y iputils-ping

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install git+https://${GITLAB_USERNAME}:${GITLAB_TOKEN}@bbpgitlab.epfl.ch/dke/apps/kg-inference

COPY ./api /code/api

EXPOSE 8080:8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
