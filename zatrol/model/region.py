from enum import Enum

from zatrol.exceptions import InvalidValue


class Region(Enum):
    eun1 = "EUNE"
    euw1 = "EUW"
    tr1 = "TR"
    ru = "RU"
    na1 = "NA"
    br1 = "BR"
    la1 = "LAN"
    la2 = "LAS"
    oc1 = "OCE"
    kr = "KR"
    jp1 = "JP"

    @staticmethod
    def parse(region: str) -> "Region":
        try:
            return Region[region]
        except KeyError:
            raise InvalidValue(f"Invalid region value {region}, select one of {[r.name for r in Region]}")  # fmt: skip


class RegionArea(Enum):
    AMERICAS = "americas"
    ASIA = "asia"
    EUROPE = "europe"

    @staticmethod
    def get_area(region: Region) -> "RegionArea":
        return _region_map.get(region)


_region_map = {
    Region.eun1: RegionArea.EUROPE,
    Region.euw1: RegionArea.EUROPE,
    Region.tr1: RegionArea.EUROPE,
    Region.ru: RegionArea.EUROPE,
    Region.na1: RegionArea.AMERICAS,
    Region.br1: RegionArea.AMERICAS,
    Region.la1: RegionArea.AMERICAS,
    Region.la2: RegionArea.AMERICAS,
    Region.oc1: RegionArea.AMERICAS,
    Region.kr: RegionArea.ASIA,
    Region.jp1: RegionArea.ASIA,
}
