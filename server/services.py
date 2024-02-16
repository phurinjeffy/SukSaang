from fastapi import FastAPI, HTTPException

import ZODB, ZODB.FileStorage
import transaction
from models import *
import BTrees
import uvicorn

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root
root.users = BTrees.OOBTree.BTree()

root.users["username"] = Customer(username="username", password="password")

app = FastAPI()

@app.get("/users/")
async def get_users():
    try:
        users = []
        for username, user in root.users.items():
            users.append({"username": username, "password": user.password})
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register/")
async def register_customer(username: str, password: str):
    try:
        with transaction.manager:
            if username in root.users:
                raise HTTPException(status_code=400, detail="User already exists")
            customer = Customer(username, password)
            root.users[username] = customer
            return {"message": "Customer registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login/")
async def login(username: str, password: str):
    if username in root.users:
        user = root.users[username]
        if user.password == password:
            return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)