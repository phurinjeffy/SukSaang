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

class Navbar(AbstractWidget):
  def __init__(self, element_id):
    AbstractWidget.__init__(self, element_id)
    
  def drawWidget(self):
    self.navbar = document.createElement("div")
    self.navbar.className = "backdrop-blur-lg w-screen h-24 text-white flex justify-center items-center fixed z-10"
    self.title = document.createElement("a")
    self.title.innerHTML = "SukSaang"
    self.title.className = "font-signature font-extrabold text-5xl"
    self.navbar.appendChild(self.title)
    self.element.appendChild(self.navbar)
    
class MainContent(AbstractWidget):
  def __init__(self, element_id):
    AbstractWidget.__init__(self, element_id)
    
  def drawWidget(self, widgets):
    self.content = document.createElement("div")
    self.content.id = "content"
    self.content.className = "pt-28 h-screen w-screen bg-gradient-to-br from from-zinc-950 via-gray-800 to-gray-700"
    self.element.appendChild(self.content)
    
    for widget in widgets:
      widget.drawWidget()

class Home(AbstractWidget):
  def __init__(self, element_id):
    AbstractWidget.__init__(self, element_id)
    
  def drawWidget(self):
    self.container = document.createElement("div")
    self.container.className = "flex flex-col justify-center items-center gap-10"
    
    self.customer = document.createElement("div")
    self.customer.className = "flex justify-center uppercase p-10 bg-gray-700 w-[400px] text-white cursor-pointer"
    self.customer.innerHTML = "customer"
    self.container.appendChild(self.customer)
    
    self.admin = document.createElement("div")
    self.admin.className = "flex justify-center uppercase p-10 bg-gray-700 w-[400px] text-white cursor-pointer" 
    self.admin.innerHTML = "admin"
    self.container.appendChild(self.admin)
    
    self.element.appendChild(self.container)
    
    
if __name__ == "__main__":
  Navbar("app").drawWidget()
  
  content = MainContent("app")
  content.drawWidget([Home("content")])