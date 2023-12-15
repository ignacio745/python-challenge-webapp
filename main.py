from fastapi import FastAPI, Depends, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import uvicorn

from database.database import get_db, Base, engine
from routers.auth import auth_router
from routers.bookings import booking_router
from routers.users import user_router
from security.oauth2 import get_current_user_from_cookie
from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="static/html")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(booking_router)

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user_from_cookie(request, db)
    except Exception:
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)