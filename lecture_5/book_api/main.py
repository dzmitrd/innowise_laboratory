from typing import Optional

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Database setup (SQLite + SQLAlchemy) ---

DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# --- ORM Model ---

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)


# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)


# --- FastAPI app ---

app = FastAPI()


# 1) POST /books/  -> add a new book
@app.post("/books/")
def add_book(title: str, author: str, year: int):
    db = SessionLocal()
    try:
        new_book = Book(title=title, author=author, year=year)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return {"id": new_book.id, "title": new_book.title, "author": new_book.author, "year": new_book.year}
    finally:
        db.close()


# 2) GET /books/ -> get all books
@app.get("/books/")
def get_books():
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        return [{"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books]
    finally:
        db.close()


# 3) DELETE /books/{book_id} -> delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        db.delete(book)
        db.commit()
        return {"message": "Book deleted"}
    finally:
        db.close()


# 4) PUT /books/{book_id} -> update a book
@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
):
    db = SessionLocal()
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if year is not None:
            book.year = year

        db.commit()
        db.refresh(book)
        return {"id": book.id, "title": book.title, "author": book.author, "year": book.year}
    finally:
        db.close()


# 5) GET /books/search/ -> search by title/author/year
@app.get("/books/search/")
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
):
    db = SessionLocal()
    try:
        query = db.query(Book)

        if title is not None:
            query = query.filter(Book.title.contains(title))
        if author is not None:
            query = query.filter(Book.author.contains(author))
        if year is not None:
            query = query.filter(Book.year == year)

        books = query.all()
        return [{"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books]
    finally:
        db.close()
