FROM python:3.8

ARG GITLAB_USERNAME
ARG GITLAB_TOKEN

WORKDIR /code
COPY . /code

RUN pip install -e .

RUN pip install git+https://${GITLAB_USERNAME}:${GITLAB_TOKEN}@bbpgitlab.epfl.ch/dke/apps/kg-inference

EXPOSE 8080:8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
