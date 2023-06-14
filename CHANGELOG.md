# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
