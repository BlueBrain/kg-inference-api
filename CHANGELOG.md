# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.2] - 22/10/2024

- Modify inference_tools dependency to be installed from `knowledge-graph-inference`

## [0.5.1] - 09/07/2024

- Removed Resolvers from the forge configuration 

## [0.5.0] - 03/05/2024

- Move `api` directory one level up
- Install `python-dotenv` for environment variable management
- Upgrade python version to 3.9
- Add `base_path` environment variable to prefix URLs

## [0.4.0] - 03/04/2024

- API: Update inference library version to v0.1.3
- Server: Remove building of server in repository level (moved to Kubernetes/AWS)
- Docs: Removed docs from this repository, moved to https://bbpgitlab.epfl.ch/dke/apps/kg-inference-client
- Client: Removed client from this repository, moved to https://bbpgitlab.epfl.ch/dke/apps/kg-inference
 
## [0.3.7] - 19/02/2024

- API: Use new version of kg-inference library 0.1.2

## [0.3.6] - 09/02/2024

- API: Use new version of kg-inference library 0.1.1
- API: Add deployment on Dockerhub on tag

## [0.3.5] - 30/01/2024

- API: Removed endpoint for morphology image generation
- API: Target new version of inference library, which enables the specification of inference result sub-type

## [0.3.4] - 10/01/2024

- API: Add DPI parameter for Generate endpoint

## [0.3.3] - 10/12/2023

- SERVER: Add NGINX server to include caching
- API: Remove dataclasses, add rule to ignore in pylint config

## [0.3.2] - 08/12/2023

- API: Fix forge configuration

## [0.3.1] - 06/12/2023

- API: Add linting with `black` and `pylint`
- API: Improve performance of morphology image generation

## [0.3.0] - 24/11/2023

- API: Add sparql and es view default values
- API: Modify gitlab credentials
- API: Introduce new endpoint /generate/morphology-image to generate morphology thumbnails

## [0.2.15] - 20/09/2023

- API: Retrieve rule through ES view so that it is at the appropriate tag
- API: Return embedding model detail in dictionary format instead of list
- API: Remove rule input parameter payload field

## [0.2.12] - 15/08/2023

- API: Make /rules and /infer requests not run asynchronously
- API: Make server run with `gunicorn` instead of `uvicorn` and increase amount of workers/threads

## [0.2.11] - 19/07/2023

- API: Updated setup.py and removed requirements.txt

## [0.2.10] - 11/07/2023

- Added basic structure for documentation
- Removed kubernetes yaml files

## [0.2.9] - 03/07/2023

- Client: Heatmap and Score distribution in different sub-tabs
- Client: Similarity model score selection when running generalization by similarity rule
- Client: Update generalization by similarity input labels and description
- API: Updated rule view

## [0.2.8] - 27/06/2023

- Client: Display a histogram of the scores distribution attributed by similarity models for all
  inferred results

## [0.2.7] - 14/06/2023

- Client: Updated the retrieval of the neuron morphology selector to get public/thalamus data
  for the shape rule. Updated plot files in the assets for the new embeddings

## [0.2.6] - 02/06/2023

- Client: 2D Plot of neuron morphology embeddings, disabled neuron morphology id input

## [0.2.5] - 18/04/2023

- Client: Neuron Morphology related rules - Added a selector for neuron morphologies (instead of writing an id)
- Client: Neuron Morphology related rules - Choose models to run with checkboxes instead of
  ignoring models with a multi-select dropdown

## [0.2.4] - 31/03/2023

- Client: Adapt call to nexus-forge changes for downloading
- API: Enable premise checking when inferring

## [0.2.3] - 30/03/2023

- Client: Custom view for the generalize up/down rule
- API: Adapted library calls to changes in the library

## [0.2.2] - 22/03/2023

- Client: Changed Elastic search view in forge configuration
- Client: Increased Gunicorn timeout

## [0.2.1] - 21/03/2023

- Disabled verification of ssl certificate when requesting from the client to the API

## [0.2.0] - 20/03/2023

- Updated the forge config yaml file in order to use the aggregated elastic and sparql endpoints
- Created a forge datamodels instance
- When inferring, all input filters must be given in a single dictionary to the library, the premise checking will use
  this single dictionary of multiple input parameters
  (as opposed to the old implementation that called check premises for each input parameter)
- Updated Rule model to add a nexus link attribute
- Refactor getting environment variables: throws exception if a mandatory environment variable is missing
- Introduce frontend client (Dash)
- Minimize CI jobs

## [0.1.2] - 12/10/2022

- Add docker-compose.yaml configuration
- Add kubernetes configuration files
- Fix rule fetching when field is missing

## [0.1.1] - 12/07/2022

- Add CORS support and whitelisted URLs

## [0.1.0] - 25/03/2022

- Authentication method using BBP token
- Rules endpoint to get all data generalization rules (`/rules`) with several parameters (resource type, filters)
- Inference endpoint to get inferred resources (`/infer`) by providing rules and filter
- CI/CD implementation to deploy in BBP Kubernetes
- Authorization functionality in swagger documentation
- Metadata in swagger documentation
