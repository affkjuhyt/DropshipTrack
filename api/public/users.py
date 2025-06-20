from fastapi import APIRouter, Depends, HTTPException, status

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.security import ALGORITHM, REFRESH_SECRET_KEY, Token, create_tokens, get_current_active_user, oauth2_scheme
from db.session import get_db
from schemas.users import UserResponse
from models.users import User

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get new access token using refresh token."""
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("token_type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user = db.query(User).filter(User.email == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return create_tokens(data={"sub": user.email, "user_id": str(user.uuid)})
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user (client should remove tokens)."""
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    print("current_user: ", current_user)
    return current_user
