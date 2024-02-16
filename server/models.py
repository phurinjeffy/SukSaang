import ZODB, ZODB.config
import persistent
from abc import ABC, abstractmethod


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
        
    