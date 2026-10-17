import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="1.0.0")

# URL of our running Catalog Service
CATALOG_SERVICE_URL = "http://localhost:8000/events"

@app.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    
    # --- STEP 1: Talk to the Catalog Service via HTTP ---
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CATALOG_SERVICE_URL}/{order.event_id}")
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Catalog Service is currently unreachable."
            )

    # --- STEP 2: Handle response status ---
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Event not found in Catalog.")
    elif response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error communicating with Catalog Service.")

    event_data = response.json()

    # --- STEP 3: Validate ticket availability ---
    if event_data["available_tickets"] < order.quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough tickets available. Only {event_data['available_tickets']} left."
        )

    # --- STEP 4: Calculate totals and save order ---
    total_price = event_data["price"] * order.quantity

    db_order = models.OrderModel(
        event_id=order.event_id,
        quantity=order.quantity,
        total_price=total_price,
        status="CONFIRMED"
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order

@app.get("/orders", response_model=list[schemas.OrderResponse])
def list_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.OrderModel).offset(skip).limit(limit).all()