from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.requests import Request
from core.config import settings
from database import database
from models.user import User as DBUser
from schemas.token import TokenData
from typing import Optional, Dict
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from .hash_password import verify_hash
from crud.user_crud import get_user_by_email
from database.database import get_db


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True
    ):
        if not scopes:
            scopes = {}
            flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})

        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(settings.cookie_name)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            else:
                return None
        return param
    
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def authenticate_user(db: Session, useremail: str, plain_password: str):
    user = get_user_by_email(db, useremail)
    if not user:
        return False
    if not verify_hash(plain_password, user.hashed_password):
        return False
    return user


def decode_token(token: str, db: Session) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        useremail: str = payload.get("username")
        if useremail is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    user = get_user_by_email(db, useremail)
    return user


def get_current_user_from_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> DBUser:
    user = decode_token(token, db)
    return user


def get_current_user_from_cookie(request: Request, db: Session) -> DBUser:
    token = request.cookies.get(settings.cookie_name)
    user = decode_token(token, db)
    return user