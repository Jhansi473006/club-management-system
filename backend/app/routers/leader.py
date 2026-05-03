from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.dependencies import require_role
from app.utils.storage import upload_file_to_supabase

router = APIRouter(
    prefix="/leader",
    tags=["Leader Features"],
    dependencies=[Depends(require_role(["leader"]))]
)

def get_leader_club(db: Session, leader_id: int):
    club = db.query(models.Club).filter(models.Club.leader_id == leader_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found for this leader")
    return club

@router.get("/my-club", response_model=schemas.ClubResponse)
def get_my_club(current_user: models.User = Depends(require_role(["leader"])), db: Session = Depends(get_db)):
    return get_leader_club(db, current_user.id)

@router.put("/club")
async def update_club_details(
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    instagram_link: Optional[str] = Form(None),
    logo: UploadFile = File(None),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    
    if name:
        club.name = name
    if description:
        club.description = description
    if contact_email is not None:
        club.contact_email = contact_email
    if instagram_link is not None:
        club.instagram_link = instagram_link
        
    if logo:
        logo_url = await upload_file_to_supabase(logo, bucket_name="club-media")
        if logo_url:
            club.logo_url = logo_url
            
    db.commit()
    db.refresh(club)
    return {"message": "Club updated successfully", "club_url": club.logo_url}

@router.get("/coordinators", response_model=List[schemas.CoordinatorResponse])
def get_club_coordinators(
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    return db.query(models.Coordinator).filter(models.Coordinator.club_id == club.id).order_by(models.Coordinator.id.desc()).all()

@router.post("/coordinators", response_model=schemas.CoordinatorResponse)
async def add_coordinator(
    role_type: str = Form(...),
    status: str = Form("approved"),
    faculty_name: Optional[str] = Form(None),
    faculty_email: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    photo: UploadFile = File(None),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    
    photo_url = None
    if photo:
        photo_url = await upload_file_to_supabase(photo, bucket_name="club-media")
        
    new_coord = models.Coordinator(
        club_id=club.id,
        role_type=role_type,
        status=status,
        faculty_name=faculty_name,
        faculty_email=faculty_email,
        user_id=user_id,
        photo_url=photo_url
    )
    db.add(new_coord)
    db.commit()
    db.refresh(new_coord)
    return new_coord

@router.put("/coordinators/{coord_id}", response_model=schemas.CoordinatorResponse)
async def update_coordinator(
    coord_id: int,
    role_type: Optional[str] = Form(None),
    faculty_name: Optional[str] = Form(None),
    faculty_email: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    status: Optional[str] = Form(None),
    photo: UploadFile = File(None),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    coord = db.query(models.Coordinator).filter(models.Coordinator.id == coord_id, models.Coordinator.club_id == club.id).first()
    if not coord:
        raise HTTPException(status_code=404, detail="Coordinator not found")
        
    if role_type: coord.role_type = role_type
    if faculty_name is not None: coord.faculty_name = faculty_name
    if faculty_email is not None: coord.faculty_email = faculty_email
    if user_id is not None: coord.user_id = user_id
    if status is not None: coord.status = status
    
    if photo:
        photo_url = await upload_file_to_supabase(photo, bucket_name="club-media")
        if photo_url:
            coord.photo_url = photo_url
            
    db.commit()
    db.refresh(coord)
    return coord

@router.delete("/coordinators/{coord_id}")
def delete_coordinator(
    coord_id: int,
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    coord = db.query(models.Coordinator).filter(models.Coordinator.id == coord_id, models.Coordinator.club_id == club.id).first()
    if not coord:
        raise HTTPException(status_code=404, detail="Coordinator not found")
        
    db.delete(coord)
    db.commit()
    return {"message": "Coordinator deleted"}

@router.post("/events", response_model=schemas.EventResponse)
async def create_club_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    instructions: Optional[str] = Form(None),
    helpline: Optional[str] = Form(None),
    registration_deadline: Optional[str] = Form(None),
    registration_link: Optional[str] = Form(None),
    image: UploadFile = File(None),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    
    image_url = None
    if image:
        image_url = await upload_file_to_supabase(image, bucket_name="events-media")
        
    new_event = models.Event(
        club_id=club.id,
        title=title,
        description=description,
        date=date,
        location=location,
        instructions=instructions,
        helpline=helpline,
        registration_deadline=registration_deadline,
        registration_link=registration_link,
        image_url=image_url,
        is_college_level=False
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/events", response_model=List[schemas.EventResponse])
def get_club_events(
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    events = db.query(models.Event).filter(models.Event.club_id == club.id).order_by(models.Event.date.desc()).all()
    return events

@router.put("/events/{event_id}", response_model=schemas.EventResponse)
async def update_club_event(
    event_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    instructions: Optional[str] = Form(None),
    helpline: Optional[str] = Form(None),
    registration_deadline: Optional[str] = Form(None),
    registration_link: Optional[str] = Form(None),
    image: UploadFile = File(None),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.club_id == club.id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    if title: event.title = title
    if description: event.description = description
    if date: event.date = date
    if location: event.location = location
    if instructions is not None: event.instructions = instructions
    if helpline is not None: event.helpline = helpline
    if registration_deadline is not None: event.registration_deadline = registration_deadline
    if registration_link is not None: event.registration_link = registration_link
    
    if image:
        image_url = await upload_file_to_supabase(image, bucket_name="events-media")
        if image_url:
            event.image_url = image_url
            
    db.commit()
    db.refresh(event)
    return event

@router.delete("/events/{event_id}")
def delete_club_event(
    event_id: int,
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.club_id == club.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}

@router.post("/events/{event_id}/photos")
async def upload_event_photos(
    event_id: int,
    photos: List[UploadFile] = File(...),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.club_id == club.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    uploaded_urls = []
    for photo in photos:
        url = await upload_file_to_supabase(photo, bucket_name="events-media")
        if url:
            new_photo = models.EventPhoto(event_id=event.id, photo_url=url)
            db.add(new_photo)
            uploaded_urls.append(url)
    
    db.commit()
    return {"message": f"Uploaded {len(uploaded_urls)} photos", "urls": uploaded_urls}

@router.post("/announcements", response_model=schemas.AnnouncementResponse)
async def create_club_announcement(
    title: str = Form(...),
    content: str = Form(...),
    registration_link: Optional[str] = Form(None),
    deadline: Optional[str] = Form(None),
    image: UploadFile = File(None),
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    
    poster_url = None
    if image:
        poster_url = await upload_file_to_supabase(image, bucket_name="announcements-media")
    
    new_announcement = models.Announcement(
        club_id=club.id,
        title=title,
        content=content,
        poster_url=poster_url,
        registration_link=registration_link,
        deadline=deadline,
        is_college_level=False
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

@router.put("/registrations/{registration_id}")
def update_registration_status(
    registration_id: int, 
    status_update: str = Form(...), 
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    
    registration = db.query(models.EventRegistration).filter(models.EventRegistration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
        
    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    if event.club_id != club.id:
        raise HTTPException(status_code=403, detail="Event does not belong to your club")
        
    if status_update not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    registration.status = status_update
    db.commit()
    db.refresh(registration)
    return {"message": "Status updated", "status": registration.status}

@router.get("/events/{event_id}/registrations")
def get_event_registrations(
    event_id: int,
    current_user: models.User = Depends(require_role(["leader"])),
    db: Session = Depends(get_db)
):
    club = get_leader_club(db, current_user.id)
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.club_id == club.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
        
    regs = db.query(models.EventRegistration, models.User).join(
        models.User, models.EventRegistration.user_id == models.User.id
    ).filter(models.EventRegistration.event_id == event_id).all()
    
    results = []
    for reg, user in regs:
        results.append({
            "registration_id": reg.id,
            "user_name": user.name,
            "user_email": user.email,
            "type": reg.registration_type,
            "status": reg.status,
            "created_at": reg.created_at
        })
    return results
