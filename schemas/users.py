from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Annotated, List, Literal, Optional
from datetime import datetime

# Base schema for user
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal["admin", "user"] = "user"

# Schema for creating a new user
class UserCreate(UserBase):
    password: str  # Password required when creating a user

# Schema for updating user information (excluding role changes for security)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Literal["admin", "user"]] = None

# Schema for updating user password
class UserUpdatePassword(BaseModel):
    password: str

# Basic response schema for user (excluding password)
class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True

# Detailed response schema with uploaded books
class UserResponseDetailed(UserResponse):
    books: Annotated[List["BookResponse"], ...] = []   # Prevent circular imports using string annotation

    @staticmethod
    def resolve_forward_refs():
        global BookResponse
        from schemas.books import BookResponse
        UserResponseDetailed.model_rebuild()

UserResponseDetailed.resolve_forward_refs()