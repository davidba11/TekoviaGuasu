from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, select, create_engine
from pydantic import BaseModel

# ---------------- configuración BD ----------------
import os

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:admin@db:5432/tekovia"
)
engine = create_engine(DB_URL, echo=False)

# ---------------- modelos -------------------------
class Event(SQLModel, table=True):
    id: int | None = None                       # autoincremento
    titulo: str
    fecha: str
    ciudad: str
    categoria: str

SQLModel.metadata.create_all(engine)

# ---------------- API -----------------------------
app = FastAPI(title="Tekovia Guasu API")


class EventIn(BaseModel):
    titulo: str
    fecha: str
    ciudad: str
    categoria: str


@app.get("/events", response_model=list[Event])
def list_events() -> list[Event]:
    with Session(engine) as db:
        return db.exec(select(Event)).all()


@app.post("/events", response_model=Event, status_code=201)
def add_event(evt: EventIn):
    with Session(engine) as db:
        new = Event.model_validate(evt)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
