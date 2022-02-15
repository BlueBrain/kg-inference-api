from fastapi import FastAPI
from starsessions import SessionMiddleware, InMemoryBackend
from router import rules

app = FastAPI(debug=True)

app.add_middleware(SessionMiddleware, backend=InMemoryBackend(), autoload=True)

app.include_router(rules.router, prefix="/rules")
