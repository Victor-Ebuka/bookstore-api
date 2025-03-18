from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from schemas.books import BookResponse
from schemas.users import UserResponse

# Base schema for books
class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    stock: int

# Schema for creating a new book
class BookCreate(BookBase):
    pass

# Schema for updating book details
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    stock: Optional[int] = None

# Basic response schema for books
class BookResponse(BookBase):
    id: UUID
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True

# Detailed response schema with uploader details
class BookResponseDetailed(BookResponse):
    uploader: UserResponse
