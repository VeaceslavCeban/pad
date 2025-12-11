from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict, List
from itertools import count

app = FastAPI(
    title="Users Service",
    version="1.0.0",
)

# ⚠ На время отладки можешь просто оставить ["*"]
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # будет проверять валидный e-mail

class UserCreate(BaseModel):
    name: str
    email: EmailStr

_users: Dict[int, User] = {}
_id_gen = count(1)

# демо-пользователь
if not _users:
    demo = User(id=next(_id_gen), name="Demo User", email="demo@example.com")
    _users[demo.id] = demo

@app.get("/users", response_model=List[User])
def list_users():
    return list(_users.values())

@app.post("/users", response_model=User)
def create_user(payload: UserCreate):
    uid = next(_id_gen)
    user = User(id=uid, name=payload.name, email=payload.email)
    _users[uid] = user
    return user
