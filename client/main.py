import json
import js
from pyscript import document
import requests
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
import base64
from io import BytesIO


def check_token():
    location_path = js.window.location.pathname
    if location_path in ["/", "/login", "/register", "/admin_login", "/admin_register"]:
        return

    access_token = js.window.localStorage.getItem("access_token")
    if not access_token:
        js.window.location.href = "/"
    else:
        if location_path.startswith("/admin"):
            url = "http://localhost:8000/admins/me"
        else:
            url = "http://localhost:8000/users/me"

        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            js.window.location.href = "/"


def fetch_user_info():
    access_token = js.window.localStorage.getItem("access_token")
    if access_token:
        url = "http://localhost:8000/users/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            username = data.get("username")
            return username
        else:
            print("Error fetching user info:", response.text)
    else:
        print("Access token not found. User not logged in.")


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
        check_token()

    def drawWidget(self, widgets):
        self.content = document.createElement("div")
        self.content.id = "content"
        self.content.className = (
            "pt-24 min-h-screen h-full min-w-fit w-full bg-gradient-to-br "
        )
        if js.window.location.pathname.startswith("/admin"):
            self.content.className += "from-zinc-950 via-gray-800 to-gray-700"
        elif js.window.location.pathname in ["/", "/login", "/register"]:
            self.content.className += "from-slate-500 to-slate-300"
        else:
            self.content.className += "from-blue-50 via-white to-blue-50"
        self.element.appendChild(self.content)

        for widget in widgets:
            widget.drawWidget()


