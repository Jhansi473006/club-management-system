from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import json
import os
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.dependencies import require_role
from app.utils.storage import upload_file_to_supabase

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role(["admin"]))]
)

@router.post("/logo")
async def update_college_logo(logo: UploadFile = File(...)):
    # Uploading college logo to supabase and saving globally
    logo_url = await upload_file_to_supabase(logo, bucket_name="college-media")
    if logo_url:
        config_path = os.path.join(os.path.dirname(__file__), "../../data_config.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}
        config["college_logo"] = logo_url
        with open(config_path, "w") as f:
            json.dump(config, f)
            
    return {"message": "College logo updated successfully", "logo_url": logo_url}

@router.post("/events", response_model=schemas.EventResponse)
async def create_college_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),  # YYYY-MM-DD HH:MM:SS
    location: str = Form(...),
    instructions: Optional[str] = Form(None),
    helpline: Optional[str] = Form(None),
    registration_deadline: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    if image:
        image_url = await upload_file_to_supabase(image, bucket_name="events-media")
        
    new_event = models.Event(
        title=title,
        description=description,
        date=date,
        location=location,
        instructions=instructions,
        helpline=helpline,
        registration_deadline=registration_deadline,
        image_url=image_url,
        is_college_level=True,
        club_id=None
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/events", response_model=List[schemas.EventResponse])
def get_college_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).filter(models.Event.is_college_level == True).order_by(models.Event.date.desc()).all()
    return events

@router.put("/events/{event_id}", response_model=schemas.EventResponse)
async def update_college_event(
    event_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    instructions: Optional[str] = Form(None),
    helpline: Optional[str] = Form(None),
    registration_deadline: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.is_college_level == True).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    if title: event.title = title
    if description: event.description = description
    if date: event.date = date
    if location: event.location = location
    if instructions is not None: event.instructions = instructions
    if helpline is not None: event.helpline = helpline
    if registration_deadline is not None: event.registration_deadline = registration_deadline
    
    if image:
        image_url = await upload_file_to_supabase(image, bucket_name="events-media")
        if image_url:
            event.image_url = image_url
            
    db.commit()
    db.refresh(event)
    return event

@router.delete("/events/{event_id}")
def delete_college_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.is_college_level == True).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    db.delete(event)
    db.commit()
    return {"message": "College event deleted"}

@router.post("/announcements", response_model=schemas.AnnouncementResponse)
async def create_college_announcement(
    title: str = Form(...),
    content: str = Form(...),
    registration_link: Optional[str] = Form(None),
    deadline: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    poster_url = None
    if image:
        poster_url = await upload_file_to_supabase(image, bucket_name="announcements-media")
        
    new_announcement = models.Announcement(
        title=title,
        content=content,
        poster_url=poster_url,
        registration_link=registration_link,
        deadline=deadline,
        is_college_level=True,
        club_id=None
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

@router.put("/registrations/{registration_id}")
def update_registration_status(registration_id: int, status_update: str = Form(...), db: Session = Depends(get_db)):
    # For Admin to approve/reject college event participants/volunteers
    registration = db.query(models.EventRegistration).filter(models.EventRegistration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    if not event.is_college_level:
        raise HTTPException(status_code=403, detail="Not a college-level event")

    if status_update not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    registration.status = status_update
    db.commit()
    db.refresh(registration)
    return {"message": "Status updated", "status": registration.status}
