from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

# Automatically create database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service", version="1.0.0")

@app.post("/events", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.EventModel(
        title=event.title,
        description=event.description,
        price=event.price,
        available_tickets=event.available_tickets
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events", response_model=list[schemas.EventResponse])
def list_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(models.EventModel).offset(skip).limit(limit).all()
    return events

@app.get("/events/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.EventModel).filter(models.EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event