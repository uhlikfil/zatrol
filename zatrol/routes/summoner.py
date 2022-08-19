from fastapi import Depends, status
from fastapi_restful import cbv
from fastapi_restful.inferring_router import InferringRouter

from zatrol.model.api_schema import ErrorDTO, SummonerDTO
from zatrol.services.summoner import SummonerSvc

router = InferringRouter(
    prefix="/api/summoner",
    tags=["summoner"],
)


@cbv.cbv(router)
class SummonerView:
    svc: SummonerSvc = Depends()

    @router.get("/", responses={status.HTTP_404_NOT_FOUND: {"model": ErrorDTO}})
    async def get(self) -> list[SummonerDTO]:
        return await self.svc.get_all()

    @router.post("/", status_code=status.HTTP_204_NO_CONTENT)
    async def post(self, summoner: SummonerDTO):
        await self.svc.insert_summoner(summoner.region, summoner.summoner_name)
