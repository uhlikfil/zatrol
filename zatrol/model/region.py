from enum import Enum


class Region(Enum):
    EUNE = "eun1"
    EUW = "euw1"
    JAP = "jp1"
    KR = "kr"
    LA1 = "la1"
    LA2 = "la2"
    NA = "na1"
    OC = "oc1"
    TR = "tr1"
    RU = "ru"


def parse_region(region: str):
    try:
        return Region[region]
    except KeyError:
        raise ValueError(f"Invalid region value '{region}', select one of {[r.name for r in Region]}")  # fmt: skip
