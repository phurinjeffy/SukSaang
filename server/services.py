import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Body, status
from database import connection
from models import *
from datetime import datetime, timedelta

# ------------------ token ------------------------
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(username: str):
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": username, "exp": expiration_time}
    encoded_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


# ------------------ user ------------------------
async def create_user(username: str = Body(...), password: str = Body(...)):
    try:
        if username in connection.root.users:
            raise ValueError("User already exists")

        user = User(username, password)
        connection.root.users[username] = user
        connection.transaction_manager.commit()

        access_token = create_access_token(username)  # Generate JWT token
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )


async def login_user(username: str = Body(...), password: str = Body(...)):
    if username in connection.root.users:
        user = connection.root.users[username]
        if user.password == password:
            access_token = create_access_token(username)  # Generate JWT token
            return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )


# ------------------ admin ------------------------
async def create_admin(username: str = Body(...), password: str = Body(...)):
    try:
        if username in connection.root.admins:
            raise ValueError("Admin already exists")

        admin = Admin(username, password)
        connection.root.admins[username] = admin
        connection.transaction_manager.commit()

        access_token = create_access_token(username)  # Generate JWT token
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create admin",
        )


async def login_admin(username: str = Body(...), password: str = Body(...)):
    if username in connection.root.admins:
        user = connection.root.admins[username]
        if user.password == password:
            access_token = create_access_token(username)  # Generate JWT token
            return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
