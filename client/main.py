import random
import js
from pyscript import document
from pyodide.ffi import create_proxy
from abc import ABC, abstractmethod
from datetime import datetime

class AbstractWidget(ABC):
  def __init__(self, element_id):
    self.element_id = element_id
    self._element = None
    
  @property
  def element(self):
    if not self._element:
      self._element = document.querySelector(f"#{self.element_id}")
    return self._element
  
  @abstractmethod
  def drawWidget(self):
    pass

class HomeWidget(AbstractWidget):
  def __init__(self, element_id):
    AbstractWidget.__init__(self, element_id)
    self.rotate = 0
    
  def rotate_image(self, event):
    if (self.rotate < 180):
      self.rotate += 90
    else:
      self.rotate -= 90
    self.cart.className = f"w-8 h-8 rotate-{self.rotate}"
    self.cart_sound.play()
    
  def drawWidget(self):
    self.navbar = document.createElement("div")
    self.navbar.className = "bg-orange-500 w-screen text-white flex justify-center items-center p-10"
    self.navbar.innerHTML = "SukSaang"
    self.element.appendChild(self.navbar)
    
    self.category = document.createElement("div")
    self.category.className = "flex flex-col p-4 bg-zinc-200 border-b border-black gap-4"
    self.category_title = document.createElement("h2")
    self.category_title.innerHTML = "Categories"
    self.category.appendChild(self.category_title)
    self.category_images = document.createElement("div")
    self.category_images.className = "flex flex-row gap-4"
    for _ in range(5):
      self.image = document.createElement("img")
      self.image.className = "w-20 h-20 hover:scale-110 duration-300"
      self.image.src = "https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg"
      self.category_images.appendChild(self.image)
    self.category.appendChild(self.category_images)
    self.element.appendChild(self.category)
    
    self.recommend = document.createElement("div")
    self.recommend.className = "flex flex-col p-4 bg-orange-200 border-b border-black gap-4"
    self.recommend_title = document.createElement("h2")
    self.recommend_title.innerHTML = "Recommended"
    self.recommend.appendChild(self.recommend_title)
    self.recommend_images = document.createElement("div")
    self.recommend_images.className = "flex flex-row justify-evenly"
    for _ in range(3):
      self.image = document.createElement("img")
      self.image.className = "w-40 h-40 hover:scale-110 duration-300"
      self.image.src = "https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg"
      self.recommend_images.appendChild(self.image)
    self.recommend.appendChild(self.recommend_images)
    self.element.appendChild(self.recommend)
    
    self.popular = document.createElement("div")
    self.popular.className = "flex flex-col p-4 bg-orange-200 border-b border-black gap-4"
    self.popular_title = document.createElement("h2")
    self.popular_title.innerHTML = "Popular"
    self.popular.appendChild(self.popular_title)
    self.popular_images = document.createElement("div")
    self.popular_images.className = "flex flex-row justify-evenly"
    for _ in range(3):
      self.image = document.createElement("img")
      self.image.className = "w-40 h-40 hover:scale-110 duration-300"
      self.image.src = "https://img.freepik.com/free-vector/illustration-gallery-icon_53876-27002.jpg"
      self.popular_images.appendChild(self.image)
    self.popular.appendChild(self.popular_images)
    self.element.appendChild(self.popular)
    
    self.footer = document.createElement("div")
    self.footer.className = "flex p-6 bg-slate-200 border-b border-black gap-4 items-center justify-center"
    self.cart = document.createElement("img")
    self.cart.src = "https://www.freeiconspng.com/thumbs/cart-icon/basket-cart-icon-27.png"
    self.cart.className = "w-8 h-8 hover:scale-110 duration-300"
    self.cart_sound = js.Audio.new("./rabbit_hit.wav")
    self.cart.onclick = self.rotate_image
    self.footer.appendChild(self.cart)
    self.element.appendChild(self.footer)
    
if __name__ == "__main__":
  output = HomeWidget("container")
  output.drawWidget()