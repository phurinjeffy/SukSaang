import persistent
from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.name

    # def login(self):
    #     pass

    # def register(self):
    #     pass


class Customer(User, persistent.Persistent):
    def __init__(self, username, password, table=0, orders=0, address="SukSaang"):
        User.__init__(self, username, password)
        self.orders = persistent.list.PersistentList()
        self.orders = orders
        self.table = table
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


class Menu(persistent.Persistent):
    def __init__(self):
        self.menus = persistent.list.PersistentList()

    def add_menu(self, food):
        self.menus.append(food)

    def delete_menu(self, food):
        self.menus.remove(food)

    def edit_menu(self, detail, amount=0):
        pass


class Admin(User, persistent.Persistent):
    def __init__(self, username, password, tables=0, statistic=0):
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
        self.customers = persistent.list.PersistentList()

    def add_customers(self, customer):
        self.customers.append(customer)


class Statistic(persistent.Persistent):
    def __init__(self, income, popular, cost):
        self.income = income
        self.popular = popular
        self.cost = cost

    def generate_graph(self):
        pass


class Food(ABC):
    def __init__(self, name, price, description, cost, ingredients=[]):
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.description = description
        self.cost = cost

    def __str__(self):
        return self.name


class MainDish(Food, persistent.Persistent):
    def __init__(self, name, price, description, cost, type, ingredients=[]):
        Food.__init__(self, name, ingredients, price, description, cost)
        self.type = type


class Drink(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost, sweetness):
        Food.__init__(self, name, ingredients, price, description, cost, sweetness)
        self.sweetness = sweetness


class Dessert(Food, persistent.Persistent):
    def __init__(self, name, ingredients, price, description, cost):
        Food.__init__(self, name, ingredients, price, description, cost)
