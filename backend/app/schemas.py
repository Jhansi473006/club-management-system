from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str # "admin", "leader", "student"
    roll_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    profile_photo_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    roll_number: Optional[str] = None


# Login schema
class Login(BaseModel):
    email: EmailStr
    password: str

# Events schema
class EventCreate(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
    instructions: Optional[str] = None
    helpline: Optional[str] = None
    registration_deadline: Optional[datetime] = None
    registration_link: Optional[str] = None

class EventPhotoResponse(BaseModel):
    id: int
    photo_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class EventResponse(EventCreate):
    id: int
    club_id: Optional[int] = None
    image_url: Optional[str] = None
    is_college_level: bool
    photos: List[EventPhotoResponse] = []

    class Config:
        from_attributes = True

# Announcement schema
class AnnouncementCreate(BaseModel):
    title: str
    content: str
    registration_link: Optional[str] = None
    deadline: Optional[datetime] = None

class AnnouncementResponse(AnnouncementCreate):
    id: int
    club_id: Optional[int] = None
    poster_url: Optional[str] = None
    is_college_level: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Coordinator schema
class CoordinatorCreate(BaseModel):
    role_type: str  # "faculty" or "student"
    status: str = "approved"
    faculty_name: Optional[str] = None
    faculty_email: Optional[str] = None
    user_id: Optional[int] = None

class CoordinatorResponse(CoordinatorCreate):
    id: int
    club_id: int
    photo_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Club Update schema
class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ClubResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    instagram_link: Optional[str] = None
    leader_id: int
    created_at: datetime

    class Config:
        from_attributes = True

