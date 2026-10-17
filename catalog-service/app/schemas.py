from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    title: str = Field(..., example="Taylor Swift Concert")
    description: str = Field(..., example="The Eras Tour live in stadium")
    price: float = Field(..., gt=0, example=99.99)
    available_tickets: int = Field(..., ge=1, example=500)

class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: float
    available_tickets: int

    class Config:
        from_attributes = True
        