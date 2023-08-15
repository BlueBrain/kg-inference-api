import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import config
from api.router import rules, inference
from fastapi.logger import logger as fastapi_logger

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

app = FastAPI(
    title="KG Inference API",
    debug=config.DEBUG_MODE,
    version="0.2.2",
    openapi_tags=tags_metadata
)


whitelisted_cors_urls = list(config.WHITELISTED_CORS_URLS.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelisted_cors_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rules.router, prefix="/rules")
app.include_router(inference.router, prefix="/infer")


# logging
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

fastapi_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.setLevel(logging.DEBUG)
