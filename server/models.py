import logging
import persistent
from abc import ABC, abstractmethod
import matplotlib as plt


class Account(ABC):
    def __init__(self, username, password, hashed_password=""):
        self.username = username
        self.password = password
        self.hashed_password = hashed_password

    def get_username(self):
        return self.username
    
    def get_hashPassword(self):
        return self.hashed_password
        
        
class Order(persistent.Persistent):
    def __init__(self, food, quantity):
        self.food = food
        self.quantity = quantity

    def get_food(self):
        return self.food
    
    def get_price(self):
        return self.food.price


class User(Account, persistent.Persistent):
    def __init__(
        self,
        username,
        password,
        hashed_password="",
        address="",
        table=0,
        cart=None,
        orders=None,
    ):
        Account.__init__(self, username, password, hashed_password)
        self.address = address
        self.table = table
        self.cart = cart if cart is not None else {}
        self.orders = orders if orders is not None else {}

    def add_order(self, order):
        self.orders.append(order)

    def delete_order(self, order):
        if order in self.orders:
            self.orders.remove(order)

    def view_cart(self):
        return self.orders

    def confirm_order(self, order):
        self.orders[order].status = 'ordered'

    def check_out(self):
        self.cart = None
        self.orders = None
        table = 0

    def clear_cart(self):
        self.orders.clear()


class Admin(Account, persistent.Persistent):
    def __init__(self, username, password, hashed_password="", tables=0, statistic=0):
        Account.__init__(self, username, password, hashed_password)
        self.tables = tables
        self.statistic = statistic
        self.menu_list = {}

    def add_menu(self, menu):
        self.menu_list[menu.name] = menu
    def delete_menu(self, menu):
        self.menu_list.delete(menu)

    def edit_menu(self, menu, detail):
        self.menu_list[menu] = detail

    def generate_payment(self):
        sum = 0
        for order in self.tables:
            sum += order.price
        return sum


class Menu(persistent.Persistent):
    def __init__(self, menus=[]):
        self.menus = persistent.list.PersistentList(menus)

    def add_menu(self, food):
        self.menus.append(food)

    def delete_menu(self, food):
        self.menus.remove(food)

    def edit_menu(self, new_detail):
        self.menu.part = new_detail


class Table(persistent.Persistent):
    def __init__(self, table_num, customers=[], available=True):
        self.table_num = table_num
        self.customers = persistent.list.PersistentList(customers)
        self.available = available

    def add_customers(self, customer):
        self.customers.append(customer)


class Stat(persistent.Persistent):
    def __init__(self, date=None, cost=0, income=0, popular=[]):
        self.date = date
        self.cost = cost
        self.income = income
        self.popular = popular

    def plot_bar_graph(self, daily_revenue, daily_cost):
        dates = sorted(daily_revenue.keys())
        revenue_values = [daily_revenue[date] for date in dates]
        cost_values = [daily_cost[date] for date in dates]

        x = range(len(dates))  # Create a list of x coordinates for each date
        width = 0.4
        
        fig, ax = plt.subplots()
        ax.bar(x, revenue_values, width, label='Revenue', color='green')
        ax.bar([i + width for i in x], cost_values, width, label='Cost', color='red')

        ax.set_xlabel('Date')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Daily Revenue and Costs')
        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in dates], rotation=45)
        plt.legend()
        
        plt.tight_layout()
        plt.show()


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
        self.logger.debug(message)

class Popular:
    def __init__(self, name=None, point=0):
        self.name = name
        self.point = point

    def get_popular(self, popular):
        return popular.point