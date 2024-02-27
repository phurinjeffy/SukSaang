import ZODB, ZODB.FileStorage
import transaction
import BTrees
import atexit
from models import *

storage = ZODB.FileStorage.FileStorage("mydata.fs")
db = ZODB.DB(storage)
connection = db.open()
root = connection.root


def init_db():
    global root
    print("Initializing database.")
    try:
        if not hasattr(root, "users"):
            root.users = BTrees.OOBTree.BTree()
            # Adding default users
            root.users["user1"] = User("user1", "password1")
            root.users["user2"] = User("user2", "password2")
            root.users["user3"] = User("user3", "password3")

        if not hasattr(root, "admins"):
            root.admins = BTrees.OOBTree.BTree()
            # Adding default admins
            root.admins["admin1"] = Admin("admin1", "adminpassword1")
            root.admins["admin2"] = Admin("admin2", "adminpassword2")

        if not hasattr(root, "menus"):
            root.menus = BTrees.OOBTree.BTree()
            # Adding default menu items
            root.menus["Pasta"] = MainDish("Pasta", 10, "Spaghetti with tomato sauce", "Italian", 5, ["spaghetti", "tomato sauce", "garlic", "basil"])
            root.menus["Burger"] = MainDish("Burger", 12, "Beef burger with fries", "American", 6, ["beef patty", "burger bun", "lettuce", "tomato", "onion", "pickles"])
            root.menus["Coke"] = Drink("Coke", 2, "Carbonated beverage", "Soft Drink", 1, ["cola", "ice"], sweetness=0.5)
            root.menus["Ice Cream"] =  Dessert("Ice Cream", 5, "Vanilla ice cream with chocolate sauce", "Dessert", 2, ["vanilla ice cream", "chocolate sauce"])

        if not hasattr(root, "tables"):
            root.tables = BTrees.OOBTree.BTree()
            # Adding default tables
            root.tables[1] = Table(1)
            root.tables[2] = Table(2)
            root.tables[3] = Table(3)

        if not hasattr(root, "bookings"):
            root.bookings = BTrees.OOBTree.BTree()

            for i in range(1,11):
                root.bookings[str(i)] = True
            
        print("Database loaded from file.")
    except Exception as e:
        print("Error loading database from file:", e)
        print("Initializing database with default data.")
        root.users = BTrees.OOBTree.BTree()
        root.admins = BTrees.OOBTree.BTree()
        root.menus = BTrees.OOBTree.BTree()
        root.tables = BTrees.OOBTree.BTree()
        root.bookings = BTrees.OOBTree.BTree()


def close_db_connection():
    global connection, db
    transaction.commit()
    connection.close()
    db.close()
    print("Database closed.")


atexit.register(close_db_connection)
