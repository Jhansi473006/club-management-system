from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "admin", "leader", "student"
    roll_number = Column(String, nullable=True)  # Student/Leader specific
    profile_photo_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    clubs = relationship("Club", back_populates="leader")
    registrations = relationship("EventRegistration", back_populates="user")
    coordinator_roles = relationship("Coordinator", back_populates="user")


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    instagram_link = Column(String, nullable=True)
    
    leader_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    leader = relationship("User", back_populates="clubs")
    events = relationship("Event", back_populates="club")
    announcements = relationship("Announcement", back_populates="club")
    coordinators = relationship("Coordinator", back_populates="club")


class Coordinator(Base):
    __tablename__ = "coordinators"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Null if external faculty not tied to a user account
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    
    faculty_name = Column(String, nullable=True)  # Useful if faculty are not registered users
    faculty_email = Column(String, nullable=True)
    
    role_type = Column(String, nullable=False) # "faculty" or "student"
    status = Column(String, default="pending")
    photo_url = Column(String, nullable=True) # "pending", "approved", "rejected"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="coordinator_roles")
    club = relationship("Club", back_populates="coordinators")


class EventPhoto(Base):
    __tablename__ = "event_photos"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    event = relationship("Event", back_populates="photos")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True) # Null if college-level
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    is_college_level = Column(Boolean, default=False)
    instructions = Column(Text, nullable=True)
    helpline = Column(String, nullable=True)
    registration_deadline = Column(DateTime(timezone=True), nullable=True)
    registration_link = Column(String, nullable=True) # External link if needed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    club = relationship("Club", back_populates="events")
    registrations = relationship("EventRegistration", back_populates="event")
    photos = relationship("EventPhoto", back_populates="event", cascade="all, delete-orphan")


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    poster_url = Column(String, nullable=True)
    is_college_level = Column(Boolean, default=False)
    registration_link = Column(String, nullable=True) # For specific requirement forms
    deadline = Column(DateTime(timezone=True), nullable=True) # For countdown
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    club = relationship("Club", back_populates="announcements")


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registration_type = Column(String, nullable=False) # "participant" or "volunteer"
    status = Column(String, default="pending") # "pending", "approved", "rejected"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")