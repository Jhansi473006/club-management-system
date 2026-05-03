from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Club
from app.schemas import UserRegister, LeaderRegister, UserLogin
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter()
@router.post("/register/student")
def register_student(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="student",
    )

    db.add(new_user)
    db.commit()

    return {"message": "Student registered successfully"}
@router.post("/register/leader")
def register_leader(data: LeaderRegister, db: Session = Depends(get_db)):

    # Check if user email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already exists")

    # Hash the password and create a new leader user
    leader = User(
        name=data.name, 
        email=data.email, 
        password=hash_password(data.password), 
        role="leader"
    )

    db.add(leader)
    db.commit()
    db.refresh(leader)

    # Create the associated club for the leader
    club = Club(
        club_name=data.club_name, description=data.description, leader_id=leader.user_id
    )

    db.add(club)
    db.commit()

    return {"message": "Leader registered successfully"}
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.user_id), "role": db_user.role})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.user_id,
        "role": db_user.role,
    }