from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel
import os

DB = os.getenv(
    "DB_URL",
    "postgresql+asyncpg://book:book@db:5432/books"
)
engine = create_engine(DB, echo=False)

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    autor: str
    anio: int

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/books")
def list_books():
    with Session(engine) as s:
        return s.exec(select(Book)).all()

class BookIn(BaseModel):
    titulo: str
    autor: str
    anio: int

@app.post("/books", status_code=201)
def add_book(b: BookIn):
    with Session(engine) as s:
        book = Book.model_validate(b)
        s.add(book)
        s.commit()
        s.refresh(book)
        return book
