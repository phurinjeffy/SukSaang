from fastapi import APIRouter, HTTPException, Body
from database import *
from models import *
import services as _services

router = APIRouter()


# ------------------ user ------------------
@router.get("/users/")
async def get_users():
    return await _services.get_users()


@router.post("/register/")
async def create_user(username: str = Body(...), password: str = Body(...)):
    return await _services.create_user(username, password)


@router.post("/login/")
async def login_user(username: str = Body(...), password: str = Body(...)):
    return await _services.login_user(username, password)


# ------------------ admin ------------------
@router.get("/admin/")
async def get_admins():
    return await _services.get_admins()


@router.post("/admin/register/")
async def create_admin(username: str = Body(...), password: str = Body(...)):
    return await _services.create_admin(username, password)


@router.post("/admin/login/")
async def login_admin(username: str = Body(...), password: str = Body(...)):
    return await _services.login_admin(username, password)


# ------------------ menu ------------------
@router.get("/admin/menus/")
async def get_menu():
    return await _services.get_menus()


@router.post("/menu/")
async def add_menu(name: str = Body(...), price: int = Body(...), description: str = Body(...), cost: int = Body(...),type: str = Body(...),ingredients: list = Body(...)):
    return await _services.add_menu(name, price, description, cost, type , ingredients)

# not support item deletion
# @router.delete("/deletemenu")
# async def delete_menu(name: str):
#     return await _services.delete_menu(name)

#-----------------------order---------------------

@router.get("/getorder/")
async def get_user_order(username: str):
    return await _services.get_user_order(username)


@router.post("/addorder/")
async def add_food(
    name: str = Body(...),
    food_name: str = Body(...)): 
    return await _services.add_order(name, food_name)

@router.delete("/deleteorder/")
async def delete_order(name : str = Body(...), food_name : str = Body(...)):
    return await _services.delete_order(name , food_name)  

#------------------Table Things----------------------

@router.get("/tables/")
async def get_tables():
    return await _services.get_tables()

@router.post("/tables/")
async def add_table(number : int):
    return await _services.add_table(number)

@router.post("/tables/customer")
async def table_add_customer(user: str = Body(...), tablenumber: int = Body(...)):
    return await _services.table_add_customer(user, tablenumber)

@router.get("/table/customer/all/")
async def show_table_customer(tablenumber: int):
    return await _services.show_table_customer(tablenumber)

@router.get("/table/menu/")
async def show_table_menu(tablenumber: int):
    return await _services.show_table_menu(tablenumber)

@router.get("/table/payemnt/")
async def show_table_payment(tablenumber: int):
    return await _services.show_table_payment(tablenumber)


