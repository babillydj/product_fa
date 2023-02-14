from typing import Dict
from fastapi import FastAPI

from app.api.api_v1 import product
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(product.router)


@app.get("/")
def read_root() -> Dict[str, str]:
    """open root"""
    return {"Hello": "World"}
