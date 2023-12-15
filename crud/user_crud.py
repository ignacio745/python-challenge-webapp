from sqlalchemy.orm import Session
from models.user import User as DBUser
from schemas.user import UserCreate
from security.hash_password import create_hash, verify_hash


def get_user_by_email(db: Session, useremail: str):
    dbuser = db.query(DBUser).filter(DBUser.email == useremail).first()
    if not dbuser:
        return False
    return dbuser


def create_user(db: Session, user: UserCreate):
    user_exist = db.query(DBUser).filter(DBUser.email == user.email).first()
    if user_exist:
        return False
    hashed_password = create_hash(user.password)
    db_user = DBUser(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_hash(password, user.hashed_password):
        return False
    return user