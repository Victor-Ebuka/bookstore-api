from uuid import UUID
from fastapi import HTTPException
from models.book import Book
from sqlalchemy.orm import Session
from schemas.books import BookCreate, BookUpdate, BookResponseDetailed, BookResponse


def create_book(book_data: BookCreate, db: Session) -> Book:
    new_book = Book(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_book_by_id(book_id: UUID, db: Session) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def update_book(book_id: UUID, book_data: BookUpdate, db: Session) -> Book:
    book = get_book_by_id(book_id, db)
    for key, value in book_data.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(book_id: UUID, db: Session) -> bool:
    book = get_book_by_id(book_id, db)
    db.delete(book)
    db.commit()
    return True

def get_all_books(db: Session) -> list[Book]:
    return db.query(Book).all()

def get_books_by_title(title: str, db: Session) -> list[Book]:
    return db.query(Book).filter(Book.title.contains(title)).all()

def get_books_by_author(author: str, db: Session) -> list[Book]:
    return db.query(Book).filter(Book.author.contains(author)).all()

def get_books_by_genre(genre: str, db: Session) -> list[Book]:
    return db.query(Book).filter(Book.genre.contains(genre)).all()

def get_book_details(book_id: UUID, db: Session) -> BookResponseDetailed:
    book = get_book_by_id(book_id, db)
    return BookResponseDetailed.model_validate(book, from_attributes=True)