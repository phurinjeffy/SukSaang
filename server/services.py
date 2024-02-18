import jwt
from fastapi import HTTPException, Body
from database import connection
from models import Customer
from datetime import datetime, timedelta

# Secret key for JWT token encoding and decoding
SECRET_KEY = "secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

# ----------------- customer -----------------------
def create_access_token(username: str):
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": username, "exp": expiration_time}
    encoded_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token

async def register_customer(username: str, password: str):
    try:
        if username in connection.root.customers:
            raise HTTPException(status_code=400, detail="User already exists")
        customer = Customer(username, password)
        connection.root.customers[username] = customer
        connection.transaction_manager.commit()
        access_token = create_access_token(username)  # Generate JWT token
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def login_customer(username: str = Body(...), password: str = Body(...)):
    if username in connection.root.customers:
        user = connection.root.customers[username]
        if user.password == password:
            access_token = create_access_token(username)  # Generate JWT token
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


# ------------------ admin ------------------------
async def register_admin(username: str, password: str):
    try:
        if username in connection.root.admins:
            raise HTTPException(status_code=400, detail="User already exists")
        customer = Customer(username, password)
        connection.root.admins[username] = customer
        connection.transaction_manager.commit()
        access_token = create_access_token(username)  # Generate JWT token
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def login_admin(username: str = Body(...), password: str = Body(...)):
    if username in connection.root.admins:
        user = connection.root.admins[username]
        if user.password == password:
            access_token = create_access_token(username)  # Generate JWT token
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
