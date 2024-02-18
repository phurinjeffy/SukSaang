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
        if not hasattr(root, 'users'):
            root.customers = BTrees.OOBTree.BTree()
            # root.users["default"] = Customer(username="default", password="default")
        if not hasattr(root, 'admins'):
            root.admins = BTrees.OOBTree.BTree()
            # root.admins["default"] = Admin(username="default", password="default")
        if not hasattr(root, 'menus'):
            root.menus = BTrees.OOBTree.BTree()
            # root.menus["veggie"] = MainDish(name="veggie", price=10, description="vegan", cost=100, type="vegan", ingredients=[])
        print("Database loaded from file.")
    except Exception as e:
        print("Error loading database from file:", e)
        print("Initializing database with default data.")
        initialize_default_data(root)
        
def initialize_default_data(root):
    root.customers = BTrees.OOBTree.BTree()
    root.admins = BTrees.OOBTree.BTree()
    root.menus = BTrees.OOBTree.BTree()