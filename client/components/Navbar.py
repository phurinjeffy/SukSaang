from __init__ import *

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

