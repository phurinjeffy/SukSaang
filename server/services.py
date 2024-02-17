from fastapi import APIRouter, HTTPException
from database import *
from models import *

router = APIRouter()


@router.get("/users/")
async def get_users():
    try:
        users = []
        for username, user in root.users.items():
            users.append({"username": username, "password": user.password})
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register/")
async def register_customer(username: str, password: str):
    try:
        if username in root.users:
            raise HTTPException(status_code=400, detail="User already exists")
        customer = Customer(username, password)
        root.users[username] = customer
        connection.transaction_manager.commit()
        return {"message": "Customer registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login/")
async def login(username: str, password: str):
    if username in root.users:
        user = root.users[username]
        if user.password == password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
