"""Service router"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from src.database import get_db_session
from src.service import CalendarService
from src.schemas import AddEventCalendarSchema

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/user/", status_code=status.HTTP_200_OK)
async def get_user_scheduler_route(
    user_id: int,
    year: int,
    month: int = None,
    state: str = None,
    db_session: Session = Depends(get_db_session),
) -> Response:
    """User calendar route"""
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User unknow"
        )

    service = CalendarService(db_session, year, state)

    if month:
        return JSONResponse(
            content=service.get_user_month_calendar(user_id, month, year),
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content=service.get_user_year_calendar(user_id, year),
        status_code=status.HTTP_200_OK,
    )


@router.post("/user/", status_code=status.HTTP_200_OK)
async def post_user_scheduler_route(
    data: AddEventCalendarSchema, db_session: Session = Depends(get_db_session)
) -> Response:
    """Add new event in user calendar route"""

    service = CalendarService(db_session, data.date.year)
    serializer = service.add_user_event_calendar(data)
    return JSONResponse(
        serializer.model_dump(),
        status_code=status.HTTP_200_OK,
    )
