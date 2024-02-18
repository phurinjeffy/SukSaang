import persistent
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.name

    def login(self):
        pass

    def register(self):
        pass


class Customer(User, persistent.Persistent):
    def __init__(self, username, password, table=0, orders=0, address="SukSaang"):
        User.__init__(self, username, password)
        self.orders = persistent.list.PersistentList()
        self.orders = orders
        self.table = table
        self.address = address

    def add_order(self):
        pass

    def delete_order(self):
        pass

    def view_cart(self):
        pass

    def confirm_order(self):
        pass

    def check_out(self):
        pass

    def clear_cart(self):
        pass


class Admin(User, persistent.Persistent):
    def __init__(self, username, password, tables, statistic):
        User.__init__(self, username, password)
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


class Table(persistent.Persistent):
    def __init__(self, customers):
        self.customers = customers

    def add_customers(self, customer):
        pass


class Statistic(persistent.Persistent):
    def __init__(self, day, cost, income, popular):
        self.day = day
        self.cost = cost
        self.income = income
        self.popular = popular

    def generate_graph(self):
        pass

class Food(ABC):
    def __init__(self, name, ingredients, price, description, cost):
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.description = description
        self.cost = cost

    def __str__(self):
        return self.name


class MainDish(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost, type):
        Food.__init__(self, name, ingredients, price, description, cost)
        self.type = type


class Drink(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost, sweetness):
        Food.__init__(self, name, ingredients, price, description, cost, sweetness)
        self.sweetness = sweetness


class Dessert(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost):
        Food.__init__(self, name, ingredients, price, description, cost)
