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


@router.post("/menu")
async def add_menu(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    return await add_memu_admin(
        name=name,
        price=price,
        description=description,
        cost=cost,
        type=type,
        ingredients=ingredients,
    )


@router.post("/order/")
async def add_food(
    name: str = Body(...),
    price: int = Body(...),
    description: str = Body(...),
    cost: int = Body(...),
    type: str = Body(...),
    ingredients: list = Body(...),
):
    pass
