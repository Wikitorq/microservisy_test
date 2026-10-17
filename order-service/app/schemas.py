from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    event_id: int = Field(..., gt=0, example=1)
    quantity: int = Field(..., ge=1, example=2)

class OrderResponse(BaseModel):
    id: int
    event_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        from_attributes = True