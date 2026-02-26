from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# base model for address
class AddressBase(BaseModel):

    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr

    street: str
    city: str
    state: str
    zip_code: str
    country: str

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


# model for creating an address
class AddressCreate(AddressBase):
    pass


# model for updating an address
class AddressUpdate(AddressBase):
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


# model for response
class AddressResponse(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
