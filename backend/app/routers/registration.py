from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, schemas
from app.utils.security import get_password_hash
from app.utils.storage import upload_file_to_supabase
from app.utils.email import generate_otp, send_otp_email

router = APIRouter(
    prefix="/register",
    tags=["Registration"]
)

@router.post("/leader")
async def register_leader_and_club(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    roll_number: Optional[str] = Form(None),
    club_name: str = Form(...),
    club_description: str = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Normalize Email
    email = email.lower().strip()
    # Check if user email exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if club name exists
    existing_club = db.query(models.Club).filter(models.Club.name == club_name).first()
    if existing_club:
        raise HTTPException(status_code=400, detail="Club name already exists")

    # Upload Logo
    logo_url = None
    if logo:
        logo_url = await upload_file_to_supabase(logo)

    # Generate OTP
    otp = generate_otp()

    # Create Leader User
    new_user = models.User(
        name=name,
        email=email,
        hashed_password=get_password_hash(password),
        role="leader",
        roll_number=roll_number,
        verification_code=otp,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send OTP email
    send_otp_email(new_user.email, otp)

    # Create Club
    new_club = models.Club(
        name=club_name,
        description=club_description,
        logo_url=logo_url,
        leader_id=new_user.id
    )
    db.add(new_club)
    db.commit()
    db.refresh(new_club)

    return {
        "message": "Leader and Club created successfully",
        "user_id": new_user.id,
        "club_id": new_club.id,
        "club_logo_url": logo_url
    }

@router.post("/student", response_model=schemas.UserResponse)
def register_student(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_email = user.email.lower().strip()
    if user.role != "student":
        raise HTTPException(status_code=400, detail="Only 'student' role registration is allowed here")
        
    existing_user = db.query(models.User).filter(models.User.email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Generate OTP
    otp = generate_otp()

    new_user = models.User(
        name=user.name,
        email=user_email,
        hashed_password=get_password_hash(user.password),
        role="student",
        roll_number=user.roll_number,
        verification_code=otp,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send OTP email
    send_otp_email(new_user.email, otp)

    return new_user

@router.post("/admin", response_model=schemas.UserResponse)
def register_admin(user: schemas.UserCreate, secret_key: str, db: Session = Depends(get_db)):
    user_email = user.email.lower().strip()
    # Very basic protection or none for development
    if secret_key != "supersecretadmin":
        raise HTTPException(status_code=403, detail="Invalid secret key")
        
    existing_user = db.query(models.User).filter(models.User.email == user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Generate OTP
    otp = generate_otp()

    new_user = models.User(
        name=user.name,
        email=user_email,
        hashed_password=get_password_hash(user.password),
        role="admin",
        verification_code=otp,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send OTP email
    send_otp_email(new_user.email, otp)

    return new_user
