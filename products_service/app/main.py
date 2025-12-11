
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from itertools import count

app = FastAPI(
    title="Products Service",
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

class Product(BaseModel):
    id: int
    name: str
    price: float

class ProductCreate(BaseModel):
    name: str
    price: float

_products: Dict[int, Product] = {}
_id_gen = count(1)

if not _products:
    p1 = Product(id=next(_id_gen), name="Demo Product 1", price=10.0)
    p2 = Product(id=next(_id_gen), name="Demo Product 2", price=20.0)
    _products[p1.id] = p1
    _products[p2.id] = p2

@app.get("/products", response_model=List[Product])
def list_products():
    return list(_products.values())

@app.post("/products", response_model=Product)
def create_product(payload: ProductCreate):
    pid = next(_id_gen)
    product = Product(id=pid, name=payload.name, price=payload.price)
    _products[pid] = product
    return product
