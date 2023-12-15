from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from typing import Dict
from security.oauth2 import authenticate_user, create_access_token
from core.config import settings
from fastapi.templating import Jinja2Templates
from schemas.login import LoginForm
from fastapi.responses import HTMLResponse, RedirectResponse
from schemas.user import UserCreate
from crud import user_crud



auth_router = APIRouter(tags=["Authentication"])

templates = Jinja2Templates(directory="static/html")

@auth_router.post("token")
def login_for_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"username": user.email})
    response.set_cookie(
        key=settings.cookie_name,
        value=f"Bearer {access_token}",
        httponly=True
    )
    return {settings.cookie_name: access_token, "token_type": "bearer"}




@auth_router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("login.html", context)


@auth_router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
            login_for_access_token(response=response, db=db, form_data=form)
            form.__dict__.update(msg="Login Successful!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


@auth_router.get("/logout", response_class=HTMLResponse)
def logout_get():
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.cookie_name)
    return response


@auth_router.get("/signup", response_class=HTMLResponse)
def signup_get(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {
            "request": request
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.post("/signup", response_class=HTMLResponse)
def signup_post(
    request: Request, 
    user: UserCreate = Depends(UserCreate.as_form),
    db: Session = Depends(get_db)
    ):
    new_user = user_crud.create_user(db, user)
    if not new_user:
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "warning": "Email already registered!!!"
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    access_token = create_access_token(data={"username": user.email})
    response.set_cookie(
        key=settings.cookie_name,
        value=f"Bearer {access_token}",
        httponly=True
    )
    return response











# templates = Jinja2Templates(directory="public/html")

# auth_router = APIRouter(tags=["Authentication"])


# @auth_router.get('/login', response_class=HTMLResponse)
# def login_get(request: Request):
#     return templates.TemplateResponse("login.html", 
#                                       {
#                                           "request": request
#                                       })

# # @auth_router.post('/login')
# # def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# #     user = db.query(DBUser).filter(DBUser.email == user_credentials.username).first()
# #     if not user:
# #         raise HTTPException(
# #             status_code=status.HTTP_403_FORBIDDEN,
# #             detail="Invalid Credentials"
# #         )
# #     if not verify_hash(user_credentials.password, user.hashed_password):
# #         raise HTTPException(
# #             status_code=status.HTTP_403_FORBIDDEN,
# #             detail="Invalid Credentials"
# #         )
    

# #     access_token = oauth2.create_access_token(data= {"user_id": user.id})

# #     return {
# #         "access_token": access_token,
# #         "token_type": "bearer"
# #     }

# @auth_router.post('/login')
# def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    
#     user = db.query(DBUser).filter(DBUser.email == email).first()
#     if not user:
#         return templates.TemplateResponse("login.html",
#                                           {
#                                               "request": request
#                                           })
#     if not verify_hash(password, user.hashed_password):
#         return templates.TemplateResponse("login.html",
#                                           {
#                                               "request": request
#                                           })
#     access_token = oauth2.create_access_token(data={"user_id": user.id})
#     response = responses.RedirectResponse(
#         "/booking/",
#         status_code=status.HTTP_302_FOUND
#     )
#     response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#     return response