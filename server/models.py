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
        table=0,
        orders=0,
        address="",
    ):
        Account.__init__(self, username, password, hashed_password)
        self.table = table
        self.orders = persistent.list.PersistentList(orders)
        self.address = address

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
    def __init__(self, menus):
        self.menus = persistent.list.PersistentList(menus)

    def add_menu(self, food):
        self.menus.append(food)

    def delete_menu(self, food):
        self.menus.remove(food)

    def edit_menu(self, detail, amount=0):
        pass


class Table(persistent.Persistent):
    def __init__(self, customers):
        self.customers = persistent.list.PersistentList(customers)

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
    def __init__(self, name, price, description, cost, ingredients=[]):
        self.name = name
        self.price = price
        self.description = description
        self.cost = cost
        self.ingredients = persistent.list.PersistentList(ingredients)


class MainDish(Food, persistent.Persistent):
    def __init__(self, name, price, description, cost, type, ingredients=[]):
        Food.__init__(self, name, price, description, cost, ingredients)
        self.type = type


class Drink(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost, sweetness):
        Food.__init__(self, name, price, description, cost, ingredients)
        self.sweetness = sweetness


class Dessert(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost):
        Food.__init__(self, name, price, description, cost, ingredients)
