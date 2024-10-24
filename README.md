# KG Inference API

The KG Inference API is designed to infer morphologies based on various input characteristics. This API leverages knowledge graphs and inference techniques to provide insights into the structure and form of entities within a defined context.


## Installation

1. Clone the repository:

```bash
git clone https://github.com/BlueBrain/kg-inference-api.git
cd kg-inference-API
```

2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install .
```

4. Run the API:

```bash
uvicorn main:app --reload
```

## Usage

Once the API is running, you can access the Swagger UI at `http://localhost:8000/docs` to explore the endpoints and test the inference functionality.


## Acknowledgements

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

For license and authors, see LICENSE.txt and AUTHORS.txt respectively.

Copyright &copy; 2022-2024 Blue Brain Project/**EPFL**