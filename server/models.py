import logging
import persistent
from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(self, username, password, hashed_password=""):
        self.username = username
        self.password = password
        self.hashed_password = hashed_password


class User(Account, persistent.Persistent):
    def __init__(
        self,
        username,
        password,
        hashed_password="",
        address="",
        table=0,
        orders=None,
    ):
        Account.__init__(self, username, password, hashed_password)
        self.address = address
        self.table = table
        self.orders = orders if orders is not None else {}

    def add_order(self, order):
        self.orders.append(order)

    def delete_order(self, order):
        if order in self.orders:
            self.orders.remove(order)

    def view_cart(self):
        return self.orders

    def confirm_order(self):
        pass

    def check_out(self):
        pass

    def clear_cart(self):
        self.orders.clear()


class Admin(Account, persistent.Persistent):
    def __init__(self, username, password, hashed_password="", tables=0, statistic=0):
        Account.__init__(self, username, password, hashed_password)
        self.tables = tables
        self.statistic = statistic

    def add_menu(self):
        pass

    def delete_menu(self):
        pass

    def edit_menu(self, menu):
        pass

    def generate_payment(self):
        pass


class Menu(persistent.Persistent):
    def __init__(self, menus=[]):
        self.menus = persistent.list.PersistentList(menus)

    def add_menu(self, food):
        self.menus.append(food)

    def delete_menu(self, food):
        self.menus.remove(food)

    def edit_menu(self, detail, amount=0):
        pass


class Table(persistent.Persistent):
    def __init__(self, table_num, customers=[], available=True):
        self.table_num = table_num
        self.customers = persistent.list.PersistentList(customers)
        self.available = available

    def add_customers(self, customer):
        self.customers.append(customer)


class Statistic(persistent.Persistent):
    def __init__(self, day, cost, income, popular):
        self.day = day
        self.cost = cost
        self.income = income
        self.popular = popular

    def generate_graph(self):
        pass


class Food(ABC):
    def __init__(self, name, price, description="", type="", cost=0, ingredients=[], photo="https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg"):
        self.name = name
        self.price = price
        self.description = description
        self.type = type
        self.cost = cost
        self.ingredients = ingredients
        self.photo = photo


class MainDish(Food, persistent.Persistent):
    def __init__(self, name, price, description="", type="", cost=0, ingredients=[], photo="https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg"):
        Food.__init__(self, name, price, description, type, cost, ingredients, photo)
        

class Drink(Food, persistent.Persistent):
    def __init__(self, name, price, description="", type="", cost=0, ingredients=[], photo="https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg", sweetness=1):
        Food.__init__(self, name, price, description, type, cost, ingredients, photo)
        self.sweetness = sweetness


class Dessert(Food, persistent.Persistent):
    def __init__(self, name, price, description="", type="", cost=0, ingredients=[], photo="https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg"):
        Food.__init__(self, name, price, description, type, cost, ingredients, photo)
        
        
class Log:
    def __init__(self, filename='app.log', level=logging.INFO):
        self.filename = filename
        self.level = level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)/Users/yokurawee/Documents/jeff-SukSaang/server/mydata.fs