from __init__ import *

class Home(AbstractWidget):
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
