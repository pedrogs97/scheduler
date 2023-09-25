"""Service use cases"""
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import extract
from src.models import HolidaysCalendarModel, UserEventCalendarModel
from src.client import HolidaysClient
from src.schemas import (
    AddEventCalendarSchema,
    EventCalendarSerializer,
    HolidaysSerializer,
)


class CalendarService:
    """Calendar service use cases"""

    def __init__(self, db_session: Session, year: int, state: str = None) -> None:
        self.db_session = db_session
        self.holiday_serivce = HolidaysClient()
        holidays = self.holiday_serivce.get_holidays(year, state)

        if (
            not self.db_session.query(HolidaysCalendarModel)
            .where(extract("year", HolidaysCalendarModel.date) == year)
            .first()
        ):
            for holiday in holidays:
                new_holiday = HolidaysCalendarModel(
                    date=datetime.strptime(holiday["date"], "%Y-%m-%d").date(),
                    name=holiday["name"],
                    type=holiday["type"],
                    level=holiday["level"],
                    law=holiday["law"] if "law" in holiday else None,
                )
                self.db_session.add(new_holiday)
                self.db_session.commit()

    def serialize_event(self, event: UserEventCalendarModel) -> EventCalendarSerializer:
        """Serialize user event calendar"""
        return EventCalendarSerializer(
            id=event.id,
            date=event.date.isoformat(),
            title=event.title,
            user_id=event.user_id,
        )

    def serialize_holiday(self, holiday: HolidaysCalendarModel) -> HolidaysSerializer:
        "Serialize holiday calendar"
        return HolidaysSerializer(
            id=holiday.id,
            date=holiday.date.isoformat(),
            name=holiday.name,
            type=holiday.type,
            level=holiday.level,
            law=holiday.law,
        )

    def get_user_month_calendar(
        self, user_id: int, month: int, year: int
    ) -> List[dict]:
        """Returns user month calendar"""
        event_calendar = (
            self.db_session.query(UserEventCalendarModel)
            .filter(
                UserEventCalendarModel.user_id == user_id,
                extract("year", UserEventCalendarModel.date) == year,
                extract("month", UserEventCalendarModel.date) == month,
            )
            .all()
        )

        holidays_calendar = (
            self.db_session.query(HolidaysCalendarModel)
            .filter(
                extract("year", HolidaysCalendarModel.date) == year,
                extract("month", HolidaysCalendarModel.date) == month,
            )
            .all()
        )

        calendar = [
            self.serialize_event(event).model_dump() for event in event_calendar
        ]
        calendar.extend(
            [
                self.serialize_holiday(holiday).model_dump()
                for holiday in holidays_calendar
            ]
        )
        return calendar

    def get_user_year_calendar(self, user_id: int, year: int) -> List[dict]:
        """Returns user year calendar"""
        event_calendar = (
            self.db_session.query(UserEventCalendarModel)
            .filter(
                UserEventCalendarModel.user_id == user_id,
                extract("year", UserEventCalendarModel.date) == year,
            )
            .all()
        )

        holidays_calendar = (
            self.db_session.query(HolidaysCalendarModel)
            .filter(extract("year", HolidaysCalendarModel.date) == year)
            .all()
        )

        calendar = [
            self.serialize_event(event).model_dump() for event in event_calendar
        ]
        calendar.extend(
            [
                self.serialize_holiday(holiday).model_dump()
                for holiday in holidays_calendar
            ]
        )
        return calendar

    def add_user_event_calendar(
        self, data: AddEventCalendarSchema
    ) -> EventCalendarSerializer:
        """Add new event in user calendar"""
        new_event = UserEventCalendarModel(**data.model_dump())

        self.db_session.add(new_event)
        self.db_session.commit()
        self.db_session.flush()
        return self.serialize_event(new_event)
