from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.utils.security import get_password_hash
from app.utils.storage import upload_file_to_supabase

router = APIRouter(
    prefix="/user",
    tags=["User Profile"]
)

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
async def update_profile(
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    roll_number: Optional[str] = Form(None),
    profile_photo: UploadFile = File(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if name:
        current_user.name = name
    if email:
        email = email.lower().strip()
        # Check uniqueness if email changed
        if email != current_user.email:
            existing_user = db.query(models.User).filter(models.User.email == email).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already in use")
            current_user.email = email
    if password:
        current_user.hashed_password = get_password_hash(password)
    if roll_number is not None:
        current_user.roll_number = roll_number
        
    if profile_photo:
        photo_url = await upload_file_to_supabase(profile_photo, bucket_name="user-media")
        if photo_url:
            current_user.profile_photo_url = photo_url
            
    db.commit()
    db.refresh(current_user)
    return current_user