class Welcome(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def redirect_to_user_login(self, event):
        js.window.location.href = "/login"

    def redirect_to_admin_login(self, event):
        js.window.location.href = "/admin_login"

    def drawWidget(self):
        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="flex flex-row justify-center items-center gap-20 mt-36 pb-8">
                <div class="user flex flex-col justify-center items-center gap-6 cursor-pointer hover:scale-105 duration-500">
                    <img class="w-44 h-44" src="/user.svg"/>
                    <p class="text-white text-3xl font-bold">User</p>
                </div>
                <div class="admin flex flex-col justify-center items-center gap-6 cursor-pointer hover:scale-105 duration-500">
                    <img class="w-44 h-44" src="/admin.svg"/>
                    <p class="text-white text-3xl font-bold">Admin</p>
                </div>
            </div>
        """
        self.element.appendChild(content)

        user_element = content.querySelector(".user")
        user_element.onclick = self.redirect_to_user_login

        admin_element = content.querySelector(".admin")
        admin_element.onclick = self.redirect_to_admin_login


class Navbar(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.nav = False
        location_path = js.window.location.pathname
        self.status = (
            "ADMIN"
            if location_path.startswith("/admin")
            and location_path not in ["/admin_login", "/admin_register"]
            else (
                "USER"
                if location_path
                not in ["/", "/login", "/register", "/admin_login", "/admin_register"]
                else False
            )
        )
        self.link_mapping = (
            {
                "/menu": "Menu",
                "/cart": "Cart",
                "": "Logout",
            }
            if self.status == "USER"
            else {
                "/admin_table": "View Table",
                "/admin_log": "View Log",
                "/admin_menu": "Adjust Menu",
                "": "Logout",
            }
        )

    def title_redirect(self, event):
        if self.status == "USER":
            js.window.location.href = "/home"
        elif self.status == "ADMIN":
            js.window.location.href = "/admin_home"
        else:
            js.window.location.href = "/"

    def toggle_menu(self, event):
        self.nav = not self.nav
        menu_container = self.element.querySelector(".menu-container")
        menu_btn = self.element.querySelector(".menu-btn")
        if self.nav:
            menu_btn.src = "/close.svg"
            menu_container.innerHTML = self.generate_menu_html()
        else:
            menu_btn.src = "/menu.svg"
            menu_container.innerHTML = ""

    def generate_menu_html(self):
        menu_elements = f'<ul class="flex flex-col justify-center items-center absolute top-0 left-0 w-full h-screen bg-gradient-to-b from-blue-300 to-blue-400 text-white md:hidden">'
        for url, text in self.link_mapping.items():
            menu_elements += f"""
                <li class="px-4 cursor-pointer capitalize py-6 text-4xl">
                    <a href="{url}">{text}</a>
                </li>
            """
        menu_elements += "</ul>"
        return menu_elements

    def logout_click(self, event):
        js.window.localStorage.removeItem("access_token")

    def drawWidget(self):
        content = document.createElement("div")

        li_elements = ""
        for url, text in self.link_mapping.items():
            li_elements += f"""
                <li class="px-4 cursor-pointer capitalize font-medium text-white hover:scale-105 duration-200">
                    <a href="{url}" class="{text.lower()}">{text}</a>
                </li>
            """

        content.innerHTML = f"""
            <div class="w-screen h-24 px-8 text-white flex {'bg-gradient-to-br from-blue-500 to-blue-400 justify-between' if self.status == "USER" else 'backdrop-blur-lg justify-between' if self.status == "ADMIN" else 'backdrop-blur-lg justify-center'} items-center fixed z-10">
                <a class="title font-signature font-extrabold text-5xl cursor-pointer">SukSaang</a>
                <div class="menu-container"></div>
                <ul class="hidden md:flex flex-row">
                    {li_elements if self.status in ["USER", "ADMIN"] else ""}
                </ul>
                <div class="menu cursor-pointer pr-4 z-10 text-gray-100 md:hidden">
                    {f'<img src="/close.svg" class="menu-btn w-10" />' if self.nav else f'<img src="/menu.svg" class="menu-btn w-10" />' if self.status in ["USER", "ADMIN"] else ""}
                </div>
            </div>
        """

        title = content.querySelector(".title")
        title.onclick = self.title_redirect

        menu = content.querySelector(".menu")
        menu.onclick = self.toggle_menu

        if self.status in ["USER", "ADMIN"]:
            logout = content.querySelector(".logout")
            logout.onclick = self.logout_click

        self.element.appendChild(content)


class NotFound(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def drawWidget(self):
        self.text = document.createElement("h1")
        self.text.className = "text-3xl text-black"
        self.text.innerHTML = "404 NOT FOUND"
        self.element.appendChild(self.text)


class Register(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def redirect_to_login(self, event):
        if js.window.location.pathname == "/register":
            js.window.location.href = "/login"
        elif js.window.location.pathname == "/admin_register":
            js.window.location.href = "/admin_login"

    def register_click(self, event):
        username = self.username_input.value
        password = self.password_input.value

        if js.window.location.pathname == "/register":
            url = "http://localhost:8000/users"
        elif js.window.location.pathname == "/admin_register":
            url = "http://localhost:8000/admins"
        data = {"username": username, "password": password}
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Register successful!")
            js.window.location.href = "/login"
        else:
            print("Error:", response.text)
            self.error_message.innerHTML = response.text

    def drawWidget(self):
        self.register = document.createElement("div")
        self.register.className = (
            "flex flex-col justify-center items-center w-screen gap-12 pt-10"
        )

        self.register_title = document.createElement("h3")
        self.register_title.innerHTML = "Sign Up"
        self.register_title.className = "text-4xl font-semibold font-medium text-white"
        self.register.appendChild(self.register_title)

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
        self.button_register = document.createElement("button")
        self.button_register.className = "w-96 h-16 bg-orange-500 shadow-md rounded-full text-white text-lg font-medium my-4"
        self.button_register.innerHTML = "Register"
        self.button_register.onclick = self.register_click

        self.question_box = document.createElement("div")
        self.question_box.className = "flex flex-row justify-center"
        self.question_text = document.createElement("a")
        self.question_text.className = "text-gray-200 cursor-pointer hover:underline"
        self.question_text.innerHTML = "Already have an account?"
        self.question_text.onclick = self.redirect_to_login

        self.username_box.appendChild(self.username_header)
        self.username_box.appendChild(self.username_input)
        self.password_box.appendChild(self.password_header)
        self.password_box.appendChild(self.password_input)
        self.button_box.appendChild(self.button_register)
        self.question_box.appendChild(self.question_text)

        self.error_message = document.createElement("p")
        self.error_message.className = "text-red-500"

        self.box.appendChild(self.username_box)
        self.box.appendChild(self.password_box)
        self.box.appendChild(self.button_box)
        self.box.appendChild(self.question_box)
        self.register.appendChild(self.box)
        self.register.appendChild(self.error_message)
        self.element.appendChild(self.register)


class Login(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def redirect_to_register(self, event):
        if js.window.location.pathname == "/login":
            js.window.location.href = "/register"
        elif js.window.location.pathname == "/admin_login":
            js.window.location.href = "/admin_register"

    def login_click(self, event):
        username = self.username_input.value
        password = self.password_input.value

        isUser = False
        isAdmin = False

        if js.window.location.pathname == "/login":
            isUser = True
            url = "http://localhost:8000/users/login"
        elif js.window.location.pathname == "/admin_login":
            isAdmin = True
            url = "http://localhost:8000/admins/login"
        data = {"username": username, "password": password}
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                access_token = data["access_token"]
                print("Login successful!")
                js.window.localStorage.setItem("access_token", access_token)
                if isUser:
                    js.window.location.href = "/home"
                elif isAdmin:
                    js.window.location.href = "/admin_home"
            else:
                message = data.get("detail", "Unknown error")
                print("Login failed:", message)
        else:
            print("Error:", response.text)
            self.error_message.innerHTML = response.text

    def drawWidget(self):
        self.login = document.createElement("div")
        self.login.className = (
            "flex flex-col justify-center items-center w-screen gap-12 pt-10"
        )

        self.login_title = document.createElement("h3")
        self.login_title.innerHTML = "Login"
        self.login_title.className = "text-4xl font-semibold font-medium text-white"
        self.login.appendChild(self.login_title)

        self.box = document.createElement("div")
        self.box.className = "flex flex-col gap-6"

        self.username_box = document.createElement("div")
        self.username_header = document.createElement("p")
        self.username_header.className = "text-base text-gray-200 font-light my-3"
        self.username_header.innerHTML = "Username"
        self.username_input = document.createElement("input")
        self.username_input.type = "text"
        self.username_input.className = (
            "w-96 h-10 rounded-lg border border-gray-300 px-3"
        )

        self.password_box = document.createElement("div")
        self.password_header = document.createElement("p")
        self.password_header.className = "text-base text-gray-200 font-light my-3"
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
        self.question_text.className = "text-gray-200 cursor-pointer hover:underline"
        self.question_text.innerHTML = "Don't have an account?"
        self.question_text.onclick = self.redirect_to_register

        self.username_box.appendChild(self.username_header)
        self.username_box.appendChild(self.username_input)
        self.password_box.appendChild(self.password_header)
        self.password_box.appendChild(self.password_input)
        self.button_box.appendChild(self.button_login)
        self.question_box.appendChild(self.question_text)

        self.error_message = document.createElement("p")
        self.error_message.className = "text-red-500"

        self.box.appendChild(self.username_box)
        self.box.appendChild(self.password_box)
        self.box.appendChild(self.button_box)
        self.box.appendChild(self.question_box)
        self.login.appendChild(self.box)
        self.login.appendChild(self.error_message)
        self.element.appendChild(self.login)


class Home(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.username = fetch_user_info()

    def redirect_to_menu(self, event):
        js.window.location.href = "/menu"

    def redirect_to_user_walkin(self, event):
        js.window.location.href = "/tables"

    def drawWidget(self):
        current_hour = js.Date.new().getHours()

        breakfast_image = "/breakfast-hero.png"
        lunch_image = "/lunch-hero.png"
        dinner_image = "/dinner-hero.png"

        if 6 <= current_hour < 12:
            image_src = breakfast_image
        elif 12 <= current_hour < 18:
            image_src = lunch_image
        else:
            image_src = dinner_image

        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="flex flex-col justify-center items-center p-10">
                <div class="flex lg:flex-row flex-col justify-center items-center gap-8">
                    <div class="flex flex-col gap-4 text-blue-950">
                        <h1 class="font-bold text-6xl">
                            Welcome, {self.username}
                        </h1>
                        <p class="font-medium text-2xl">
                            Order with a click, savor every bite.
                        </p>
                        <button class="menu-btn flex justify-center items-center gap-1 bg-blue-400 text-white w-fit mt-6 px-6 py-4 rounded-full hover:scale-105 duration-300">
                            View Menu
                            <img class="w-6" src="/arrow.svg" />
                        </button>
                    </div>
                    <div>
                        <div class="bg-cover bg-center bg-no-repeat" style="background-image: url('/hero-bg.png');"/>
                        <img class="w-full" src="{image_src}" />
                    </div>
                </div>
            </div>
            <div class="mt-14 mb-10 text-3xl font-semibold text-blue-950">
                Your food adventure starts here.
            </div>
            <div class="flex lg:flex-row flex-col justify-center items-center gap-6 bg-blue-400 py-10 px-14 rounded-xl text-white">
                <div class="walkin-btn w-24 flex flex-col justify-center items-center mx-10 gap-4 cursor-pointer hover:scale-105 duration-300">
                    <img class="" src="/walkin.svg" />
                    <p class="">Walk In</p>
                </div>
                <div onclick="window.location.href='/menu'" class="menu-btn w-24 flex flex-col justify-center items-center mx-10 gap-4 cursor-pointer hover:scale-105 duration-300">
                    <img class="" src="/table.svg" />
                    <p class="">Menu</p>
                </div>
            </div>
        """
        self.element.appendChild(content)

        menu_btn = content.querySelector(".menu-btn")
        menu_btn.onclick = self.redirect_to_menu

        walkin_btn = content.querySelector(".walkin-btn")
        walkin_btn.onclick = self.redirect_to_user_walkin


class Menu(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.categories = ["rice", "noodle", "pasta", "steak", "soup", "sides"]
        self.selected_category = None
        self.opened_modal = None

    def fetch_menu_info(self):
        url = "http://localhost:8000/menus"
        response = requests.get(url)
        if response.status_code == 200:
            self.menu = response.json()["menus"]
        else:
            print("Error fetching menu:", response.text)

    def handle_menu_item_click(self, event):
        if self.opened_modal:
            self.opened_modal.close_modal()
        menu_item_name = event.currentTarget.querySelector("h3").textContent
        document.body.style.overflow = "hidden"
        self.opened_modal = Detail("content", menu_item_name)
        self.opened_modal.drawWidget()

    def handle_category_click(self, event):
        category = event.currentTarget.querySelector("p").textContent.lower()
        self.selected_category = category
        self.drawWidget()

    def drawWidget(self):
        # Fetch menu information every time drawWidget is called
        self.fetch_menu_info()

        # Filter menu items based on selected category
        if self.selected_category:
            filtered_menu = [
                item
                for item in self.menu
                if item.get("type", "").lower() == self.selected_category
            ]
        else:
            filtered_menu = self.menu

        svg_images = ""
        for category in self.categories:
            svg_images += f"""
                <div class="flex flex-col justify-center items-center hover:scale-105 duration-300 cursor-pointer category-item">
                    <img class="w-24 h-24 m-1" src="/category/{category}.svg" />
                    <p class="capitalize font-light text-base">{category}</p>
                </div>
            """

        menu_container = ""
        for item in filtered_menu:
            menu_container += f"""
                <div class="menu-item flex flex-col justify-center items-center hover:scale-105 duration-300 cursor-pointer">
                    <img class="w-32 h-32 mb-1" src="{item['photo']}" />
                    <h3 class="capitalize font-light text-sm sm:text-lg">{item['name']}</h3>
                    <p class="text-sm font-light">฿ {item['price']}</p>
                </div>
            """

        # Remove existing content
        if self.element.firstChild:
            self.element.removeChild(self.element.firstChild)

        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="flex flex-col justify-center items-center text-gray-700">
                <div class="w-full">
                    <div class="text-2xl font-extralight bg-blue-200 p-6">
                        Categories
                    </div>
                    <div class="flex flex-row gap-8 bg-white border-b border-slate-400 border-opacity-75 p-8">
                        {svg_images}
                    </div>
                </div>
                <div class="w-full">
                    <div class="text-2xl font-extralight bg-blue-100 p-6">
                        {self.selected_category.capitalize() if self.selected_category else 'Recommended'}
                    </div>
                    <div class="flex flex-row gap-8 bg-white border-b border-slate-400 border-opacity-75 p-10">
                        {menu_container}
                    </div>
                </div>
                <div class="fixed bottom-0 right-0 rounded-lg bg-blue-400 z-10 py-4 px-6 flex justify-center items-center gap-4 cursor-pointer" onclick="window.location.href='/cart'">
                    <img class="w-10 h-10" src="/cart.svg"/>
                </div>
            </div>
        """
        self.element.appendChild(content)

        # Bind event for category items
        category_items = self.element.querySelectorAll(".category-item")
        for category_item in category_items:
            category_item.onclick = self.handle_category_click

        # Bind event for menu items
        menu_items = self.element.querySelectorAll(".menu-item")
        for menu_item in menu_items:
            menu_item.onclick = self.handle_menu_item_click


class Detail(AbstractWidget):
    def __init__(self, element_id, menu_item):
        AbstractWidget.__init__(self, element_id)
        self.menu_item = menu_item
        self.item = None
        self.quantity = 1
        self.fetch_menu_item_info()
        self.modal_content = None

    def fetch_menu_item_info(self):
        url = f"http://localhost:8000/menus/{self.menu_item}"
        response = requests.get(url)
        if response.status_code == 200:
            self.item = response.json()
        else:
            print("Error fetching menu item:", response.text)

    def close_modal(self, event=None):
        if self.modal_content:
            self.element.removeChild(self.modal_content)
            document.body.style.overflow = "auto"
            self.modal_content = None

    def add_to_cart(self, event, quantity):
        username = fetch_user_info()
        food_name = self.item["name"]

        url = f"http://localhost:8000/users/{username}/cart?food_name={food_name}&quantity={quantity}"
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print("Succesfully Added to Cart")
        else:
            print("Error:", response.text)
        self.close_modal()

    def drawWidget(self):
        self.modal_content = document.createElement("div")
        self.modal_content.innerHTML = f"""
            <div class="w-2/5 bg-blue-300 rounded-lg p-8 border border-white shadow-lg fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                <span class="close text-white cursor-pointer">&times;</span>
                <div class="flex flex-col justify-center items-center text-white gap-6">
                    <img class="w-44 w-44" src={self.item['photo']} />
                    <p class="font-semibold text-lg">{self.item['name']}</p>
                    <ul class="list-disc font-extralight text-sm">
                        <li>
                            <span class="font-medium mr-1">Price: </span> ฿{self.item['price']}
                        </li>
                        <li>
                            <span class="font-medium mr-1">Description: </span> {self.item['description']}
                        </li>
                        <li>
                            <span class="font-medium mr-1">Type: </span> {self.item['type']}
                        </li>
                        <li>
                            <span class="font-medium mr-1">Ingredients: </span> {self.item['ingredients']}
                        </li>
                    </ul>
                    <div class="flex flex-row gap-4">
                        <button class="decrement"> - </button>
                        <p class="quantity">{self.quantity}</p>
                        <button class="increment"> + </button>
                    </div>
                    <button class="add-btn hover:scale-105 duration-500">Add to Cart</button>
                </div>
            </div>
        """
        self.element.appendChild(self.modal_content)

        close_button = self.modal_content.querySelector(".close")
        close_button.onclick = self.close_modal

        self.quantity_element = self.modal_content.querySelector(".quantity")

        def decrement(event):
            if self.quantity > 1:
                self.quantity -= 1
                self.quantity_element.textContent = self.quantity

        def increment(event):
            self.quantity += 1
            self.quantity_element.textContent = self.quantity

        decrement_button = self.modal_content.querySelector(".decrement")
        decrement_button.onclick = decrement
        increment_button = self.modal_content.querySelector(".increment")
        increment_button.onclick = increment

        self.add_button = self.modal_content.querySelector(".add-btn")
        self.add_button.onclick = lambda event: self.add_to_cart(event, self.quantity)


class Cart(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.username = fetch_user_info()
        self.cart = None
        self.subtotal = 0
        self.check = 0
        self.fetch_cart_info()

    def fetch_menu_item_info(self, menu_name):
        url = f"http://localhost:8000/menus/{menu_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching menu item:", response.text)

    def fetch_cart_info(self):
        if self.check == 0:
            url = f"http://localhost:8000/users/{self.username}/cart"
            response = requests.get(url)
            if response.status_code == 200:
                self.cart = response.json()["cart"]
            else:
                print("Error fetching menu:", response.text)

    def delete_cart(self, food_name, quantity):
        url = f"http://localhost:8000/users/{self.username}/cart/{food_name}?quantity={quantity}"
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("Successfully Updated Quantity")
        else:
            print("Error:", response.text)

    def place_order(self, event):
        url = f"http://localhost:8000/users/{self.username}/orders/place_order"
        response = requests.post(url)
        if response.status_code == 200:
            print("Successfully Placed Order")
            self.cart = []  # Empty the cart
            self.subtotal = 0  # Reset the subtotal to zero
            self.check = 1
            self.drawWidget()
            js.alert("Placed Order Successfully")
        else:
            print("Error placing order:", response.text)

    def drawWidget(self):
        items_container = ""
        for i, item in enumerate(self.cart):
            total = int(item["price"] * item["quantity"])
            menu = self.fetch_menu_item_info(item["name"])
            items_container += f"""
                <tr class="border-b border-gray-500 font-light">
                    <td>
                        <div class="flex flex-row justify-start items-center gap-4 p-4 pr-0">
                            <img class="w-14 h-14 mb-1" src={menu['photo']} />
                            <p class="capitalize text-base sm:text-lg">{item['name']}</p>
                        </div>
                    </td>
                    <td class="text-right">
                        ฿ {item['price']}
                    </td>
                    <td class="text-right">
                        <div class="flex flex-row gap-4 justify-end">
                            <button class="decrement" data-index="{i}"> - </button>
                            <p class="quantity text-sm">{item['quantity']}</p>
                            <button class="increment" data-index="{i}"> + </button>
                        </div>
                    </td>
                    <td class="text-right p-4 pl-0">
                        ฿ <span class="total">{total}</span>
                    </td>
                </tr>
            """
            self.subtotal += total

        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="w-full flex flex-col items-center text-black gap-8 py-10">
                <div class="text-4xl font-light">
                    Cart
                </div>
                <div class="w-screen px-10">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b border-gray-500">
                                <th class="font-light text-left p-4 pr-0">Item</th>
                                <th class="font-light text-right">Price</th>
                                <th class="font-light text-right">Quantity</th>
                                <th class="font-light text-right p-4 pl-0">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_container}
                        </tbody>
                    </table>
                </div>
                <div class="font-base">
                    Subtotal: ฿ <span class="subtotal">{self.subtotal}</span>
                </div>
                <button class="place-order-btn mt-10 text-white bg-blue-500 rounded-full p-8 cursor-pointer">
                    Place Order
                </button>
            </div>
        """
        self.element.innerHTML = (
            ""  # Clear the content of the element before appending the new content
        )
        self.element.appendChild(content)

        place_order_btn = self.element.querySelector(".place-order-btn")
        place_order_btn.onclick = self.place_order

        def update_quantity(event, amount):
            item_index = int(event.target.dataset.index)
            food_name = self.cart[item_index]["name"]

            if self.cart[item_index]["quantity"] >= 1:
                self.delete_cart(food_name, -amount)

                self.cart[item_index]["quantity"] += amount
                price_change = self.cart[item_index]["price"] * amount

                quantity_element = event.target.parentElement.querySelector(".quantity")
                quantity_element.textContent = self.cart[item_index]["quantity"]

                total_element = event.target.parentElement.parentElement.nextElementSibling.querySelector(
                    ".total"
                )
                total_element.textContent = (
                    int(total_element.textContent) + price_change
                )

                subtotal_element = self.element.querySelector(".subtotal")
                subtotal_element.textContent = (
                    int(subtotal_element.textContent) + price_change
                )

                if self.cart[item_index]["quantity"] == 0:
                    row = event.target.closest("tr")
                    row.parentNode.removeChild(row)

        decrement_buttons = self.element.querySelectorAll(".decrement")
        for button in decrement_buttons:
            button.onclick = lambda event: update_quantity(event, -1)

        increment_buttons = self.element.querySelectorAll(".increment")
        for button in increment_buttons:
            button.onclick = lambda event: update_quantity(event, 1)


class TableUser(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.tables = None
        self.fetch_table_info()
        self.username = fetch_user_info()
        self.table_select = 0

    def fetch_table_info(self):
        url = "http://localhost:8000/tables"
        response = requests.get(url)
        if response.status_code == 200:
            self.tables = response.json()["tables"]
        else:
            print("Error fetching logs:", response.text)

    def redirect_to_menu(self):
        js.window.location.href = "/menu"

    def drawWidget(self):
        content = document.createElement("div")
        content.setAttribute("class", "flex flex-col justify-center items-center")

        tables_container = document.createElement("div")
        tables_container.setAttribute("class", "w-full grid grid-cols-3 gap-4 p-8")

        for table in self.tables:
            table_div = document.createElement("div")
            table_div.onclick = self.tableClicked
            table_div.setAttribute(
                "class",
                f"table-item p-4 rounded flex justify-center items-center {'bg-blue-100 hover:scale-105 duration-300 cursor-pointer' if not table['customers'] else 'bg-red-200 cursor-not-allowed'}",
            )
            table_div.setAttribute("data-table-id", str(table["table_num"]))
            table_div.innerHTML = f"""
                <div class="text-lg font-semibold">Table {table['table_num']}</div>
            """
            tables_container.appendChild(table_div)

        content.appendChild(tables_container)

        confirm_button = document.createElement("button")
        confirm_button.setAttribute("class", "confirm-button")
        confirm_button.innerHTML = "Confirm Table"
        confirm_button.onclick = self.confirmBooking
        content.appendChild(confirm_button)

        self.element.appendChild(content)

    def tableClicked(self, event):
        table_div = event.target.closest(".table-item")
        if table_div:
            table_id = table_div.getAttribute("data-table-id")
            if self.table_select != table_id:
                prev_table_div = self.element.querySelector(
                    f'.table-item[data-table-id="{self.table_select}"]'
                )
                if prev_table_div:
                    prev_table_color = prev_table_div.getAttribute("data-prev-color")
                    prev_table_div.style.backgroundColor = prev_table_color

            self.table_select = table_id
            # Store the current background color in a data attribute
            table_div.setAttribute("data-prev-color", table_div.style.backgroundColor)
            table_div.style.backgroundColor = "yellow"

    def confirmBooking(self, event):
        if self.table_select is not None:
            table_id = self.table_select
            for table in self.tables:
                if str(table["table_num"]) == self.table_select:
                    if table["available"]:
                        confirm = js.confirm(f"Confirm for Table {table_id}?")
                        if confirm:
                            self.table_add_customer()
                            js.alert("Successful")
                    else:
                        print(f"Table {table_id} is not available for booking.")
                        js.alert(f"Table {table_id} is not available for booking.")
                    break
        else:
            print("No table selected.")
            js.alert("No table selected.")

    def table_add_customer(self):
        table_num = self.table_select

        url = f"http://localhost:8000/tables/{int(table_num)}/customers"
        response = requests.post(url, self.username)

        if response.status_code == 200:
            print(f"Customer added successfully")
            self.redirect_to_menu()
        else:
            print(f"Failed to add customer:", response.text)


class Booking(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.tables = None
        self.fetch_table_info()
        self.username = fetch_user_info()
        self.table_select = 0

    def fetch_table_info(self):
        url = "http://localhost:8000/tables"
        response = requests.get(url)
        if response.status_code == 200:
            self.tables = response.json()["tables"]
        else:
            print("Error fetching logs:", response.text)

    def redirect_to_menu(self):
        js.window.location.href = "/menu"

    def drawWidget(self):
        # Use Tailwind's flex, flex-wrap, and justify-center classes for the container
        tables_container = document.createElement("div")
        tables_container.setAttribute(
            "class", "flex flex-wrap justify-center space-x-4 space-y-4"
        )
        for table in self.tables:
            table_div = document.createElement("div")
            table_div.onclick = self.tableClicked
            # Add `cursor-not-allowed` and `opacity-50` for booked tables to make it clear they are not selectable
            table_class_list = [
                "table-item",
                "p-4",
                "m-2",
                "rounded",
                "shadow",
                "transition-colors",
            ]
            if table["customers"]:
                table_class_list.extend(
                    ["bg-blue-500", "cursor-not-allowed", "opacity-50"]
                )
            else:
                table_class_list.append("bg-gray-300")
            table_div.setAttribute("class", " ".join(table_class_list))
            table_div.setAttribute("data-table-id", str(table["table_num"]))
            table_div.innerHTML = (
                f"<div class='text-lg font-semibold'>{table['table_num']}</div>"
            )
            table_div.dataset.available = str(not table["customers"])
            tables_container.appendChild(table_div)
        # Append table grid container
        self.element.innerHTML = ""  # Clear the previous content
        self.element.appendChild(tables_container)
        # Confirmation button with Tailwind classes
        confirm_button = document.createElement("button")
        confirm_button.setAttribute(
            "class",
            "mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded",
        )
        confirm_button.innerHTML = "Confirm Table"
        confirm_button.onclick = self.confirmBooking
        self.element.appendChild(confirm_button)

    def tableClicked(self, event):
        table_div = event.target.closest(".table-item")
        if table_div:
            # Remove selection class from previously selected table
            if self.table_select:
                prev_table_div = self.element.querySelector(
                    f'.table-item[data-table-id="{self.table_select}"]'
                )
                prev_table_div.classList.remove("ring-2", "ring-yellow-500")
            # Set the new selection
            table_id = table_div.getAttribute("data-table-id")
            self.table_select = table_id
            table_div.classList.add("ring-2", "ring-yellow-500")

    def confirmBooking(self, event):
        if self.table_select:
            selected_table_div = self.element.querySelector(
                f'[data-table-id="{self.table_select}"]'
            )
            # Only proceed if the selected table is available for booking
            if selected_table_div.dataset.available == "True":
                table_id = self.table_select
                # Run through each table to see if the selected one matches and is available
                for table in self.tables:
                    if str(table["table_num"]) == table_id and not table["customers"]:
                        self.table_add_customer()
                        break
                js.window.location.href = "/home"
            else:
                print(
                    f"Table {self.table_select} is already booked or is not available for booking."
                )
            self.table_select = None  # Reset the selection
        else:
            print("No table selected.")

    def table_add_customer(self):
        table_num = self.table_select
        url = f"http://localhost:8000/tables/{table_num}/customers"
        response = requests.post(url, self.username)
        if response.status_code == 200:
            print(f"Customer added successfully")
            self.redirect_to_menu()
        else:
            print(f"Failed to add customer:", response.text)


class AdminHome(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.stats = None
        self.fetch_stats_info()

    def fetch_stats_info(self):
        url = f"http://localhost:8000/stats"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Stats fetched successfully")
            self.stats = response.json()["stats"]
            self.updateStats()
        else:
            print(f"Failed to get stats:", response.text)

    def updateStats(self, selected_month=datetime.date.today().month):
        self.month = selected_month

        filtered_stats = [
            data
            for data in self.stats
            if datetime.datetime.strptime(data["date"], "%Y-%m-%d").month == self.month
        ]

        self.dates = [data["date"] for data in filtered_stats]
        self.incomes = [data["income"] for data in filtered_stats]
        self.costs = [data["cost"] for data in filtered_stats]

        bar_width = 0.35

        x = range(len(self.dates))
        x1 = [i - bar_width / 2 for i in x]  # Position for the income bars
        x2 = [i + bar_width / 2 for i in x]  # Position for the cost bars

        plt.bar(x1, self.incomes, width=bar_width, label="Income")
        plt.bar(x2, self.costs, width=bar_width, label="Cost")

        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.xticks(x, self.dates)
        plt.legend()

        # Convert the Matplotlib plot to a base64-encoded string
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        self.image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        self.incomes_total = sum(self.incomes)
        self.costs_total = sum(self.costs)

        chartElement = document.querySelector("#chart")
        if chartElement:
            chartElement.setAttribute(
                "src", f"data:image/png;base64,{self.image_base64}"
            )

        incomesElement = document.querySelector("#incomes_total")
        if incomesElement:
            incomesElement.textContent = str(self.incomes_total)

        costsElement = document.querySelector("#costs_total")
        if costsElement:
            costsElement.textContent = str(self.costs_total)

    def drawWidget(self):
        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="flex flex-col justify-center items-center text-white gap-4">
                <h3 class="font-semibold text-3xl my-4">Statistics</h3>
                <img id="chart" src="data:image/png;base64,{self.image_base64}" alt="Income and Cost Chart">
                <div class="flex flex-col">
                    <h2>Stats for <span class="text-black"><select id="month-select">{self.get_month_options()}</select></span></h2>
                    <table>
                        <tr>
                            <td>Total Incomes:</td>
                            <td class="text-right">฿<span id="incomes_total" >{self.incomes_total}</span></td>
                        </tr>
                        <tr>
                            <td>Total Costs:</td>
                            <td class="text-right">฿<span id="costs_total">{self.costs_total}</span></td>
                        </tr>
                    </table>
                </div>
            </div>
        """
        self.element.appendChild(content)

        month_select = content.querySelector("#month-select")
        month_select.onchange = lambda event: self.onMonthSelectChange(event)

    def onMonthSelectChange(self, event):
        selected_month = event.target.value
        self.updateStats(int(selected_month))
        
    def get_month_options(self):
        options = ""
        for i in range(1, 13):
            month_name = datetime.date(1900, i, 1).strftime("%B")
            selected = "selected" if i == self.month else ""
            options += f'<option value="{i}" {selected}>{month_name}</option>'
        return options


class AdminTable(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.table = None
        self.customers = None
        self.opened_modal = None
        self.fetch_table_info()

    def fetch_table_info(self):
        url = "http://localhost:8000/tables"
        response = requests.get(url)
        if response.status_code == 200:
            self.table = response.json()["tables"]
        else:
            print("Error fetching menu:", response.text)

    def fetch_table_customer_info(self, table_num):
        url = f"http://localhost:8000/tables/{table_num}/customers"
        response = requests.get(url)
        if response.status_code == 200:
            self.customers = response.json()
        else:
            print("Error fetching table info:", response.text)

    def view_order(self, table_num):
        url = f"http://localhost:8000/tables/{table_num}/orders"
        response = requests.get(url)
        if response.status_code == 200:
            orders = response.json()
            if self.opened_modal:
                self.opened_modal.close_modal()
            document.body.style.overflow = "hidden"
            self.opened_modal = Receipt("content", orders, table_num)
            self.opened_modal.drawWidget()

        else:
            print("Error fetching orders:", response.text)

    def check_out(self, table_num):
        url = f"http://localhost:8000/table/{table_num}/checkout"
        response = requests.put(url)
        if response.status_code == 200:
            print("Check out successful")
            js.alert("Check out successful")
            js.window.location.reload()
        else:
            print("Error checking out")
            js.alert("Error:", response.text)

    def drawWidget(self):
        tables_container = ""
        for table in self.table:
            self.fetch_table_customer_info(int(table["table_num"]))

            tables_container += f"""
                <tr class="border-b border-gray-500 font-light">
                    <td class="p-4 pr-0">{table['table_num']}</td>
                    <td>{self.customers}</td>
                    <td class="view-order cursor-pointer" id="view-order-{table['table_num']}">View Order</td>
                    <td><button id="check-out-{table['table_num']}">Check Out</button></td>
                </tr>
            """

        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="w-full flex flex-col items-center text-white gap-8 py-10">
                <div class="text-4xl font-semibold">
                    Tables
                </div>
                <div class="w-screen px-10 my-6">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b border-gray-500">
                                <th class="font-light text-left p-4 pr-0">Table</th>
                                <th class="font-light text-left">Customers</th>
                                <th class="font-light text-left">Orders</th>
                                <th class="font-light text-left">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tables_container}
                        </tbody>
                    </table>
                </div>
            </div>
        """
        self.element.appendChild(content)

        def handle_view_order_click(table_num):
            return lambda event: self.view_order(table_num)

        def handle_check_out_click(table_num):
            return lambda event: self.check_out(table_num)

        # Attach event handlers for the buttons
        for table in self.table:
            view_order_button = content.querySelector(
                f"#view-order-{table['table_num']}"
            )
            view_order_button.onclick = handle_view_order_click(int(table["table_num"]))
            check_out_button = content.querySelector(f"#check-out-{table['table_num']}")
            check_out_button.onclick = handle_check_out_click(int(table["table_num"]))


class Receipt(AbstractWidget):
    def __init__(self, element_id, orders, table_num):
        AbstractWidget.__init__(self, element_id)
        self.orders = orders
        self.table_num = table_num
        self.modal_content = None
        self.show_table_payment(table_num)
        self.payment_image = f"https://promptpay.io/0824468446/{self.payment}.png"

    def show_table_payment(self, table_num):
        url = f"http://localhost:8000/table/{table_num}/payment"
        response = requests.get(url)
        if response.status_code == 200:
            self.payment = str(response.json()["total_payment"])
        else:
            print("Error fetching table info:", response.text)

    def close_modal(self, event=None):
        if self.modal_content:
            self.element.removeChild(self.modal_content)
            document.body.style.overflow = "auto"
            self.modal_content = None

    def drawWidget(self):
        self.modal_content = document.createElement("div")

        modal_content = "<ul class='list-disc font-extralight text-sm'>"
        for order in self.orders:
            modal_content += f"<li class='font-medium mr-1'>{order['name']} - ฿{order['price']} - x {order['quantity']} = ฿{order['price']*order['quantity']}</li>"
        modal_content += "</ul>"

        self.modal_content.innerHTML = f"""
            <div class="w-2/5 bg-zinc-800 rounded-lg p-8 border border-white shadow-lg fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                <span class="close text-white cursor-pointer">&times;</span>
                <div class="flex flex-col justify-center items-center text-white gap-6">
                    <p class="font-semibold text-lg">Table {self.table_num} | Orders</p>
                    {modal_content}
                    <p class="font-semibold text-base">Total: ฿{self.payment}</p>
                    {
                       f'<img src="{self.payment_image}" alt="Payment" style="max-width: 80%; max-height: 80%;">' if self.payment != "0" else ''
                    }
                </div>
            </div>
        """
        self.element.appendChild(self.modal_content)

        close_button = self.modal_content.querySelector(".close")
        close_button.onclick = self.close_modal


class AdminLog(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.logs = None
        self.fetch_log_info()

    def fetch_log_info(self):
        url = "http://localhost:8000/logs"
        response = requests.get(url)
        if response.status_code == 200:
            self.logs = response.json()
        else:
            print("Error fetching logs:", response.text)

    def drawWidget(self):
        table_rows = ""
        for log in self.logs:
            l = log.split(" - ", 2)
            if len(l) == 3:
                table_rows += f"""
                    <tr>
                        <td class="px-4 py-2 text-left bg-gray-800 border">{l[0]}</td>
                        <td class="px-4 py-2 text-left bg-gray-800 border">{l[1]}</td>
                        <td class="px-4 py-2 text-left bg-gray-800 border">{l[2]}</td>
                    </tr>
                """
            else:
                print("Unexpected log format:", log)

        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="flex flex-col justify-center items-center text-white mx-12 pb-12">
                <div class="text-4xl font-semibold my-6">
                    Logs
                </div>
                <table class="table-auto w-full">
                    <thead>
                        <tr>
                            <th class="px-4 py-2 text-left bg-gray-900 border">Timestamp</th>
                            <th class="px-4 py-2 text-left bg-gray-900 border">Level</th>
                            <th class="px-4 py-2 text-left bg-gray-900 border">Message</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        """
        self.element.appendChild(content)


class AdminMenu(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)
        self.menu = []
        self.add_toggle = False
        self.fetch_menu_info()

    def fetch_menu_info(self):
        url = "http://localhost:8000/menus"
        response = requests.get(url)
        if response.status_code == 200:
            self.menu = response.json()["menus"]
        else:
            print("Error fetching menu:", response.text)

    def toggle_edit_mode(self, event):
        row = event.target.closest("tr")
        cells = list(row.querySelectorAll("td"))
        edit_button = row.querySelector(".edit-btn")

        if edit_button.innerHTML == "Save":
            updated_data = {}
            food_name = cells[1].dataset.originalValue
            updated_cells = []

            for cell in cells[:-2]:
                field_name = cell.dataset.field
                if field_name == "photo":
                    continue
                value = cell.querySelector("input").value
                updated_data[field_name] = value
                updated_cells.append((cell, value))

            success = self.edit_menu(food_name, updated_data)
            if success:
                for cell, value in updated_cells:
                    cell.innerHTML = value
                    cell.classList.remove("edit-mode")
                edit_button.innerHTML = "Edit"
                delete_button = row.querySelector(".delete-btn")
                delete_button.remove()
            else:
                js.alert("Failed to update menu.")
        else:
            for cell in cells[:-1]:
                cell.classList.add("edit-mode")
                cell.dataset.originalValue = cell.innerHTML.strip()
                if cell.dataset.field:
                    if cell.dataset.field != "photo":
                        cell.innerHTML = f'<input class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" value="{cell.innerHTML.strip()}" />'
            edit_button.innerHTML = "Save"
            delete_button = document.createElement("td")
            delete_button.className = "delete-btn cursor-pointer"
            delete_button.innerHTML = f"<img src='/trash.svg' class='w-6' />"
            delete_button.onclick = self.delete_menu_row
            row.appendChild(delete_button)

    def edit_menu(self, food_name, updated_data):
        url = f"http://localhost:8000/menus/{food_name}"
        headers = {"Content-Type": "application/json"}
        response = requests.patch(url, headers=headers, params=updated_data)
        if response.status_code == 200:
            print(f"Menu '{food_name}' updated successfully")
            return True
        else:
            print(f"Failed to update menu '{food_name}':", response.text)
            return False

    def add_clicked(self, event):
        self.add_toggle = not self.add_toggle
        new_container = document.querySelector(".new-container")
        if self.add_toggle:
            new_container.classList.remove("hidden")
            add_btn = new_container.querySelector(".add-btn")
            add_btn.onclick = self.add_menu
        else:
            new_container.classList.add("hidden")

    def add_menu(self, event):
        def upload_file():
            url = "http://localhost:8000/menus"
            response = requests.post(url, data=form_data, files=files)

            if response.status_code == 200:
                print(f"Menu added successfully")
                form.classList.add("hidden")
                js.window.location.reload(True)
            else:
                print(f"Failed to add menu:", response.text)
                error = document.querySelector(".error-msg")
                error.innerHTML = f"Failed to add menu: {response.text}"

        form = document.querySelector(".new-container")

        form_data = {
            "category": form.querySelector("#new-category").value,
            "name": form.querySelector("#new-name").value,
            "description": form.querySelector("#new-description").value,
            "type": form.querySelector("#new-type").value,
            "price": form.querySelector("#new-price").value,
            "cost": form.querySelector("#new-cost").value,
            "ingredients": form.querySelector("#new-ingredients").value.split(","),
        }

        files = {}
        photo_input = form.querySelector("#new-photo")
        if photo_input and photo_input.files.length > 0:
            photo_file = photo_input.files.item(0)

            # Use FileReader API to read the file as base64 encoded string
            reader = js.FileReader.new()
            reader.readAsDataURL(photo_file)

            # Define a callback function to handle the file reading completion
            def file_loaded(event):
                file_data = reader.result.split(",")[1]  # Extract base64 data
                files["photo"] = (photo_file.name, file_data, photo_file.type)
                form_data["photo"] = (photo_file.name, file_data, photo_file.type)
                upload_file()

            reader.onload = file_loaded

        else:
            print("No photo selected.")
            upload_file()

    def delete_menu(self, food_name):
        url = f"http://localhost:8000/menus/{food_name}"
        response = requests.delete(url)
        if response.status_code == 200:
            print(f"Menu '{food_name}' deleted successfully")
            return True
        else:
            print(f"Failed to delete menu '{food_name}':", response.text)
            return False

    def delete_menu_row(self, event):
        row = event.target.closest("tr")
        cells = list(row.querySelectorAll("td"))
        food_name = cells[1].dataset.originalValue
        confirm = js.window.confirm(f"Are you sure you want to remove '{food_name}'?")
        if confirm:
            success = self.delete_menu(food_name)
            if success:
                row.remove()

    def drawWidget(self):
        items_container = ""
        for item in self.menu:
            items_container += f"""
                <tr class="border-b border-gray-500 font-light">
                    <td class="p-4 pr-0 flex gap-4 items-center" data-field="photo">
                        <img class="w-10 h-10" src="{item['photo']}" />
                    </td>
                    <td class="text-left" data-field="name">
                        {item['name']}
                    </td>
                    <td class="text-left" data-field="description">
                        {item['description']}
                    </td>
                    <td class="text-left" data-field="type">
                        {item['type']}
                    </td>
                    <td class="text-left" data-field="ingredients">
                        {item['ingredients']}
                    </td>
                    <td class="text-right" data-field="price">
                        {item['price']}
                    </td>
                    <td class="text-right" data-field="cost">
                        {item['cost']}
                    </td>
                    <td class="edit-btn text-right cursor-pointer">
                        Edit
                    </td>
                </tr>
            """

        content = document.createElement("div")
        content.innerHTML = f"""
            <div class="w-full flex flex-col items-center text-white gap-8 py-10">
                <div class="text-4xl font-semibold">
                    Adjust Menu
                </div>
                <div class="w-screen px-10 my-6">
                    <table class="w-full">
                        <thead>
                            <tr class="border-b border-gray-500">
                                <th class="font-light text-left p-4 pr-0">Name</th>
                                <th class="font-light text-left"></th>
                                <th class="font-light text-left">Description</th>
                                <th class="font-light text-left">Type</th>
                                <th class="font-light text-left">Ingredients</th>
                                <th class="font-light text-right">Price</th>
                                <th class="font-light text-right">Cost</th>
                                <th class="font-light text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_container}
                        </tbody>
                    </table>
                </div>
                <div class="new-container hidden flex flex-col justify-center items-center gap-2">
                    <select id="new-category" class="w-full text-black border border-gray-300 rounded px-3 py-1">
                        <option value="MAIN">Main</option>
                        <option value="DRINK">Drink</option>
                        <option value="DESSERT">Dessert</option>
                    </select>
                    <input id="new-photo" class="w-full border border-gray-300 rounded px-3 py-1" type="file" accept="image/*">
                    <input id="new-name" class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" placeholder="Name">
                    <input id="new-description" class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" placeholder="Description">
                    <input id="new-type" class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" placeholder="Type">
                    <input id="new-ingredients" class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" placeholder="Ingredients">
                    <input id="new-price" class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" placeholder="Price">
                    <input id="new-cost" class="w-full text-black border border-gray-300 rounded px-3 py-1" type="text" placeholder="Cost">
                    <button class="add-btn">Add</button>
                </div>
                <div class="new-btn cursor-pointer flex flex-col justify-center items-center hover:scale-105 duration-300 gap-2">
                    <img src="/add.svg" class="w-10" />
                    Add Item
                </div>
                <div class="error-msg text-red-500 text-center"></div>
            </div>
        """
        self.element.appendChild(content)

        edit_buttons = content.querySelectorAll(".edit-btn")
        for button in edit_buttons:
            button.onclick = self.toggle_edit_mode

        new_button = content.querySelector(".new-btn")
        new_button.onclick = self.add_clicked


if __name__ == "__main__":
    location_path = js.window.location.pathname

    Navbar("app").drawWidget()

    content = Layout("app")
    if location_path == "/":
        content.drawWidget([Welcome("content")])
    elif location_path in ["/login", "/admin_login"]:
        content.drawWidget([Login("content")])
    elif location_path in ["/register", "/admin_register"]:
        content.drawWidget([Register("content")])
    elif location_path == "/home":
        content.drawWidget([Home("content")])
    elif location_path == "/tables":
        content.drawWidget([TableUser("content")])
    elif location_path == "/booking":
        content.drawWidget([Booking("content")])
    elif location_path == "/menu":
        content.drawWidget([Menu("content")])
    elif location_path == "/cart":
        content.drawWidget([Cart("content")])
    elif location_path == "/admin_home":
        content.drawWidget([AdminHome("content")])
    elif location_path == "/admin_table":
        content.drawWidget([AdminTable("content")])
    elif location_path == "/admin_log":
        content.drawWidget([AdminLog("content")])
    elif location_path == "/admin_menu":
        content.drawWidget([AdminMenu("content")])
    else:
        content.drawWidget([NotFound("content")])
