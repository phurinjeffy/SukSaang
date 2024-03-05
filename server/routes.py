from fastapi import APIRouter, HTTPException, Body, Depends
from database import *
from models import *
from schemas import *
import services as _services
from typing import Optional

router = APIRouter()


# ------------------ user ------------------
@router.get("/users/me", response_model=UserBase)
async def get_current_user(current_user: User = Depends(_services.get_current_user)):
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
@router.get("/admins/me", response_model=AdminBase)
async def get_current_admin(current_admin: Admin = Depends(_services.get_current_admin)):
    return current_admin


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
@router.get("/menus/{menu_item}")
async def get_menu(menu_item: str):
    return await _services.get_menu(menu_item)


@router.get("/menus")
async def get_menus():
    return await _services.get_menus()


@router.post("/menus")
async def add_menu(
    category: str = Body(...),
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    type: str = Body(...),
    cost: int = Body(...),
    ingredients: list = Body(...),
    sweetness: int = Body(...)
):
    return await _services.add_menu(category, name, price, description, type, cost, ingredients, sweetness)


@router.patch("/menus/{food_name}")
async def edit_menu(
    food_name: str,
    category: Optional[str] = None,
    name: Optional[str] = None,
    price: Optional[int] = None,
    description: Optional[str] = None,
    type: Optional[str] = None,
    cost: Optional[int] = None,
    ingredients: Optional[list] = None,
    sweetness: Optional[int] = None
):
    return await _services.edit_menu(food_name, category, name, price, description, type, cost, ingredients, sweetness)


@router.delete("/menus/{food_name}")
async def delete_menu(food_name: str):
    return await _services.delete_menu(food_name)

# ------------------ order ------------------
@router.get("/users/{username}/orders")
async def get_orders(username: str):
    return await _services.get_orders(username)


@router.post("/users/{username}/orders")
async def add_order(username: str, food_name: str, quantity: int):
    return await _services.add_order(username, food_name, quantity)


@router.delete("/users/{username}/orders/{food_name}")
async def delete_order(username: str, food_name: str, quantity: int):
    return await _services.delete_order(username, food_name, quantity)


#------------------ Table ----------------------
@router.get("/tables/")
async def get_tables():
    return await _services.get_tables()


@router.post("/tables/")
async def add_table(table_num : int):
    return await _services.add_table(table_num)


@router.post("/tables/{table_num}/customers")
async def add_table_customer(table_num: int, user: str = Body(...)):
    return await _services.add_table_customer(table_num, user)


@router.get("/tables/{table_num}/customers")
async def show_table_customer(table_num: int):
    return await _services.show_table_customer(table_num)


@router.get("/tables/{table_num}/orders")
async def show_table_orders(table_num: int):
    return await _services.show_table_orders(table_num)


@router.get("/table/{table_num}/payment")
async def show_table_payment(table_num: int):
    return await _services.show_table_payment(table_num)
