import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from database import connection
from models import *
from datetime import datetime, timedelta

# ------------------ token ------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        if username not in connection.root.users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user_data = connection.root.users[username]
        return user_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not decode token"
        )


async def get_user(username: str):
    try:
        user = connection.root.users.get(username)
        if user:
            return {"username": user.username, "password": user.password}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{username}' not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_users():
    try:
        users = []
        for username, user in connection.root.users.items():
            users.append({"username": username, "password": user.password})
        return {"users": users}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

async def retrieve_user_info(access_token: str):
    try:
        user = connection.root.users.get(access_token=access_token)
        if user:
            return {
                "username": user.username,
                "email": user.email,
                # Include other user information you want to retrieve
            }
        else:
            return None  # Return None if user is not found
    except Exception as e:
        raise e  # You can handle the exception as per your application's requirements
    
async def get_user(access_token: str):
    try:
        # Assuming you have a function to retrieve user info based on access token
        user_info = await retrieve_user_info(access_token)
        return user_info
    except Exception as e:
        raise e 

async def create_user(username: str, password: str):
    try:
        if username in connection.root.users:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )
        user = User(username, password)
        connection.root.users[username] = user
        connection.transaction_manager.commit()
        return {"username": username, "message": "User created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )


async def delete_user(username: str):
    try:
        if username in connection.root.users:
            del connection.root.users[username]
            connection.transaction_manager.commit()
            return {"message": f"User '{username}' deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User '{username}' not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def login_user(username: str, password: str):
    if username in connection.root.users:
        user = connection.root.users[username]
        if user.password == password:
            access_token = create_access_token(username)  # Generate JWT token
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )


# ------------------ admin ------------------------
async def get_current_admin(token: str = Depends(oauth2_scheme)) -> Admin:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        if username not in connection.root.admins:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
            )
        admin_data = connection.root.admins[username]
        return admin_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not decode token"
        )


async def get_admin(username: str):
    try:
        admin = connection.root.admins.get(username)
        if admin:
            return {"username": admin.username, "password": admin.password}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Admin '{username}' not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_admins():
    try:
        admins = []
        for username, user in connection.root.admins.items():
            admins.append({"username": username, "password": user.password})
        return {"admins": admins}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def create_admin(username: str, password: str):
    try:
        if username in connection.root.admins:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Admin already exists"
            )
        admin = Admin(username, password)
        connection.root.admins[username] = admin
        connection.transaction_manager.commit()
        return {"username": username, "message": "Admin created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create admin",
        )


async def delete_admin(username: str):
    try:
        if username in connection.root.admins:
            del connection.root.admins[username]
            connection.transaction_manager.commit()
            return {"message": f"Admin '{username}' deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Admin '{username}' not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def login_admin(username: str, password: str):
    if username in connection.root.admins:
        user = connection.root.admins[username]
        if user.password == password:
            access_token = create_access_token(username)  # Generate JWT token
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )


# ------------------ admin menu ------------------------
async def get_menu(menu_item: str):
    try:
        item = connection.root.menus.get(menu_item)
        if item:
            return {
                "name": item.name,
                "price": item.price,
                "description": item.description,
                "type": item.type,
                "ingredients": item.ingredients,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu '{menu_item}' not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


async def get_menus():
    try:
        menus = []
        for name, menu in connection.root.menus.items():
            menus.append(
                {
                    "name": menu.name,
                    "price": menu.price,
                    "description": menu.description,
                    "type": menu.type,
                    "cost": menu.cost,
                    "ingredients": menu.ingredients,
                }
            )
        return {"menus": menus}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def add_menu(
    category: str,
    name: str,
    price: int,
    description: str,
    type: str,
    cost: int,
    ingredients: list,
    sweetness: int,
):
    try:
        if name in connection.root.menus:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Menu already exists"
            )
        if category.upper() == "DRINK":
            menu = Drink(name, price, description, type, cost, ingredients, sweetness)
        elif category.upper() == "DESSERT":
            menu = Dessert(name, price, description, type, cost, ingredients)
        else:
            menu = MainDish(name, price, description, type, cost, ingredients)
        connection.root.menus[name] = menu
        connection.transaction_manager.commit()
        return {"message": "Menus registered successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create menu",
        )


async def delete_menu(food_name: str):
    try:
        if food_name in connection.root.menus:
            del connection.root[food_name]
            connection.transaction_manager.commit()
            return {"message": f"Menu Item '{food_name}' deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu Item '{food_name}' not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# ------------ Customer Order ------------------
async def get_orders(username: str):
    try:
        if username in connection.root.users:
            orders = []
            user_orders = connection.root.users[username].orders
            for item in user_orders:
                orders.append(
                    {
                        "name": item.name,
                        "price": item.price,
                    }
                )
            return {"orders": orders}
        else:
            return {"message": "User not found."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user orders.",
        )


async def add_order(username: str, food_name: str, amount: int):
    try:
        if food_name in connection.root.menus:
            food = connection.root.menus[food_name]
        else:
            return {"message": "The menu doesn't have this food"}
        if username in connection.root.users:
            for _ in range(amount):
                connection.root.users[username].orders.append(food)
            return {"message": "Order added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add menu",
        )


async def delete_order(username: str, food_name: str):
    try:
        if username in connection.root.users:
            user_obj = connection.root.users[username]
            for food in user_obj.orders:
                if food.name == food_name:
                    user_obj.orders.remove(food)
                    return {"message": "Order deleted successfully"}
            return {"error": "Food item not found in user's order list"}
        else:
            return {"error": "User not found"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete order",
        )


# --------------------Table-------------------------
async def get_tables():
    try:
        all_table = []
        for table in connection.root.tables:
            all_table.append({"table_num": table})
        return {"tables": all_table}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def add_table(table_num: str):
    try:
        if table_num in connection.root.tables:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Table already exists"
            )
        table = Table(table_num)
        connection.root.tables[table_num] = table
        connection.transaction_manager.commit()
        return {"message": "Table is added successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add table",
        )


async def add_table_customer(table_num: str, user: str):
    try:
        if user not in connection.root.users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if table_num not in connection.root.tables:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )

        table = connection.root.tables[table_num]
        if any(user == customer.username for customer in table.customers):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User '{user}' is already at table '{table_num}'",
            )
        table.customers.append(connection.root.users[user])
        connection.transaction_manager.commit()

        return {"message": f"User '{user}' added to table '{table_num}' successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def show_table_customer(table_num: int):
    try:
        if table_num in connection.root.tables:
            return [
                customer.username
                for customer in connection.root.tables[table_num].customers
            ]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def show_table_orders(table_num: int):
    try:
        if table_num in connection.root.tables:
            all_orders = []

            for customer in connection.root.tables[table_num].customers:
                customer_orders = [order for order in customer.orders]
                all_orders.extend(customer_orders)

            return all_orders
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def show_table_payment(table_num: int):
    try:
        if table_num in connection.root.tables:
            total_payment = 0

            for customer in connection.root.tables[table_num].customers:
                for order in customer.orders:
                    total_payment += order.price

            return {"total_payment": total_payment}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
