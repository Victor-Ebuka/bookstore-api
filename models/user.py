from sqlalchemy import Column, Integer, String
from database.session import Base
from sqlalchemy.orm import relationship
from enum import Enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("admin", "user", name="user_roles"), default="user")

    # Relationship to the Book model
    books = relationship("Book", back_populates="uploader")
