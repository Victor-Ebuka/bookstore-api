from fastapi import APIRouter, Depends
from crud.auth import login_a_user
from database.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return login_a_user(email, password, db)