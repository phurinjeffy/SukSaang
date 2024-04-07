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
            root.menus["Tomato Spaghetti"] = MainDish("Pasta", 10, "Spaghetti with tomato sauce", "Pasta", 5, ["spaghetti", "tomato sauce", "garlic", "basil"], photo="https://food.fnr.sndimg.com/content/dam/images/food/fullset/2021/02/05/Baked-Feta-Pasta-4_s4x3.jpg.rend.hgtvcom.1280.1280.suffix/1615916524567.jpeg")
            root.menus["Burger"] = MainDish("Burger", 12, "Beef burger with fries", "Junk", 6, ["beef patty", "burger bun", "lettuce", "tomato", "onion", "pickles"], photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwDExpkw1h_HE8snvuV5fSRA-uTf3MMpnwpv7BEnCfdQ&s")
            root.menus["Coke"] = Drink("Coke", 2, "Carbonated beverage", "Drink", 1, ["cola", "ice"], sweetness=0.5, photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgjGimql4X_n9_6KM-V7l0cgokXjbMTtztQrgD21-ebA&s")
            root.menus["Ice Cream"] =  Dessert("Ice Cream", 5, "Vanilla ice cream with chocolate sauce", "Dessert", 2, ["vanilla ice cream", "chocolate sauce"], photo="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Ice_cream_with_whipped_cream%2C_chocolate_syrup%2C_and_a_wafer_%28cropped%29.jpg/640px-Ice_cream_with_whipped_cream%2C_chocolate_syrup%2C_and_a_wafer_%28cropped%29.jpg")
            root.menus["Chicken Tikka Masala"] = MainDish("Chicken Tikka Masala", 15, "Grilled chicken in a creamy tomato sauce", "Rice", 8, ["chicken breast", "tomatoes", "cream", "spices", "onions"], photo="https://www.allrecipes.com/thmb/1ul-jdOz8H4b6BDrRcYOuNmJgt4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/239867chef-johns-chicken-tikka-masala-ddmfs-3X4-0572-e02a25f8c7b745459a9106e9eb13de10.jpg")
            root.menus["Caesar Salad"] = MainDish("Caesar Salad", 8, "Fresh romaine lettuce with Caesar dressing and croutons", "Sides", 4, ["romaine lettuce", "Caesar dressing", "parmesan cheese", "croutons"], photo="https://natashaskitchen.com/wp-content/uploads/2019/01/Caesar-Salad-Recipe-3.jpg")
            root.menus["Sushi Platter"] = MainDish("Sushi Platter", 20, "Assorted sushi rolls with soy sauce and wasabi", "Rice", 12, ["sushi rice", "nori seaweed", "assorted fish", "vegetables", "soy sauce", "wasabi"], photo="https://zushi.com.au/wp-content/uploads/2020/12/sushi-and-sashimi-catering-platter-10-e1691215721899.jpg")
            root.menus["Fish and Chips"] = MainDish("Fish and Chips", 14, "Battered and fried fish served with French fries", "Steak", 7, ["white fish fillets", "batter", "potatoes", "oil"], photo="https://www.thespruceeats.com/thmb/sdVTq0h7xZvJjPr6bE2fhh5M3NI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/SES-best-fish-and-chips-recipe-434856-hero-01-27d8b57008414972822b866609d0af9b.jpg")
            root.menus["Tom Yum Soup"] = MainDish("Tom Yum Soup", 10, "Spicy and sour Thai soup with shrimp or chicken", "Soup", 5, ["lemongrass", "galangal", "kaffir lime leaves", "chili", "lime juice", "fish sauce"], photo="https://i0.wp.com/www.brasswok.com/wp-content/uploads/2015/12/Thai-Food-Tom-Yam-Kung-e1457481635537.jpg?resize=640%2C400&ssl=1")
            root.menus["Ramen"] = MainDish("Ramen", 12, "Japanese noodle soup with broth, noodles, meat, and toppings", "Noodle", 6, ["ramen noodles", "broth", "pork belly", "egg", "green onions", "bamboo shoots"], photo="https://www.justonecookbook.com/wp-content/uploads/2023/04/Spicy-Shoyu-Ramen-8055-I.jpg")
            root.menus["New York Strip Steak"] = MainDish("New York Strip Steak", 25, "Grilled beef steak cut from the short loin", "Steak", 15, ["New York strip steak", "salt", "pepper", "butter", "garlic"], photo="https://www.grillseeker.com/wp-content/uploads/2021/05/How-to-Grill-the-Perfect-New-York-Strip-Steak-Feature-Image.jpg")
            root.menus["Pho"] = MainDish("Pho", 10, "Vietnamese noodle soup with broth, rice noodles, herbs, and meat", "Noodle", 6, ["rice noodles", "beef broth", "sirloin steak", "bean sprouts", "basil", "lime", "chili"], photo="https://www.allrecipes.com/thmb/SZjdgaXhmkrRNLoOvdxuAktwk3E=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/228443-authentic-pho-DDMFS-4x3-0523f6531ccf4dbeb4b5bde52e007b1e.jpg")
            root.menus["Grilled Salmon"] = MainDish("Grilled Salmon", 18, "Fresh salmon fillet grilled to perfection", "Steak", 12, ["salmon fillet", "olive oil", "lemon", "salt", "pepper", "herbs"], photo="https://www.thespruceeats.com/thmb/HgM2h42z1HGEcSWkWk5CgAjDDpQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/how-to-grill-salmon-2216658-hero-01-a9c948f8a238400ebaafc0caf509c7fa.jpg")
            root.menus["Chocolate Lava Cake"] = Dessert("Chocolate Lava Cake", 8, "Warm chocolate cake with a gooey molten center", "Dessert", 4, ["chocolate", "butter", "sugar", "eggs", "flour"], photo="https://www.thespruceeats.com/thmb/GfDTLZYz5JvL50_w8WqfEZjNs4g=/2000x1333/filters:fill(auto,1)/chocolate-lava-cake-2500-56a2108b3df78cf77272b1da.jpg")
            root.menus["Mango Sticky Rice"] = Dessert("Mango Sticky Rice", 6, "Thai dessert made with sweet glutinous rice, fresh mango, and coconut milk", "Dessert", 3, ["glutinous rice", "mango", "coconut milk", "sugar", "salt"], photo="https://cdn.jwplayer.com/v2/media/oaULnCZz/poster.jpg?width=720")
            root.menus["Mojito"] = Drink("Mojito", 10, "Classic Cuban cocktail made with rum, lime, mint, sugar, and soda water", "Drink", 5, ["white rum", "lime", "mint leaves", "sugar", "soda water"], photo="https://www.bhg.com/thmb/RuIXqyj_sGoJwZSs8DpKLF2Qa2g=/1244x0/filters:no_upscale():strip_icc()/diy-mojito-RU186788-1-b3184133555544bbae783b67881d1400.jpg")
            root.menus["Iced Matcha Latte"] = Drink("Iced Matcha Latte", 6, "Refreshing Japanese green tea beverage made with matcha powder and milk", "Drink", 3, ["matcha powder", "milk", "ice", "sweetener (optional)"], photo="https://cdn.loveandlemons.com/wp-content/uploads/2023/06/iced-matcha-latte.jpg")
            root.menus["Virgin Pina Colada"] = Drink("Virgin Pina Colada", 7, "Non-alcoholic tropical drink made with pineapple, coconut cream, and ice", "Mocktail", 4, ["pineapple juice", "coconut cream", "ice", "pineapple wedge (for garnish)"], photo="https://www.playpartyplan.com/wp-content/uploads/2022/07/virgin-pina-colada-3-e1658357704676.jpg")

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
            root.popular['Coke'] = Popular(dish="Coke", point=2)
            
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
