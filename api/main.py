import os
import uvicorn
from fastapi import FastAPI
from starsessions import SessionMiddleware, InMemoryBackend
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
    version="0.1.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    SessionMiddleware,
    backend=InMemoryBackend(),
    autoload=True
)

whitelisted_cors_urls = list(os.environ.get('WHITELISTED_CORS_URLS', '').split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelisted_cors_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rules.router, prefix="/rules")
app.include_router(inference.router, prefix="/infer")


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8080, reload=True)
