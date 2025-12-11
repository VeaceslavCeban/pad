
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Payments Service",
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

class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    method: str

class PaymentResponse(BaseModel):
    status: str
    message: str

@app.post("/payments", response_model=PaymentResponse)
def process_payment(payload: PaymentRequest):
    return PaymentResponse(
        status="success",
        message=f"Оплата {payload.amount} принята методом {payload.method} для заказа {payload.order_id}",
    )
