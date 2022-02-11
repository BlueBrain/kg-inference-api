from fastapi import FastAPI

from router import rules

app = FastAPI(debug=True)


app.include_router(rules.router, prefix="/rules")
