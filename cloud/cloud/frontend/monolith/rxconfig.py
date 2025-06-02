import reflex as rx
import os

config = rx.Config(
    app_name="tekovia_app",
    # 👉 URL global que usa todo el modelo interno
    api_url=os.getenv("BACKEND_URL", "http://localhost:8000"),
    db_url=os.getenv(
        "DB_URL",
        "postgresql+psycopg2://postgres:admin@localhost:5432/TekoviaGuasu"
    ),
    tailwind=None,
)