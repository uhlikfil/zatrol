from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse

from zatrol.settings import Settings

router = APIRouter(tags=["ui"], default_response_class=HTMLResponse)


@router.route("/")
@router.route("/generate")
@router.route("/quote")
@router.route("/summoner")
def serve(_):
    return FileResponse(Settings.path.UI_BUILD / "index.html")
