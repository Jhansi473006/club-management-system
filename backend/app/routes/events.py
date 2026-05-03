from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import Event, EventRegistration, VolunteerApplication
from app.utils.security import decode_access_token
from app.database import get_db

router = APIRouter()


# =========================
# 📦 Pydantic Schemas
# =========================


class EventCreate(BaseModel):
    club_id: int
    title: str
    description: str
    date: str
    location: str


class EventRegister(BaseModel):
    event_id: int
    student_id: int


# =========================
# 📥 GET ALL EVENTS
# =========================


@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


# =========================
# ➕ CREATE EVENT (LEADER)
# =========================


@router.post("/events/create")
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: dict = Depends(decode_access_token)):
    if current_user["role"] != "leader":
        raise HTTPException(status_code=403, detail="Not authorized")

    new_event = Event(
        club_id=event.club_id,
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        poster="uploads/default.jpg",  # default image
    )

    db.add(new_event)
    db.commit()

    return {"message": "Event created successfully"}


# =========================
# 📝 REGISTER FOR EVENT
# =========================


@router.post("/events/register")
def register_event(data: EventRegister, db: Session = Depends(get_db)):

    existing = (
        db.query(EventRegistration)
        .filter(
            EventRegistration.event_id == data.event_id,
            EventRegistration.student_id == data.student_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Already registered")

    registration = EventRegistration(event_id=data.event_id, student_id=data.student_id)

    db.add(registration)
    db.commit()

    return {"message": "Registered successfully"}


# =========================
# 🙋 APPLY FOR VOLUNTEER
# =========================


@router.post("/events/volunteer")
def apply_volunteer(data: EventRegister, db: Session = Depends(get_db)):

    existing = (
        db.query(VolunteerApplication)
        .filter(
            VolunteerApplication.event_id == data.event_id,
            VolunteerApplication.student_id == data.student_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    volunteer = VolunteerApplication(event_id=data.event_id, student_id=data.student_id)

    db.add(volunteer)
    db.commit()

    return {"message": "Applied as volunteer"}
