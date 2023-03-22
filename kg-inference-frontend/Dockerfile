FROM debian:bullseye as base

RUN apt update && apt install -y \
    cmake  \
    libhdf5-dev  \
    pip \
    python3.9 \
    git && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
COPY ./frontend /code/frontend

WORKDIR /code

RUN pip install git+https://github.com/BlueBrain/nexus-forge
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/frontend"

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server", "--timeout", "90"]

EXPOSE 8050:8050

