"""Service schemas"""
from typing import Optional
from datetime import date
from pydantic import BaseModel


class AddEventCalendarSchema(BaseModel):
    """New event calendar"""

    user_id: int
    date: date
    title: str


class EventCalendarSerializer(BaseModel):
    """Event calendar serializer"""

    id: int
    user_id: int
    date: str
    title: str


class HolidaysSerializer(BaseModel):
    """Holiday calendar serializer"""

    id: int
    date: str
    name: str
    type: str
    level: str
    law: Optional[str] = None
