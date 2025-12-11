
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from itertools import count

app = FastAPI(
    title="Inventory Service",
    version="1.0.0",
)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int

_items: Dict[int, InventoryItem] = {}
_id_gen = count(1)

if not _items:
    i1 = InventoryItem(id=next(_id_gen), name="Demo Product 1", quantity=100)
    i2 = InventoryItem(id=next(_id_gen), name="Demo Product 2", quantity=50)
    _items[i1.id] = i1
    _items[i2.id] = i2

@app.get("/inventory", response_model=List[InventoryItem])
def list_inventory():
    return list(_items.values())
