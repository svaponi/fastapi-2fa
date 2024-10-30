from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from app.core.hashing import Hasher
from app.core.otp import OTP
from app.database.models.users import User
from app.database.repository.users import get_user_by_email
from app.database.session import get_db
from app.webapps.login.forms import LoginForm

router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return request.app.templates.TemplateResponse("login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user: User = get_user_by_email(form.email, db=db)
            if (
                user is None
                or not Hasher.verify_password(form.password, user.hashed_password)
                or not OTP.verify_otp(user.secret, form.token)
            ):
                form.__dict__.get("errors").append("Incorrect Credentails")
                return request.app.templates.TemplateResponse(
                    "login.html", form.__dict__
                )

            return request.app.templates.TemplateResponse(
                "index.html", {"request": request, "email": user.email}
            )
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return request.app.templates.TemplateResponse("login.html", form.__dict__)
    return request.app.templates.TemplateResponse("login.html", form.__dict__)
