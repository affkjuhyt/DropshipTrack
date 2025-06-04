from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import Token, create_tokens, get_current_active_user, verify_password
from db.session import get_db
from models.users import User
from schemas.users import UserLogin

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user and return access & refresh tokens."""
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return create_tokens(data={"sub": user.email, "user_id": str(user.uuid)})


@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_active_user)):
    """Verify token and return user information if valid."""
    return {
        "status": "success",
        "user": {
            "email": current_user.email,
            "uuid": str(current_user.uuid),
            "is_active": current_user.is_active
        }
    }
