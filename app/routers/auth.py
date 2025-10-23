from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.hashing import verify_password
from app.core.security import create_token
from app.models.user import User
from app.schemas.auth import TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=TokenPair)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_token(str(user.id), minutes=60)
    return TokenPair(access_token=access)
