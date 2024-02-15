from __init__ import *

class Login(AbstractWidget):
    def __init__(self, element_id):
        AbstractWidget.__init__(self, element_id)

    def drawWidget(self):
        self.login = document.createElement("div")
        self.login.className = "flex flex-col w-screen p-4 gap-4 text-center text-xl"
        self.login_title = document.createElement("p")
        self.login_title.innerHTML = "Login"
        self.login_title.className = "text-center text-2xl font-semibold font-varela font-medium break-words my-8"
        self.login.appendChild(self.login_title)

        # box
        self.box = document.createElement("div")
        self.box.className = "flex flex-col gap-4"
        # box username
        self.username_box = document.createElement("div")
        self.username_box.className = ""
        self.username_header = document.createElement("p")
        self.username_header.className = "text-center text-2xl font-semibold font-varela font-medium break-words my-8"
        self.username_header.innerHTML = "username"
        self.username_input = document.createElement("input")
        self.username_input.className = (
            "w-96 h-14 relative rounded-lg border border-gray-300 px-5"
        )
        # box password
        self.password_box = document.createElement("div")
        self.password_box.classname = ""
        self.password_header = document.createElement("p")
        self.password_header.className = "text-center text-2xl font-semibold font-varela font-medium break-words my-8"
        self.password_header.innerHTML = "password"
        self.password_input = document.createElement("input")
        self.password_input.className = (
            "w-96 h-14 relative rounded-lg border border-gray-300 px-5"
        )
        # box button
        self.button_box = document.createElement("div")
        self.button_box.className = ""
        self.button_login = document.createElement("button")
        self.button_login.className = "w-96 h-16 bg-orange-500 shadow-md rounded-full text-white text-lg font-varela font-medium my-8"
        self.button_login.innerHTML = "Login"
        # box question
        self.question_box = document.createElement("div")
        self.question_box.className = ""
        self.question_text = document.createElement("p")
        self.question_text.className = "text-center"
        self.question_text.innerHTML = "Don't have an account?"

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

