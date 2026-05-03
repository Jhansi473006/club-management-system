from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app import models, schemas
from app.dependencies import require_role

router = APIRouter(
    prefix="/student",
    tags=["Student Module"],
    dependencies=[Depends(require_role(["student"]))] # Also could allow all users to fetch clubs, but requested separate modules
)

@router.get("/clubs", response_model=List[schemas.ClubResponse])
def get_all_clubs(db: Session = Depends(get_db)):
    clubs = db.query(models.Club).all()
    return clubs

@router.get("/clubs/{club_id}")
def get_club_details(club_id: int, db: Session = Depends(get_db)):
    club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
        
    coordinators = db.query(models.Coordinator).filter(models.Coordinator.club_id == club_id).all()
    events = db.query(models.Event).filter(models.Event.club_id == club_id).all()
    announcements = db.query(models.Announcement).filter(models.Announcement.club_id == club_id).order_by(models.Announcement.created_at.desc()).all()
    
    return {
        "club": club,
        "coordinators": coordinators,
        "events": events,
        "announcements": announcements
    }

@router.get("/events")
def get_all_events(upcoming: bool = True, db: Session = Depends(get_db)):
    now = datetime.now()
    if upcoming:
        events = db.query(models.Event).filter(models.Event.date >= now).order_by(models.Event.date.asc()).all()
    else:
        events = db.query(models.Event).filter(models.Event.date < now).order_by(models.Event.date.desc()).all()
    return events

@router.post("/events/{event_id}/register")
def register_for_event(
    event_id: int, 
    registration_type: str, # "participant" or "volunteer"
    current_user: models.User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    if registration_type not in ["participant", "volunteer"]:
        raise HTTPException(status_code=400, detail="Invalid registration type")
        
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    existing_reg = db.query(models.EventRegistration).filter(
        models.EventRegistration.event_id == event_id,
        models.EventRegistration.user_id == current_user.id
    ).first()
    
    if existing_reg:
        raise HTTPException(status_code=400, detail="You have already registered for this event")
        
    new_reg = models.EventRegistration(
        event_id=event_id,
        user_id=current_user.id,
        registration_type=registration_type,
        status="pending"
    )
    db.add(new_reg)
    db.commit()
    return {"message": "Registered successfully", "status": new_reg.status}

@router.post("/clubs/{club_id}/apply-coordinator")
def apply_coordinator(
    club_id: int, 
    current_user: models.User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
        
    existing_app = db.query(models.Coordinator).filter(
        models.Coordinator.club_id == club_id,
        models.Coordinator.user_id == current_user.id
    ).first()
    
    if existing_app:
        raise HTTPException(status_code=400, detail="Already applied or a coordinator")
        
    new_coord = models.Coordinator(
        club_id=club.id,
        user_id=current_user.id,
        role_type="student",
        status="pending"
    )
    db.add(new_coord)
    db.commit()
    return {"message": "Coordinator application submitted successfully"}

@router.get("/my-registrations")
def get_my_registrations(current_user: models.User = Depends(require_role(["student"])), db: Session = Depends(get_db)):
    registrations = db.query(models.EventRegistration).filter(models.EventRegistration.user_id == current_user.id).all()
    # To return nicely, we merge event details
    result = []
    for reg in registrations:
        event = db.query(models.Event).filter(models.Event.id == reg.event_id).first()
        result.append({
            "registration_id": reg.id,
            "event_id": reg.event_id,
            "status": reg.status,
            "type": reg.registration_type,
            "event_title": event.title if event else "Unknown",
            "event_date": event.date if event else None
        })
    return result
