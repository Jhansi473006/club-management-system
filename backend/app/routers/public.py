from sqlalchemy.orm import Session, joinedload
import json
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/public",
    tags=["Public APIs (Homepage)"]
)

@router.get("/system-logo")
def get_system_logo():
    config_path = os.path.join(os.path.dirname(__file__), "../../data_config.json")
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return {"logo_url": config.get("college_logo")}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"logo_url": None}

@router.get("/clubs-slideshow", response_model=List[schemas.ClubResponse])
def get_clubs_slideshow(db: Session = Depends(get_db)):
    # Returns all clubs with their basic details
    clubs = db.query(models.Club).all()
    # In a full production app, you might aggregate coordinator details here,
    # but the frontend can also fetch them specifically or we can add them to a complex response model.
    return clubs

@router.get("/events-slideshow", response_model=List[schemas.EventResponse])
def get_events_slideshow(db: Session = Depends(get_db)):
    # Returns events with images for the highlights slideshow
    events = db.query(models.Event).filter(models.Event.image_url != None).order_by(models.Event.date.desc()).limit(10).all()
    return events

@router.get("/event/{event_id}")
def get_event_details(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).options(joinedload(models.Event.photos)).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    coordinators = []
    club_info = None
    
    if event.club_id:
        club = db.query(models.Club).filter(models.Club.id == event.club_id).first()
        if club:
            club_info = {
                "id": club.id,
                "name": club.name,
                "logo_url": club.logo_url
            }
            # Fetch coordinators for the club
            coords_query = db.query(models.Coordinator).filter(
                models.Coordinator.club_id == club.id, 
                models.Coordinator.status == "approved"
            ).all()
            for c in coords_query:
                name = c.faculty_name
                email = c.faculty_email
                if c.user_id:
                    user = db.query(models.User).filter(models.User.id == c.user_id).first()
                    if user:
                        name = user.name
                        email = user.email
                if name:
                    coordinators.append({
                        "id": c.id,
                        "name": name,
                        "email": email,
                        "role_type": c.role_type,
                        "photo_url": c.photo_url
                    })

    volunteers_query = db.query(models.EventRegistration, models.User).join(
        models.User, models.EventRegistration.user_id == models.User.id
    ).filter(
        models.EventRegistration.event_id == event_id,
        models.EventRegistration.registration_type == "volunteer",
        models.EventRegistration.status == "approved"
    ).all()
    
    event_volunteers = []
    for reg, user in volunteers_query:
        event_volunteers.append({
            "id": user.id,
            "name": user.name,
            "role_type": "Event Volunteer",
            "photo_url": user.profile_photo_url
        })

    return jsonable_encoder({
        "event": event,
        "club": club_info,
        "coordinators": coordinators,
        "volunteers": event_volunteers
    })

@router.get("/club/{club_id}")
def get_club_details(club_id: int, db: Session = Depends(get_db)):
    club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    
    events = db.query(models.Event).filter(models.Event.club_id == club_id).all()
    announcements = db.query(models.Announcement).filter(models.Announcement.club_id == club_id).all()
    
    coordinators_query = db.query(models.Coordinator).filter(models.Coordinator.club_id == club_id, models.Coordinator.status == "approved").all()
    coordinators = []
    for c in coordinators_query:
        name = c.faculty_name
        email = c.faculty_email
        if c.user_id:
            user = db.query(models.User).filter(models.User.id == c.user_id).first()
            if user:
                name = user.name
                email = user.email
        if name:
            coordinators.append({
                "id": c.id,
                "name": name,
                "email": email,
                "role_type": c.role_type,
                "photo_url": c.photo_url
            })

    return {
        "club": club,
        "events": events,
        "announcements": announcements,
        "coordinators": coordinators
    }

@router.get("/announcements")
def get_all_announcements(db: Session = Depends(get_db)):
    # Fetch all announcements, newest first
    announcements = db.query(models.Announcement).order_by(models.Announcement.created_at.desc()).all()
    
    result = []
    for ann in announcements:
        club_name = "College Level"
        if ann.club_id:
            club = db.query(models.Club).filter(models.Club.id == ann.club_id).first()
            if club:
                club_name = club.name
                
        result.append({
            "id": ann.id,
            "title": ann.title,
            "content": ann.content,
            "poster_url": ann.poster_url,
            "club_name": club_name,
            "created_at": ann.created_at,
            "deadline": ann.deadline,
            "registration_link": ann.registration_link
        })
        
    return result

@router.get("/announcement/{announcement_id}")
def get_single_announcement(announcement_id: int, db: Session = Depends(get_db)):
    ann = db.query(models.Announcement).filter(models.Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
        
    club_name = "College Level"
    if ann.club_id:
        club = db.query(models.Club).filter(models.Club.id == ann.club_id).first()
        if club:
            club_name = club.name
            
    return {
        "id": ann.id,
        "title": ann.title,
        "content": ann.content,
        "poster_url": ann.poster_url,
        "club_name": club_name,
        "created_at": ann.created_at,
        "deadline": ann.deadline,
        "registration_link": ann.registration_link,
        "is_college_level": ann.is_college_level
    }
