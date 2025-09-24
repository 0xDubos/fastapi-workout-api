from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import User, UserCreate

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/users/")
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")

    # Hash the password and create a new User object
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(username=user_data.username, hashed_password=hashed_password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Return the user's ID and username, but not the password
    return {"id": db_user.id, "username": db_user.username}

    