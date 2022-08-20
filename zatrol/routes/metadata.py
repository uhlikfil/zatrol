from fastapi import status
from fastapi_restful.inferring_router import InferringRouter

from zatrol.model.region import Region
from zatrol.services import champion as champion_svc

router = InferringRouter(prefix="/metadata", tags=["metadata"])


@router.get("/region", status_code=status.HTTP_200_OK)
def get_region() -> list[str]:
    return [reg.value for reg in Region]


@router.get("/champion", status_code=status.HTTP_200_OK)
def get_champion() -> list[str]:
    return champion_svc.get_champions()
