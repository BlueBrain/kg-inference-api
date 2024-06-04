"""
Module: main.py

This module initializes a FastAPI application for the KG Inference API, configures middleware, includes routers,
and sets up logging.

Initialization Steps:
    1. Import necessary modules and packages (logging, FastAPI, middleware, configuration, routers).
    2. Set up metadata for API tags.
    3. Create a FastAPI application instance with specified title, debug mode, version, and tags.
    4. Configure CORS middleware with whitelisted URLs.
    5. Include routers for rules, inference.
    6. Configure logging for Gunicorn, UVicorn, and FastAPI.

"""

import logging
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger as fastapi_logger
from api import config
from api.router import rules, inference

# Metadata for API tags
tags_metadata = [
    {
        "name": "Rules",
        "description": "Operations related to retrieving rules",
    },
    {
        "name": "Inference",
        "description": "Operations related to inferring resources from the knowledge graph",
    },
]

# FastAPI application instance
app = FastAPI(
    title="KG Inference API",
    debug=config.DEBUG_MODE,
    version="0.5.0",
    openapi_tags=tags_metadata,
    docs_url=f"{config.BASE_PATH}/docs",
)

# Whitelisted CORS URLs
whitelisted_cors_urls = list(config.WHITELISTED_CORS_URLS.split(","))

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelisted_cors_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_router = APIRouter(prefix=config.BASE_PATH)

# Include routers
base_router.include_router(rules.router, prefix="/rules")
base_router.include_router(inference.router, prefix="/infer")

app.include_router(base_router)

# Logging configuration
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

fastapi_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.setLevel(logging.DEBUG)
