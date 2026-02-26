from sqlalchemy.orm import Session
from . import models, schemas


def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


def delete_address(db: Session, address_id: int):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address


def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        for key, value in address.model_dump(exclude_unset=True).items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address
