from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.users import UserCreate, UserResponseDetailed, UserResponse, UserUpdatePassword, UserUpdate
from crud.users import create_user, get_a_user_profile, update_user_password, delete_a_user_profile, get_all_users, get_user_by_id, update_user_profile, delete_a_user
from crud.auth import get_current_user
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"], 
)

@router.post("/", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)

@router.get("/profile", response_model=UserResponseDetailed)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return get_a_user_profile(current_user)

@router.put("/profile", response_model=UserResponse)
def update_profile(user_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user_profile(current_user, user_data, db)

@router.put("/profile/password", response_model=UserResponseDetailed)
def update_password(user_data: UserUpdatePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_user_password(current_user, user_data, db)

@router.delete("/profile")
def delete_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if delete_a_user_profile(current_user, db):
        return "Profile deleted successfully"

@router.delete("/{user_id}")
def delete_user(user_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if delete_a_user(current_user, user_id, db):
        return "User deleted successfully"

@router.get("/", response_model=list[UserResponse])
def read_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_all_users(current_user, db)

@router.get("/{user_id}", response_model=UserResponseDetailed)
def read_user_by_id(user_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_by_id(current_user, user_id, db)