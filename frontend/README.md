### Running locally with python:

Need: `cmake` and `hdf5` for `neurom`'s `morphio` dependency:
([see](https://morphio.readthedocs.io/en/latest/install.html))

Debian:

    sudo apt install cmake libhdf5-dev

Red Hat:

    sudo yum install cmake3.x86_64 hdf5-devel.x86_64

Mac OS:

    brew install hdf5 cmake

Then:

    python -m venv env_name
    source env_name/bin/activate
    env_name/bin/python -m pip install --upgrade pip
    env_name/bin/python -m pip install git+https://github.com/BlueBrain/nexus-forge
    env_name/bin/python -m pip install --no-cache-dir --upgrade -r ./requirements.txt
    env_name/bin/python frontend/app.py

### Running locally with docker: 

    docker build -t <image_name> .
    docker run -d -p 8050:8050 <image_name>

### Running locally with docker compose
`docker-compose.yml` at root of the repository: add gitlab username and gitlab token

    docker network create bluebrainatlas_default
    docker compose up 

Served on: [localhost:8050](localhost:8050)