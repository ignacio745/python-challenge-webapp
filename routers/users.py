from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import User as User, UserCreate, UserSignIn
from database.database import get_db
from crud import user_crud


user_router = APIRouter(prefix="/user", tags=["Users"])



@user_router.get("/", response_model=User)
def read_user(user: UserSignIn, db: Session = Depends(get_db)):
    dbuser = user_crud.get_user_by_email(db=db, user=user)
    if not dbuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password"
        )
    return dbuser


@user_router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db=db, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return db_user
