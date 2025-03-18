from uuid import UUID
from fastapi import HTTPException
from crud.auth import hash_password
from models.user import User
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserUpdate, UserUpdatePassword

def create_user(user_data: UserCreate, db: Session) -> User:
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=new_password, role=user_data.role, first_name=user_data.first_name, last_name=user_data.last_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(current_user: User, db: Session) -> list[User]:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(User).all()

def get_user_by_id(current_user: User, user_id: UUID, db: Session) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_a_user_profile(current_user: User) -> User:
    return current_user

def update_user_profile(current_user: User, user_data: UserUpdate, db: Session) -> User:
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

def update_user_password(current_user: User, user_data: UserUpdatePassword, db: Session) -> User:
    new_hashed_password = hash_password(user_data.password)
    current_user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(current_user)
    return current_user

def delete_a_user(current_user: User, user_id: UUID, db: Session) -> bool:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    user = get_user_by_id(current_user, user_id, db)
    db.delete(user)
    db.commit()
    return True

def delete_a_user_profile(current_user: User, db: Session) -> bool:
    db.delete(current_user)
    db.commit()
    return True