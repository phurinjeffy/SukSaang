from fastapi import APIRouter, HTTPException, Body
from database import *
from models import *
from services import *

router = APIRouter()

#------------------ token with user ------------------
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
async def register_new_customer(username: str = Body(...), password: str = Body(...)):
    try:
        return await register_customer(username, password)  # Call register_customer function from services.py
    except HTTPException as e:
        raise e

@router.post("/login/")
async def user_login(username: str = Body(...), password: str = Body(...)):
    try:
        return await login_customer(username, password)  # Call login function from services.py
    except HTTPException as e:
        raise e



# @router.get("/admins/")
# async def get_admin():
#     try:
#         admins = []
#         for username, user in root.admins.items():
#             admins.append({"username": username, "password": user.password})
#         return {"admins": admins}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/admin/register/")
# async def register_admin(username: str, password: str):
#     try:
#         if username in root.admins:
#             raise HTTPException(status_code=400, detail="Admin already exists")
#         admin = Admin(username, password)
#         root.admins[username] = admin
#         connection.transaction_manager.commit()
#         return {"message": "Admin registered successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/admin/login/")
# async def login_admin(username: str = Body(...), password: str = Body(...)):
#     if username in root.admins:
#         admin = root.admins[username]
#         if isinstance(admin, Admin) and admin.password == password:
#             return {"message": "Admin login successful"}
#     raise HTTPException(
#         status_code=401, detail="Invalid username or password for admin"
#     )

@router.get("/admins/")
async def get_admin():
    try:
        admins = []
        for username, user in root.admins.items():
            admins.append({"username": username, "password": user.password})
        return {"admins": admins}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/register/")
async def register_new_admin(username: str = Body(...), password: str = Body(...)):
    try:
        return await register_admin(username, password)  # Call register_admin function from services.py
    except HTTPException as e:
        raise e

@router.post("/admin/login/")
async def admin_login(username: str = Body(...), password: str = Body(...)):
    try:
        return await login_admin(username, password)  # Call login_admin function from services.py
    except HTTPException as e:
        raise e
    

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
