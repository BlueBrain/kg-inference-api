# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
