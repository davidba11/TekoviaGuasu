import reflex as rx
import os

config = rx.Config(
    app_name="tekovia_app",
    api_url="http://0.0.0.0:8000",
    db_url=os.getenv("DB_URL", "postgresql+psycopg2://postgres:admin@db:5432/tekovia"),
    backend_host="0.0.0.0",
)