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

class LoginPage(AbstractWidget):
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
    
    self.login = document.createElement("div")
    self.login.className = "flex flex-col h-screen w-screen p-4 bg-zinc-200 gap-4 text-center text-xl"
    self.login_title = document.createElement("p")
    self.login_title.innerHTML = "Login"
    self.login_title.className = "text-center text-2xl font-semibold font-varela font-medium break-words my-8"
    self.login.appendChild(self.login_title)

    #box
    self.box = document.createElement("div")
    self.box.className = "flex flex-col gap-4"
    #box username
    self.username_box = document.createElement("div")
    self.username_box.className = ""
    self.username_header = document.createElement("p")
    self.username_header.className = "text-center text-2xl font-semibold font-varela font-medium break-words my-8"
    self.username_header.innerHTML = "username"
    self.username_input = document.createElement("input")
    self.username_input.className = "w-96 h-14 relative rounded-lg border border-gray-300 px-5"
    #box password
    self.password_box = document.createElement("div")
    self.password_box.classname = ""
    self.password_header = document.createElement("p")
    self.password_header.className = "text-center text-2xl font-semibold font-varela font-medium break-words my-8"
    self.password_header.innerHTML = "password"
    self.password_input = document.createElement("input")
    self.password_input.className = "w-96 h-14 relative rounded-lg border border-gray-300 px-5"
    #box button
    self.button_box = document.createElement("div")
    self.button_box.className = ""
    self.button_login = document.createElement("button")
    self.button_login.className = "w-96 h-16 bg-orange-500 shadow-md rounded-full text-white text-lg font-varela font-medium my-8"
    self.button_login.innerHTML = "Login"
    self.button_login.onclick = self.rotate_image

    #box question signup
    self.question_signup_box = document.createElement("div")
    self.question_signup_box.className = ""
    self.question_text = document.createElement("p")
    self.question_text.className = "text-center font-bold"
    self.question_text.innerHTML = "Don't have an account?"

    self.signup_text = document.createElement("p")
    self.signup_text.className = "text-center underline"
    self.signup_text.innerHTML = "sign up"

    self.username_box.appendChild(self.username_header)
    self.username_box.appendChild(self.username_input)
    self.password_box.appendChild(self.password_header)
    self.password_box.appendChild(self.password_input)
    self.button_box.appendChild(self.button_login)
    self.question_signup_box.appendChild(self.question_text)
    self.question_signup_box.appendChild(self.signup_text)

    self.box.appendChild(self.username_box)
    self.box.appendChild(self.password_box)
    self.box.appendChild(self.button_box)
    self.box.appendChild(self.question_signup_box)
    self.login.appendChild(self.box)
    self.element.appendChild(self.login)


    # self.footer = document.createElement("div")
    # self.footer.className = "flex p-6 bg-slate-200 border-b border-black gap-4 items-center justify-center"
    # self.cart = document.createElement("img")
    # self.cart.src = "https://www.freeiconspng.com/thumbs/cart-icon/basket-cart-icon-27.png"
    # self.cart.className = "w-8 h-8"
    # self.cart_sound = js.Audio.new("./rabbit_hit.wav")
    # self.cart.onclick = self.rotate_image
    # self.footer.appendChild(self.cart)
    # self.element.appendChild(self.footer)
    
if __name__ == "__main__":
  output = LoginPage("container")
  output.drawWidget()