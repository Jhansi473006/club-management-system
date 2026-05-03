from app.models import Event, EventRegistration


def create_event(db, club_id, title, description, date, location):

    event = Event(
        club_id=club_id,
        title=title,
        description=description,
        date=date,
        location=location,
    )

    db.add(event)
    db.commit()

    return event
def register_event(db, event_id, student_id, type):

    existing = (
        db.query(EventRegistration)
        .filter(
            EventRegistration.event_id == event_id,
            EventRegistration.student_id == student_id,
        )
        .first()
    )

    if existing:
        return "already_registered"

    registration = EventRegistration(
        event_id=event_id, student_id=student_id, type=type
    )

    db.add(registration)
    db.commit()

    return "success"