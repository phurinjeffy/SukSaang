import ZODB
import ZODB.FileStorage
import transaction
from models import *
import BTrees

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

def init_db():
    global root
    print("Initializing database.")
    try:
        root = connection.root
        print("Database loaded from file.")
    except Exception as e:
        print("Error loading database from file:", e)
        print("Initializing database with default data.")
        root.users = BTrees.OOBTree.BTree()
        root.menus = BTrees.OOBTree.BTree()
        root.users["default"] = Customer(username="default", password="default")
        root.menus["vegtablePizza"] = MainDish("veg", 10, "jwfiokdc", 10, "maindish", [])