from sqlalchemy import Column, Enum, Integer, String
from database.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]), default=UserRole.user, nullable=False)

    # Relationship to the Book model
    books = relationship("Book", back_populates="uploader")
