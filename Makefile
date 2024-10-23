SHELL := /bin/bash

build:  ## Build the Docker image
	docker compose --progress=plain build kg-inference-api

run: build  ## Run the application in Docker
	docker compose up --remove-orphans
