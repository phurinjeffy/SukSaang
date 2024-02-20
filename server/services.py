import jwt
from fastapi import HTTPException, Body, status
from database import connection
from models import *
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


async def register_customer(username: str = Body(...), password: str = Body(...)):
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
async def register_admin(username: str = Body(...), password: str = Body(...)):
    try:
        if username in connection.root.admins:
            raise HTTPException(status_code=400, detail="User already exists")
        admin = Admin(username, password)
        connection.root.admins[username] = admin
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

# ------------------------ menu Admin -----------------------

async def add_memu_admin(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    try:
        if name in connection.root.menus:
            raise HTTPException(status_code=400, detail="Menu already exists")
        dish = MainDish(name, price, description, cost, type, ingredients)
        connection.root.menus[name] = dish
        connection.transaction_manager.commit()
        return {"message": "Menus registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------ order User -----------------------

async def add_order_user( 
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
    sweetness: str = Body(...)
):
    try:
        if name in connection.root.orders:
            raise ValueError("Name already exists")
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))