from app.models import MembershipRequest, Member, CoordinatorApplication


def send_join_request(db, club_id: int, student_id: int):

    # Check if student is already a club member
    member = (
        db.query(Member)
        .filter(Member.club_id == club_id, Member.student_id == student_id)
        .first()
    )

    if member:
        return "already_member"

    # Check if student already sent join request
    existing_request = (
        db.query(MembershipRequest)
        .filter(
            MembershipRequest.club_id == club_id,
            MembershipRequest.student_id == student_id,
        )
        .first()
    )

    if existing_request:
        return "request_exists"

    # Create join request
    request = MembershipRequest(
        club_id=club_id,
        student_id=student_id,
        status="pending",
    )

    db.add(request)
    db.commit()

    return "success"


def apply_coordinator(db, club_id: int, student_id: int):

    # Check if student already a member
    member = (
        db.query(Member)
        .filter(Member.club_id == club_id, Member.student_id == student_id)
        .first()
    )

    if member:
        return "already_member"

    # Check if student already applied
    existing = (
        db.query(CoordinatorApplication)
        .filter(
            CoordinatorApplication.club_id == club_id,
            CoordinatorApplication.student_id == student_id,
        )
        .first()
    )

    if existing:
        return "already_applied"

    # Create coordinator application
    application = CoordinatorApplication(
        club_id=club_id,
        student_id=student_id,
        status="pending",
    )

    db.add(application)
    db.commit()

    return "success"