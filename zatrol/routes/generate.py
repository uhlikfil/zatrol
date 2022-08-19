from fastapi import Depends, status
from fastapi.responses import StreamingResponse
from fastapi_restful import cbv
from fastapi_restful.inferring_router import InferringRouter

from zatrol.model.api_schema import ErrorDTO
from zatrol.services.generate import GenerateSvc

router = InferringRouter(
    prefix="/api/generate",
    tags=["generate"],
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorDTO}},
)


@cbv.cbv(router)
class GenerateView:
    svc: GenerateSvc = Depends()

    @router.get("/{puuid}", response_class=StreamingResponse)
    async def get(self, puuid: str, quote_id: int = None, game_id: int = None):
        img = await self.svc.generate(puuid, quote_id, game_id)
        return StreamingResponse(img, media_type="image/png")
