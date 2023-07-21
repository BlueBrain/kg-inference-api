FROM debian:bullseye as base

RUN apt update && apt install -y \
    cmake  \
    libhdf5-dev  \
    pip \
    python3.9 \
    git && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY ./frontend /code/frontend
COPY version.py /code

RUN pip install -e ./frontend

EXPOSE 8050:8050

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/frontend/frontend"

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server", "--timeout", "90"]


