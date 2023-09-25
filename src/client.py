"""Service client"""
from datetime import datetime
import requests
from requests.exceptions import Timeout
from fastapi.exceptions import HTTPException
from src.config import HOLIDAYS_URL


class HolidaysClient:
    """Consumer holiday service"""

    def get_holidays(self, year: int = datetime.now().year, state: str = None) -> dict:
        """Get holidays from Holidays service"""
        try:
            params = {
                "year": year,
            }

            if state:
                params.update({"state": state})

            reponse = requests.get(
                url=f"{HOLIDAYS_URL}holidays/", params=params, timeout=2
            )
            if reponse.status_code != 200:
                raise HTTPException(
                    status_code=reponse.status_code, detail=reponse.json()
                )

            return reponse.json()
        except Timeout:
            return []
