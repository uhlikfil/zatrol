from fastapi import Depends, status
from fastapi_restful import cbv
from fastapi_restful.inferring_router import InferringRouter

from zatrol.model.api_schema import ErrorDTO, QuoteDTO
from zatrol.services.quote import QuoteSvc

router = InferringRouter(
    prefix="/quote",
    tags=["quote"],
    responses={status.HTTP_404_NOT_FOUND: {"model": ErrorDTO}},
)


@cbv.cbv(router)
class QuoteView:
    svc: QuoteSvc = Depends()

    @router.get("/{puuid}")
    async def get(self, puuid: str) -> list[QuoteDTO]:
        return await self.svc.get_all(puuid)

    @router.post("/", status_code=status.HTTP_204_NO_CONTENT)
    async def post(self, quote: QuoteDTO):
        champs = quote.champ_restrictions or []
        await self.svc.insert_quote(quote.puuid, quote.text, champs)
