from fastapi import FastAPI
from .database import engine
from . import models

# Create app instance
app = FastAPI(title="Address Book API")

# Create database tables
models.Base.metadata.create_all(bind=engine)
