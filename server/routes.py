from fastapi import APIRouter, HTTPException, Body
from database import *
from models import *
import services as _services

router = APIRouter()


# ------------------ user ------------------
@router.get("/users/")
async def get_users():
    try:
        users = []
        for username, user in root.customers.items():
            users.append({"username": username, "password": user.password})
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register/")
async def create_user(username: str = Body(...), password: str = Body(...)):
    try:
        return await _services.create_user(username, password)
    except HTTPException as e:
        raise e


@router.post("/login/")
async def login_user(username: str = Body(...), password: str = Body(...)):
    try:
        return await _services.login_user(username, password)
    except HTTPException as e:
        raise e


# ------------------ admin ------------------
@router.get("/admin/")
async def get_admins():
    try:
        admins = []
        for username, user in root.admins.items():
            admins.append({"username": username, "password": user.password})
        return {"admins": admins}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/register/")
async def create_admin(username: str = Body(...), password: str = Body(...)):
    try:
        return await _services.create_admin(username, password)
    except HTTPException as e:
        raise e


@router.post("/admin/login/")
async def login_admin(username: str = Body(...), password: str = Body(...)):
    try:
        return await _services.login_admin(username, password)
    except HTTPException as e:
        raise e


# ------------------ menu ------------------
@router.get("/admin/menus/")
async def get_menus():
    try:
        menus = []
        for name, menu in root.menus.items():
            menus.append(
                {
                    "name": menu.name,
                    "price": menu.price,
                    "description": menu.description,
                    "cost": menu.cost,
                    "ingredients": menu.ingredients,
                }
            )
        return {"menus": menus}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/menu/")
async def add_menu(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    try:
        if name in root.menus:
            raise HTTPException(status_code=400, detail="Menu already exists")
        dish = MainDish(name, price, description, cost, type, ingredients)
        root.menus[name] = dish
        connection.transaction_manager.commit()
        return {"message": "Menus registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
