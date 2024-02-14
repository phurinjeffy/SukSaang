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
    self.category.className = "flex flex-col p-4 bg-zinc-200 border-b border-black gap-4 text-center text-xl"
    self.category_title = document.createElement("h2")
    self.category_title.innerHTML = "Vegeterian Pizza"
    self.category.appendChild(self.category_title)
    self.category_images = document.createElement("div")
    self.category_images.className = "flex flex-row gap-4 justify-center items-center"
    self.image = document.createElement("img")
    self.image.className = "w-40 h-40 flex flex-row justify-evenly items-center text-center"
    self.image.src = "https://www.orchidsandsweettea.com/wp-content/uploads/2019/05/Veggie-Pizza-2-of-5-e1691215701129.jpg"
    self.category_images.appendChild(self.image)
    self.category.appendChild(self.category_images)
    self.element.appendChild(self.category)

    self.detail = document.createElement("div")
    self.detail.className = "flex-row justify-evenly text-center p-20 gap-10"
    self.detail_title = document.createElement("h2")
    self.detail_title.innerHTML = "Description"
    self.detail.appendChild(self.detail_title)
    self.detail_info = document.createElement("p")
    self.detail_info.className = "w-50"
    self.detail_info.innerHTML = "Indulge in a culinary delight with our Vegetarian Pizza, a symphony of flavors bursting with fresh bell peppers, onions, mushrooms, olives, and tomatoes atop a golden, crispy crust. Each bite is a celebration of nature's bounty, with the savory richness of mozzarella cheese tying it all together. Whether you're a devoted vegetarian or simply craving a fresh, flavorful option, our Vegetarian Pizza promises to satisfy your palate and leave you craving more."
    self.detail.appendChild(self.detail_info)
    self.element.appendChild(self.detail)
    
    self.footer = document.createElement("div")
    self.footer.className = "flex p-6 bg-slate-200 border-b border-black gap-4 items-center justify-center"
    self.cart = document.createElement("img")
    self.cart.src = "https://www.freeiconspng.com/thumbs/cart-icon/basket-cart-icon-27.png"
    self.cart.className = "w-8 h-8"
    self.cart_sound = js.Audio.new("./rabbit_hit.wav")
    self.cart.onclick = self.rotate_image
    self.footer.appendChild(self.cart)
    self.element.appendChild(self.footer)
    
if __name__ == "__main__":
  output = HomeWidget("container")
  output.drawWidget()