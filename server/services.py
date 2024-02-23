import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
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


async def create_user(username: str, password: str):
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

async def get_menus():
    try:
        menus = []
        for name, menu in connection.root.menus.items():
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def add_menu(
    name: str,
    price: int,
    description: str,
    cost: int,
    type: str,
    ingredients: list,
):
    try:
        if name in connection.root.menus:
            raise ValueError("Menu already exists")

        dish = MainDish(name, price, description, cost, type, ingredients)
        connection.root.menus[name] = dish
        connection.transaction_manager.commit()

        return {"message": "Menus registered successfully"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create menu",
        )

# 'RootConvenience' object does not support item deletion
# async def delete_menu(food_name: str):
#     try:
#         if food_name in connection.root.menus:
#             del connection.root[food_name]
#             await connection.commit()
#             print(f"Menu item '{food_name}' deleted successfully.")
#         else:
#             print(f"Menu item '{food_name}' not found.")
#     except Exception as e:
#         print(f"Error deleting menu item '{food_name}': {e}")

#------------Customer Order------------------
async def add_order(user : str, food_name : str):
    try:
        if food_name in connection.root.menus:
            food = connection.root.menus[food_name]
        else:
            return {"message" : "In menu don't have this food"} 
        if user in connection.root.users:
            connection.root.users[user].orders.append(food)
            return {"message": "Order added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add menu",
        )

async def get_user_order(user: str):
    try:
        if user in connection.root.users:
            user_orders = connection.root.users[user].orders
            order_names = [food.name for food in user_orders]
            return {"orders": order_names}
        else:
            return {"message": "User not found."}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user orders.",
        )

async def delete_order(user: str, food_name: str):
    try:
        if user in connection.root.users:
            user_obj = connection.root.users[user]
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

#--------------------Table-------------------------
    
async def get_tables():
    try:
        all_table = []
        for table in connection.root.tables:
            all_table.append({"table_number": table})
        return {"tables": all_table}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

async def add_table(tnum: str):
    try:
        if tnum in connection.root.tables:
            raise ValueError("Table already exists")

        table = Table(tnum)
        connection.root.tables[tnum] = table
        connection.transaction_manager.commit()
        return {"message": "Table is added successfully"}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add table",
        )

async def table_add_customer(user: str, table: str):
    try:
        if user in connection.root.users and table in connection.root.tables:
            connection.root.tables[table].customers.append(connection.root.users[user])
            connection.transaction_manager.commit()
            return {"message": f"User '{user}' added to table '{table}' successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or table not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def show_table_customer(table_num: int):
    try:
        if table_num in connection.root.tables:
            return [customer.username for customer in connection.root.tables[table_num].customers]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="table not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def show_table_menu(table_num: int):
    try:
        if table_num in connection.root.tables:
            all_menus = []
            
            for customer in connection.root.tables[table_num].customers:
                customer_menus = [order for order in customer.orders]
                all_menus.extend(customer_menus)
            
            return all_menus
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def show_table_payment(table_num: int):
    try:
        if table_num in connection.root.tables:
            total_payment = 0
            
            for customer in connection.root.tables[table_num].customers:
                for order in customer.orders:
                    total_payment += order.price
            
            return {"total_payment": total_payment}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))