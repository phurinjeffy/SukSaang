from __init__ import *

class NotFound(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def drawWidget(self):
        self.text = document.createElement("h1")
        self.text.className = "text-3xl text-white"
        self.text.innerHTML = "404 NOT FOUND"
        self.element.appendChild(self.text)