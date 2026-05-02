from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_google_token, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class GoogleLoginRequest(BaseModel):
    token: str

@router.post("/google")
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    # 1. Verify Google Token
    idinfo = verify_google_token(request.token)
    if not idinfo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    
    email = idinfo.get("email")
    name = idinfo.get("name")
    google_id = idinfo.get("sub")
    picture = idinfo.get("picture")

    # 2. Get or Create User
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            name=name,
            google_id=google_id,
            profile_picture=picture
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update name or picture if changed
        user.name = name
        user.profile_picture = picture
        db.commit()
        db.refresh(user)

    # 3. Create Backend JWT
    access_token = create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name,
            "picture": user.profile_picture
        }
    }
