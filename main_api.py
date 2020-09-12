from typing import Optional
from db import DB
from fastapi import FastAPI

app = FastAPI()
db = DB()


@app.get("/stations/type")
def read_root():
    return db.get_station_types()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}