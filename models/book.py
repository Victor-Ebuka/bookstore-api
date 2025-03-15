from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    
    # Relationship to the User model
    uploader = relationship("User", back_populates="books")
