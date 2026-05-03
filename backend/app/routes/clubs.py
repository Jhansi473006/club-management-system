from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
from app.database import get_db
from app.models import Club, MembershipRequest, Member, CoordinatorApplication
from app.services import club_service
from app.utils.security import decode_access_token

router = APIRouter()


# ✅ Get all clubs
@router.get("/clubs")
def get_clubs(db: Session = Depends(get_db)):
    return db.query(Club).all()


# ✅ Get club by leader id
@router.get("/clubs/leader/{leader_id}")
def get_club_by_leader(leader_id: int, db: Session = Depends(get_db)):
    club = db.query(Club).filter(Club.leader_id == leader_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return {"club_id": club.club_id, "name": club.club_name, "description": club.description}


# ✅ Save club
@router.post("/save_club")
def save_club(
    club_id: int = Form(...),
    club_name: str = Form(...),
    description: str = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(decode_access_token)
):
    if current_user["role"] != "leader":
        raise HTTPException(status_code=403, detail="Not authorized")

    club = db.query(Club).filter(Club.club_id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    if logo:
        path = f"app/static/images/{logo.filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(logo.file, f)

    club.club_name = club_name
    club.description = description

    db.commit()
    return {"message": "Saved"}


# ✅ Send join request
@router.post("/clubs/request")
def join_request(club_id: int, student_id: int, db: Session = Depends(get_db)):

    result = club_service.send_join_request(db, club_id, student_id)

    if result == "already_member":
        raise HTTPException(status_code=400, detail="Already a member")

    if result == "request_exists":
        raise HTTPException(status_code=400, detail="Request already sent")

    return {"message": "Join request sent"}


# ✅ Get ALL membership requests (for leader dashboard)
@router.get("/clubs/requests")
def get_requests(db: Session = Depends(get_db)):
    return db.query(MembershipRequest).all()


# ✅ Approve request
@router.post("/clubs/approve/{request_id}")
def approve_request(request_id: int, db: Session = Depends(get_db)):

    request = db.query(MembershipRequest).filter_by(request_id=request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    member = Member(club_id=request.club_id, student_id=request.student_id)

    db.add(member)
    db.delete(request)
    db.commit()

    return {"message": "Approved"}


# ✅ Reject request
@router.post("/clubs/reject/{request_id}")
def reject_request(request_id: int, db: Session = Depends(get_db)):

    request = db.query(MembershipRequest).filter_by(request_id=request_id).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    db.delete(request)
    db.commit()

    return {"message": "Rejected"}


# ✅ Get members of a club
@router.get("/clubs/{club_id}/members")
def get_members(club_id: int, db: Session = Depends(get_db)):
    return db.query(Member).filter(Member.club_id == club_id).all()


# =========================
# 🔥 COORDINATOR SYSTEM
# =========================


# ✅ Get coordinator requests
@router.get("/clubs/coordinator/requests")
def get_coord_requests(db: Session = Depends(get_db)):
    return db.query(CoordinatorApplication).all()


# ✅ Approve coordinator
@router.post("/clubs/coordinator/approve/{id}")
def approve_coord(id: int, db: Session = Depends(get_db)):

    app = db.query(CoordinatorApplication).filter_by(application_id=id).first()

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.status = "approved"
    db.commit()

    return {"message": "Coordinator Approved"}
