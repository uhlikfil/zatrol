from fastapi import BackgroundTasks, Depends, status
from fastapi_restful.inferring_router import InferringRouter

from zatrol.database.dao.game import GameDAO
from zatrol.database.dao.summoner import SummonerDAO
from zatrol.model.api_schema import ErrorDTO, SummonerDTO
from zatrol.services import match_history
from zatrol.services.summoner import SummonerSvc

router = InferringRouter(prefix="/summoner", tags=["summoner"])


@router.get("", responses={status.HTTP_404_NOT_FOUND: {"model": ErrorDTO}})
async def get(svc: SummonerSvc = Depends()) -> list[SummonerDTO]:
    return await svc.get_all()


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def post(
    summoner: SummonerDTO,
    tasks: BackgroundTasks,
    summoner_dao: SummonerDAO = Depends(),
    game_dao: GameDAO = Depends(),
):
    svc = SummonerSvc(summoner_dao)
    puuid = await svc.insert_summoner(summoner.region, summoner.summoner_name)
    tasks.add_task(
        match_history.process_summoner,
        summoner_dao,
        game_dao,
        await summoner_dao.get(puuid),
    )
