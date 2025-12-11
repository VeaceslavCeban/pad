
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from itertools import count

app = FastAPI(
    title="Orders Service",
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

class Order(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]
    total: float

class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]
    total: float

_orders: Dict[int, Order] = {}
_id_gen = count(1)

@app.get("/orders", response_model=List[Order])
def list_orders():
    return list(_orders.values())

@app.post("/orders", response_model=Order)
def create_order(payload: OrderCreate):
    oid = next(_id_gen)
    order = Order(
        id=oid,
        user_id=payload.user_id,
        product_ids=payload.product_ids,
        total=payload.total,
    )
    _orders[oid] = order
    return order
