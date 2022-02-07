from enum import Enum


class Region(Enum):
    EUNE = "eun1"
    EUW = "euw1"
    TR = "tr1"
    RU = "ru"
    NA = "na1"
    BR = "br1"
    LAN = "la1"
    LAS = "la2"
    OCE = "oc1"
    KR = "kr"
    JP = "jp1"

    @staticmethod
    def parse(region: str) -> "Region":
        try:
            return Region[region]
        except KeyError:
            raise ValueError(f"Invalid region value '{region}', select one of {[r.name for r in Region]}")  # fmt: skip


class RegionArea(Enum):
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"

    @staticmethod
    def get_area(region: Region) -> "RegionArea":
        return _region_map.get(region)


_region_map = {
    Region.EUNE: RegionArea.EUROPE,
    Region.EUW: RegionArea.EUROPE,
    Region.TR: RegionArea.EUROPE,
    Region.RU: RegionArea.EUROPE,
    Region.NA: RegionArea.AMERICAS,
    Region.BR: RegionArea.AMERICAS,
    Region.LAN: RegionArea.AMERICAS,
    Region.LAS: RegionArea.AMERICAS,
    Region.OCE: RegionArea.AMERICAS,
    Region.KR: RegionArea.ASIA,
    Region.JP: RegionArea.ASIA,
}
