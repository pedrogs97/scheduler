"""Main"""
from fastapi import FastAPI
from src.models import Base
from src.database import engine
from src.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
