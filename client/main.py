import js
from pyscript import document
import requests
from abc import ABC, abstractmethod


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


class Layout(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def drawWidget(self, widgets):
        self.content = document.createElement("div")
        self.content.id = "content"
        self.content.className = "pt-28 h-screen w-screen bg-gradient-to-br from from-zinc-950 via-gray-800 to-gray-700"
        self.element.appendChild(self.content)

        for widget in widgets:
            widget.drawWidget()


class Welcome(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def redirect_to_login(self, event):
        js.window.location.href = "/login"

    def drawWidget(self):
        self.container = document.createElement("div")
        self.container.className = "flex flex-col justify-center items-center gap-10"

        self.customer = document.createElement("div")
        self.customer.className = "flex justify-center uppercase p-10 bg-gray-700 w-[400px] text-white cursor-pointer"
        self.customer.innerHTML = "customer"
        self.customer.onclick = self.redirect_to_login
        self.container.appendChild(self.customer)

        self.admin = document.createElement("div")
        self.admin.className = "flex justify-center uppercase p-10 bg-gray-700 w-[400px] text-white cursor-pointer"
        self.admin.innerHTML = "admin"
        self.admin.onclick = self.redirect_to_login
        self.container.appendChild(self.admin)

        self.element.appendChild(self.container)


class Login(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def redirect_to_register(self, event):
        js.window.location.href = "/register"
        
    def login_click(self, event):
        username = self.username_input.value
        password = self.password_input.value
        
        url = "http://localhost:8000/login/"
        data = {
            "username": username,
            "password": password
        }
        headers = {
            'Content-Type': 'application/json',
        }
        
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            message = data.get("message", "Login successful")
            if message == "Login successful":
                print("Login successful!")
                js.window.location.href = "/home"
            else:
                print("Login failed:", message)
        else:
            print("Error:", response.text)

    def drawWidget(self):
        self.login = document.createElement("div")
        self.login.className = (
            "flex flex-col justify-center items-center w-screen gap-4 pt-10"
        )

        self.login_title = document.createElement("h3")
        self.login_title.innerHTML = "Login"
        self.login_title.className = "text-4xl font-semibold font-medium text-white"
        self.login.appendChild(self.login_title)

        self.box = document.createElement("div")
        self.box.className = "flex flex-col gap-6"

        self.username_box = document.createElement("div")
        self.username_header = document.createElement("p")
        self.username_header.className = "text-base text-gray-300 font-light my-3"
        self.username_header.innerHTML = "Username"
        self.username_input = document.createElement("input")
        self.username_input.type = "text"
        self.username_input.className = (
            "w-96 h-10 rounded-lg border border-gray-300 px-3"
        )

        self.password_box = document.createElement("div")
        self.password_header = document.createElement("p")
        self.password_header.className = "text-base text-gray-300 font-light my-3"
        self.password_header.innerHTML = "Password"
        self.password_input = document.createElement("input")
        self.password_input.type = "password"
        self.password_input.className = (
            "w-96 h-10 rounded-lg border border-gray-300 px-3"
        )

        self.button_box = document.createElement("div")
        self.button_login = document.createElement("button")
        self.button_login.className = "w-96 h-16 bg-orange-500 shadow-md rounded-full text-white text-lg font-medium my-4"
        self.button_login.innerHTML = "Login"
        self.button_login.onclick = self.login_click

        self.question_box = document.createElement("div")
        self.question_box.className = "flex flex-row justify-center"
        self.question_text = document.createElement("a")
        self.question_text.className = "text-gray-400 cursor-pointer"
        self.question_text.innerHTML = "Don't have an account?"
        self.question_text.onclick = self.redirect_to_register

        self.username_box.appendChild(self.username_header)
        self.username_box.appendChild(self.username_input)
        self.password_box.appendChild(self.password_header)
        self.password_box.appendChild(self.password_input)
        self.button_box.appendChild(self.button_login)
        self.question_box.appendChild(self.question_text)

        self.box.appendChild(self.username_box)
        self.box.appendChild(self.password_box)
        self.box.appendChild(self.button_box)
        self.box.appendChild(self.question_box)
        self.login.appendChild(self.box)
        self.element.appendChild(self.login)


class Navbar(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def redirect_to_root(self, event):
        js.window.location.href = "/"

    def drawWidget(self):
        self.navbar = document.createElement("div")
        self.navbar.className = "backdrop-blur-lg w-screen h-24 text-white flex justify-center items-center fixed z-10"
        self.title = document.createElement("a")
        self.title.innerHTML = "SukSaang"
        self.title.className = "font-signature font-extrabold text-5xl cursor-pointer"
        self.title.onclick = self.redirect_to_root
        self.navbar.appendChild(self.title)
        self.element.appendChild(self.navbar)


class NotFound(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def drawWidget(self):
        self.text = document.createElement("h1")
        self.text.className = "text-3xl text-white"
        self.text.innerHTML = "404 NOT FOUND"
        self.element.appendChild(self.text)


class Home(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.restaurant_name = "Restaurant Name"
        self.username = "John Doe"

    def drawWidget(self):
        self.container = document.createElement("div")
        self.container.className = "flex flex-col justify-center items-center gap-6 text-white"
        self.element.appendChild(self.container)

        self.logo = document.createElement("img")
        self.logo.src = "/restaurant.svg"
        self.logo.className = "w-48 h-48"
        self.container.appendChild(self.logo)

        self.name = document.createElement("h2")
        self.name.innerHTML = f"{self.restaurant_name}"
        self.name.className = "text-2xl font-semibold"
        self.container.appendChild(self.name)
        
        self.welcome_message = document.createElement("h3")
        self.welcome_message.innerHTML = f"Welcome, {self.username}"
        self.welcome_message.className = "text-lg font-base"
        self.container.appendChild(self.welcome_message)


if __name__ == "__main__":
    location_path = js.window.location.pathname

    Navbar("app").drawWidget()

    content = Layout("app")
    if location_path == "/":
        content.drawWidget([Welcome("content")])
    elif location_path == "/login":
        content.drawWidget([Login("content")])
    elif location_path == "/register":
        content.drawWidget([Login("content")])
    elif location_path == "/home":
        content.drawWidget([Home("content")])
    else:
        content.drawWidget([NotFound("content")])
