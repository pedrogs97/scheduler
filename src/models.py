"""Service models"""
from sqlalchemy import Column, Integer, Date, String
from src.database import Base


class UserEventCalendarModel(Base):
    """User event calendar"""

    __tablename__ = "user_event_calendar"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, nullable=False)
    date = Column("date", Date, nullable=False)
    title = Column("title", String, nullable=False)


class HolidaysCalendarModel(Base):
    """Holidays calendar"""

    __tablename__ = "holidays_calendar"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    date = Column("date", Date, nullable=False)
    name = Column("name", String, nullable=False)
    type = Column("type", String, nullable=False)
    level = Column("level", String, nullable=False)
    law = Column("law", String, nullable=True, default="")
