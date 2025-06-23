# controllers/event_state.py
import reflex as rx
from sqlmodel import Session, select, create_engine
from models.event import Event
from os import getenv

class EventState(rx.State):
    # ── datos en memoria ────────────────────────────────────────────────
    _all_rows: list[dict] = []
    events: list[dict] = []
    form_data: dict = {"titulo": "", "fecha": "", "ciudad": "", "categoria": ""}
    edit_id: int | None = None
    show_modal: bool = False
    delete_id: int | None = None
    delete_title: str = ""

    # ── paginación ──────────────────────────────────────────────────────
    offset: int = 0
    limit: int = 6
    total_items: int = 0

    def get_engine(self):
        return create_engine(
            getenv("DB_URL", "postgresql+psycopg2://postgres:admin@db:5432/tekovia")
        )

    def create_tables(self):
        try:
            engine = self.get_engine()
            Event.metadata.create_all(engine)
        except Exception as e:
            print(f"[ERROR al crear tablas]: {e}")

    @rx.var
    def current_page(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var
    def num_total_pages(self) -> int:
        return max((self.total_items + self.limit - 1) // self.limit, 1)

    @rx.event
    def next_page(self):
        if self.offset + self.limit < self.total_items:
            self.offset += self.limit
            yield self.refresh_page()

    @rx.event
    def prev_page(self):
        if self.offset > 0:
            self.offset -= self.limit
            yield self.refresh_page()

    @rx.event
    def refresh_page(self):
        self.events = self._all_rows[self.offset : self.offset + self.limit]
        self.set()

    @rx.event
    async def load(self):
        self.create_tables()
        engine = self.get_engine()
        with Session(engine) as session:
            result = session.exec(select(Event).order_by(Event.fecha)).all()
            self._all_rows = [e.dict() for e in result]
        self.total_items = len(self._all_rows)
        self.offset = 0
        yield self.refresh_page()

    @rx.event
    def process_form(self, form: dict):
        if not all(form.values()):
            return rx.toast("Completa todos los campos")

        engine = self.get_engine()
        if self.edit_id is not None:
            original = next((e for e in self._all_rows if e["id"] == self.edit_id), None)
            if original and form == {
                "titulo": original["titulo"],
                "fecha": original["fecha"],
                "ciudad": original["ciudad"],
                "categoria": original["categoria"],
            }:
                return rx.toast("No se encuentran cambios para modificar")

            with Session(engine) as session:
                event = session.get(Event, self.edit_id)
                if event:
                    for k, v in form.items():
                        setattr(event, k, v)
                    session.add(event)
                    session.commit()
            self.edit_id = None
        else:
            with Session(engine) as session:
                nuevo = Event(**form)
                session.add(nuevo)
                session.commit()

        return type(self).load()

    @rx.event
    def edit_event(self, id: int):
        event = next((e for e in self._all_rows if e["id"] == id), None)
        if event:
            self.form_data = {
                "titulo": event["titulo"],
                "fecha": event["fecha"],
                "ciudad": event["ciudad"],
                "categoria": event["categoria"],
            }
            self.edit_id = id
            self.set()

    @rx.event
    def clear_form(self):
        self.form_data = {"titulo": "", "fecha": "", "ciudad": "", "categoria": ""}
        self.edit_id = None
        self.set()

    @rx.event
    def show_delete_modal(self, id: int, titulo: str):
        self.delete_id = id
        self.delete_title = titulo
        self.show_modal = True
        self.set()

    @rx.event
    def hide_modal(self):
        self.show_modal = False
        self.delete_id = None
        self.delete_title = ""
        self.set()

    @rx.event
    def confirm_delete(self):
        if self.delete_id is not None:
            engine = self.get_engine()
            with Session(engine) as session:
                event = session.get(Event, self.delete_id)
                if event:
                    session.delete(event)
                    session.commit()
        self.delete_id = None
        self.delete_title = ""
        self.show_modal = False
        return type(self).load()

    @rx.event
    def set_form_field(self, field: str, value: str):
        self.form_data[field] = value
        self.set()
