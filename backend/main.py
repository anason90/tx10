"""FastAPI application entry point."""
from fastapi import FastAPI

from . import models
from .api import land_owners, projects, sales, shareholders, units
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate Lifecycle API", version="0.1.0")

app.include_router(land_owners.router)
app.include_router(projects.router)
app.include_router(shareholders.router)
app.include_router(units.router)
app.include_router(sales.router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Real Estate Lifecycle API"}
