ARG PYTHON_VERSION=3.9
ARG PYTHON_BASE=${PYTHON_VERSION}-slim

FROM python:$PYTHON_BASE
SHELL ["bash", "-e", "-x", "-o", "pipefail", "-c"]

ARG REQUIRED_PACKAGES="supervisor nginx git"
ARG OPTIONAL_PACKAGES="vim less curl jq htop strace net-tools iproute2 psmisc procps"

RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    ca-certificates \
    ${REQUIRED_PACKAGES} \
    ${OPTIONAL_PACKAGES}
apt-get clean
rm -rf /var/lib/apt/lists/*
EOT

COPY ./nginx/ /etc/nginx/
COPY ./supervisord.conf /etc/supervisor/supervisord.conf

WORKDIR /code
COPY . /code/api

RUN pip install -e ./api

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}/code/api"

STOPSIGNAL SIGINT
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
