# routes/tiktok.py
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from services import Services

router = APIRouter(prefix="/tiktok", tags=["TikTok"])


@router.get("/mp3/download")
def download_mp3(url: str = Query(..., description="TikTok URL")):
    mp3_bytes = Services.tiktok_downloader.download_mp3(url=url)

    return StreamingResponse(
        content=mp3_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'attachment; filename="download.mp3"'}
    )


@router.get("/mp4/download")
def download_mp4(url: str = Query(..., description="TikTok URL")):
    mp4_bytes = Services.tiktok_downloader.download_mp4(url=url)

    return StreamingResponse(
        content=mp4_bytes,
        media_type="video/mp4",
        headers={"Content-Disposition": 'attachment; filename="download.mp4"'}
    )