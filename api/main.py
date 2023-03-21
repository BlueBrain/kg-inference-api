from fastapi import FastAPI
from api import config
from api.router import rules, inference
from fastapi.middleware.cors import CORSMiddleware

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
    version="0.1.2",
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

