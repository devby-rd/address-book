from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.utils import calculate_distance

from .database import engine, get_db
from . import models, schema, crud

# Create app instance
app = FastAPI(title="Address Book API")

# Create database tables
models.Base.metadata.create_all(bind=engine)


@app.post("/addresses/", response_model=schema.AddressResponse)
def create_address(address: schema.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db=db, address=address)


@app.get("/addresses/{address_id}", response_model=schema.AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.get_address(db=db, address_id=address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/addresses/", response_model=List[schema.AddressResponse])
def get_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db=db, skip=skip, limit=limit)
    return addresses


@app.put("/addresses/{address_id}", response_model=schema.AddressResponse)
def update_address(address_id: int, address: schema.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db=db, address_id=address_id, address=address)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.delete("/addresses/{address_id}", response_model=schema.AddressResponse)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.delete_address(db=db, address_id=address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.get("/addresses/nearby/", response_model=List[schema.AddressResponse])
def get_nearby_addresses(latitude: float = Query(..., ge=-90, le=90), longitude: float = Query(..., ge=-180, le=180), radius: float = Query(..., gt=0, description="Search radius in kilometers (km)"), db: Session = Depends(get_db)):
    addresses = crud.get_addresses(db=db)
    nearby_addresses = []
    for address in addresses:
        distance = calculate_distance(latitude, longitude, address.latitude, address.longitude)
        if distance <= radius:
            nearby_addresses.append(address)
    return nearby_addresses
