from __init__ import *

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
