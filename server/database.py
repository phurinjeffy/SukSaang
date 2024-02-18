import ZODB, ZODB.FileStorage
import transaction
import BTrees
import atexit

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
        if not hasattr(root, "admins"):
            root.admins = BTrees.OOBTree.BTree()
        if not hasattr(root, "menus"):
            root.menus = BTrees.OOBTree.BTree()
        print("Database loaded from file.")
    except Exception as e:
        print("Error loading database from file:", e)
        print("Initializing database with default data.")
        root.users = BTrees.OOBTree.BTree()
        root.admins = BTrees.OOBTree.BTree()
        root.menus = BTrees.OOBTree.BTree()


def close_db_connection():
    global connection, db
    transaction.commit()
    connection.close()
    db.close()
    print("Database closed.")


atexit.register(close_db_connection)
