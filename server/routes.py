from fastapi import APIRouter, HTTPException, Body, Depends
from database import *
from models import *
from schemas import *
import services as _services

router = APIRouter()


# ------------------ user ------------------
@router.get("/users/me", response_model=UserBase)
async def read_users_me(current_user: User = Depends(_services.get_current_user)):
    return current_user


@router.get("/users/{username}")
async def get_user(username: str):
    return await _services.get_user(username)


@router.get("/users")
async def get_users():
    return await _services.get_users()


@router.post("/users")
async def create_user(username: str = Body(...), password: str = Body(...)):
    return await _services.create_user(username, password)


@router.delete("/users/{username}")
async def delete_user(username: str):
    return await _services.delete_user(username)


@router.post("/users/login")
async def login_user(username: str = Body(...), password: str = Body(...)):
    return await _services.login_user(username, password)


# ------------------ admin ------------------
@router.get("/admins/{username}")
async def get_admin(username: str):
    return await _services.get_admin(username)


@router.get("/admins")
async def get_admins():
    return await _services.get_admins()


@router.post("/admins")
async def create_admin(username: str = Body(...), password: str = Body(...)):
    return await _services.create_admin(username, password)


@router.delete("/admins/{username}")
async def delete_admin(username: str):
    return await _services.delete_admin(username)


@router.post("/admins/login")
async def login_admin(username: str = Body(...), password: str = Body(...)):
    return await _services.login_admin(username, password)


# ------------------ menu ------------------
@router.get("/menus")
async def get_menus():
    return await _services.get_menus()


@router.post("/menus")
async def add_menu(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    return await _services.add_menu(name, price, description, cost, type, ingredients)


# ------------------ order ------------------
@router.get("/users/{username}/orders")
async def get_orders(username: str):
    return await _services.get_orders(username)


@router.post("/users/{username}/orders")
async def add_order(username: str, food_name: str):
    return await _services.add_order(username, food_name)


@router.delete("/users/{username}/orders/{food_name}")
async def delete_order(username: str, food_name: str):
    return await _services.delete_order(username, food_name)
