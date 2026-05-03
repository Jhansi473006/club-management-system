from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from pydantic import BaseModel
from app.utils.security import verify_password, create_access_token

class VerifyRequest(BaseModel):
    email: str
    code: str

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.Login, db: Session = Depends(get_db)):
    email = user_credentials.email.lower().strip()
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
        
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
        
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified. Please verify your email first."
        )
        
    # Create token
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-email")
def verify_email(payload: VerifyRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    if user.verification_code != payload.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    user.is_verified = True
    user.verification_code = None  # Clear the code after successful verification
    db.commit()

    return {"message": "Email verified successfully. You can now log in."}
