# monolith/tekovia_app/app.py
import reflex as rx
from pages.eventos import eventos

app = rx.App()
app.add_page(eventos, route="/")