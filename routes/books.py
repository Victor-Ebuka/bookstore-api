from uuid import UUID
from fastapi import APIRouter, Depends
from crud.books import get_books, get_a_book_by_id, get_books_by_title, get_books_by_author, get_books_by_genre, create_book, get_book_details, update_book, delete_a_book
from database.session import get_db
from sqlalchemy.orm import Session
from schemas.books import BookCreate, BookUpdate, BookResponseDetailed, BookResponse

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.get("/", response_model=list[BookResponse])
def read_books(db: Session = Depends(get_db)):
    return get_books(db)

@router.get("/{book_id}", response_model=BookResponseDetailed)
def read_book_by_id(book_id: UUID, db: Session = Depends(get_db)):
    return get_a_book_by_id(book_id, db)

@router.get("/title/{title}", response_model=list[BookResponse])
def read_books_by_title(title: str, db: Session = Depends(get_db)):
    return get_books_by_title(title, db)

@router.get("/author/{author}", response_model=list[BookResponse])  
def read_books_by_author(author: str, db: Session = Depends(get_db)):
    return get_books_by_author(author, db)

@router.get("/genre/{genre}", response_model=list[BookResponse])    
def read_books_by_genre(genre: str, db: Session = Depends(get_db)):
    return get_books_by_genre(genre, db)

@router.post("/", response_model=BookResponse)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    return create_book(book_data, db)

@router.get("/{book_id}/details", response_model=BookResponseDetailed)
def read_book_details(book_id: UUID, db: Session = Depends(get_db)):
    return get_book_details(book_id, db)

@router.put("/{book_id}", response_model=BookResponse)
def update_book_info(book_id: UUID, book_data: BookUpdate, db: Session = Depends(get_db)):
    return update_book(book_id, book_data, db)

@router.delete("/{book_id}")
def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    if delete_a_book(book_id, db):
        return "Book deleted successfully"
    
