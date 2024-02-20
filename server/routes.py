from fastapi import APIRouter, HTTPException, Body
from database import *
from models import *
import services as _services

router = APIRouter()


# ------------------ user ------------------
@router.get("/users/{username}")
async def get_user(username: str):
    return await _services.get_user(username)


@router.get("/users/")
async def get_users():
    return await _services.get_users()


@router.post("/register/")
async def create_user(username: str = Body(...), password: str = Body(...)):
    return await _services.create_user(username, password)


@router.delete("/users/{username}")
async def delete_user(username: str):
    return await _services.delete_user(username)


@router.post("/login/")
async def login_user(username: str = Body(...), password: str = Body(...)):
    return await _services.login_user(username, password)


# ------------------ admin ------------------
@router.get("/admin/{username}")
async def get_admin(username: str):
    return await _services.get_admin(username)


@router.get("/admin/")
async def get_admins():
    return await _services.get_admins()


@router.post("/admin/register/")
async def create_admin(username: str = Body(...), password: str = Body(...)):
    return await _services.create_admin(username, password)


@router.delete("/admin/{username}")
async def delete_admin(username: str):
    return await _services.delete_admin(username)


@router.post("/admin/login/")
async def login_admin(username: str = Body(...), password: str = Body(...)):
    return await _services.login_admin(username, password)


# ------------------ menu ------------------
@router.get("/admin/menus/")
async def get_menus():
    return await _services.get_menus()


@router.post("/menu/")
async def add_menu(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    return await _services.add_menu(name, price, description, cost, type, ingredients)


# ------------------ food ------------------
@router.post("/food/")
async def add_food(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    pass
