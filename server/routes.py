from fastapi import APIRouter, HTTPException, Body
from database import *
from models import *
import services as _services

router = APIRouter()


# ------------------ user ------------------
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
@router.get("/admins/menus")
async def get_menus():
    return await _services.get_menus()


@router.post("/admins/menus")
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
@router.get("/users/orders")
async def get_orders(username):
    return await _services.get_orders(username)


@router.post("/users/orders")
async def add_order(name: str = Body(...), food_name: str = Body(...)):
    return await _services.add_order(name, food_name)


@router.delete("/user/orders/{name}/{food_name}")
async def delete_order(name: str = Body(...), food_name: str = Body(...)):
    return await _services.delete_order(name, food_name)
