from fastapi_restful.api_model import APIModel
from pydantic import Field

from zatrol.model.region import Region
from zatrol.settings import Settings


class ErrorDTO(APIModel):
    """Generic error response"""

    detail: str = Field(description="User friendly error message")


class QuoteDTO(APIModel):
    id: int = None
    puuid: str
    text: str = Field(
        min_length=Settings.const.MIN_QUOTE_LEN,
        max_length=Settings.const.MAX_QUOTE_LEN,
    )
    champ_restrictions: list[str] = []


class SummonerDTO(APIModel):
    puuid: str = None
    region: Region
    summoner_name: str
    last_match: str = None
