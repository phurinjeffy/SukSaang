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
    if hasattr(root, 'users'):
        print("Database already initialized.")
    else:
        print("Initializing database.")
        try:
            root = connection.root
            print("Database loaded from file.")
        except Exception as e:
            print("Error loading database from file:", e)
            print("Initializing database with default data.")
            root.users = BTrees.OOBTree.BTree()
            root.users["user1"] = Customer(username="user1", password="pass1")