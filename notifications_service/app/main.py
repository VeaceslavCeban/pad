
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Notifications Service",
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

class Notification(BaseModel):
    recipient: str
    message: str

_queue: List[Notification] = []

@app.get("/notifications", response_model=List[Notification])
def list_notifications():
    return _queue

@app.post("/notifications", response_model=Notification)
def send_notification(payload: Notification):
    _queue.append(payload)
    return payload
