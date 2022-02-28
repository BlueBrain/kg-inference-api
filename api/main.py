import uvicorn
from fastapi import FastAPI
from starsessions import SessionMiddleware, InMemoryBackend
from api.router import rules, inference

app = FastAPI(debug=True)

app.add_middleware(SessionMiddleware, backend=InMemoryBackend(), autoload=True)

app.include_router(rules.router, prefix="/rules")
app.include_router(inference.router, prefix="/infer")