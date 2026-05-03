from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
# Import all models to ensure they are registered with SQLAlchemy
from app import models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="College Club Management System API",
    description="Backend API for managing college clubs, events, and registrations.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, registration, admin, leader, student, public, user
app.include_router(auth.router)
app.include_router(registration.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(leader.router)
app.include_router(student.router)
app.include_router(public.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the College Club Management System API"}

import os
from fastapi.staticfiles import StaticFiles
os.makedirs("uploads", exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory="uploads"), name="uploads")
