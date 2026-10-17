from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), index=True, nullable=False)        # Added length (255)
    description = Column(String(500), nullable=True)               # Added length (500)
    price = Column(Float, nullable=False)
    available_tickets = Column(Integer, nullable=False)