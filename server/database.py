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
            root.menus["Pasta"] = MainDish("Pasta", 10, "Spaghetti with tomato sauce", "Italian", 5, ["spaghetti", "tomato sauce", "garlic", "basil"], photo="https://food.fnr.sndimg.com/content/dam/images/food/fullset/2021/02/05/Baked-Feta-Pasta-4_s4x3.jpg.rend.hgtvcom.1280.1280.suffix/1615916524567.jpeg")
            root.menus["Burger"] = MainDish("Burger", 12, "Beef burger with fries", "American", 6, ["beef patty", "burger bun", "lettuce", "tomato", "onion", "pickles"], photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwDExpkw1h_HE8snvuV5fSRA-uTf3MMpnwpv7BEnCfdQ&s")
            root.menus["Coke"] = Drink("Coke", 2, "Carbonated beverage", "Soft Drink", 1, ["cola", "ice"], sweetness=0.5, photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgjGimql4X_n9_6KM-V7l0cgokXjbMTtztQrgD21-ebA&s")
            root.menus["Ice Cream"] =  Dessert("Ice Cream", 5, "Vanilla ice cream with chocolate sauce", "Dessert", 2, ["vanilla ice cream", "chocolate sauce"], photo="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Ice_cream_with_whipped_cream%2C_chocolate_syrup%2C_and_a_wafer_%28cropped%29.jpg/640px-Ice_cream_with_whipped_cream%2C_chocolate_syrup%2C_and_a_wafer_%28cropped%29.jpg")

        if not hasattr(root, "tables"):
            root.tables = BTrees.OOBTree.BTree()
            # Adding default tables
            root.tables[1] = Table(1, customers=[], available=True)
            root.tables[2] = Table(2, customers=[], available=True)
            root.tables[3] = Table(3, customers=[], available=True)
            root.tables[4] = Table(4, customers=[], available=True)
            root.tables[5] = Table(5, customers=[], available=True)
            root.tables[6] = Table(6, customers=[], available=True)
            root.tables[7] = Table(7, customers=[], available=True)
            root.tables[8] = Table(8, customers=[], available=True)
            root.tables[9] = Table(9, customers=[], available=True)
            root.tables[10] = Table(10, customers=[], available=True)
            root.tables[11] = Table(11, customers=[], available=True)
            root.tables[12] = Table(12, customers=[], available=True)
        
        if not hasattr(root, "stats"):
            root.stats = BTrees.OOBTree.BTree()
            # Febuary
            root.stats['2024-02-01'] = Stat(date='2024-02-01', cost=50, income=120)
            root.stats['2024-02-02'] = Stat(date='2024-02-02', cost=45, income=280)
            root.stats['2024-02-03'] = Stat(date='2024-02-03', cost=30, income=160)
            # March
            root.stats['2024-03-01'] = Stat(date='2024-03-01', cost=70, income=700)
            root.stats['2024-03-02'] = Stat(date='2024-03-02', cost=55, income=530)
            root.stats['2024-03-03'] = Stat(date='2024-03-03', cost=20, income=450)
            # April
            root.stats['2024-04-01'] = Stat(date='2024-04-01', cost=100, income=200)
            root.stats['2024-04-02'] = Stat(date='2024-04-02', cost=35, income=75)
            root.stats['2024-04-03'] = Stat(date='2024-04-03', cost=65, income=185)
            
        if not hasattr(root, "popular"):
            root.popular = BTrees.OOBTree.BTree()
            root.popular['Coke'] = Popular(name="Coke", point=2)
            root.popular['Pasta'] = Popular(name="Pasta", point=4)
            root.popular['Burger'] = Popular(name="Burger", point=3)
            
        print("Database loaded from file.")
    except Exception as e:
        print("Error loading database from file:", e)
        print("Initializing database with default data.")
        root.users = BTrees.OOBTree.BTree()
        root.admins = BTrees.OOBTree.BTree()
        root.menus = BTrees.OOBTree.BTree()
        root.tables = BTrees.OOBTree.BTree()
        root.stats = BTrees.OOBTree.BTree()
        root.popular = BTrees.OOBTree.BTree()


def close_db_connection():
    global connection, db
    transaction.commit()
    connection.close()
    db.close()
    print("Database closed.")


atexit.register(close_db_connection)
