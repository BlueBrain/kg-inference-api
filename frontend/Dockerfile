FROM debian:bullseye as base

RUN apt update && apt install -y \
    cmake  \
    libhdf5-dev  \
    pip \
    python3.9 \
    git && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY . /code

RUN pip install -e .

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/frontend"

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server", "--timeout", "90"]

EXPOSE 8050:8050

