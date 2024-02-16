import client.components.abs as abs

if __name__ == "__main__":
    location_path = js.window.location.pathname

    Navbar("app").drawWidget()

    content = Layout("app")
    if location_path == "/":
        content.drawWidget([Home("content")])
    elif location_path == "/login":
        content.drawWidget([Login("content")])
    else:
        content.drawWidget([NotFound("content")])
