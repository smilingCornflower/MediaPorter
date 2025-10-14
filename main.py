from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from starlette.responses import PlainTextResponse
from database import log_download
from services import Services, clean_youtube_url

app = FastAPI(title="Media Porter")


@app.get("/download/youtube/mp3")
def download_youtube_mp3(url: str = Query(..., description="YouTube video URL")):
    try:
        cleaned_url = clean_youtube_url(url)
        print(f"{cleaned_url = }")

        mp3_bytes = Services.youtube_downloader.download_mp3(url=cleaned_url)
        log_download(url=cleaned_url, fmt="youtube-mp3")

        return StreamingResponse(
            content=mp3_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'attachment; filename="youtube_audio.mp3"'}
        )
    except Exception as e:
        print(f"Exception in download_youtube_mp3() - {e}")
        return PlainTextResponse(content="Internal server exception", status_code=500)


@app.get("/download/youtube/mp4")
def download_youtube_mp4(url: str = Query(..., description="YouTube video URL")):
    try:
        cleaned_url = clean_youtube_url(url)
        print(f"{cleaned_url = }")

        mp4_bytes = Services.youtube_downloader.download_mp4(url=cleaned_url)
        log_download(url=cleaned_url, fmt="youtube-mp4")

        return StreamingResponse(
            content=mp4_bytes,
            media_type="video/mp4",
            headers={"Content-Disposition": 'attachment; filename="youtube_video.mp4"'}
        )
    except Exception as e:
        print(f"Exception in download_youtube_mp4() - {e}")
        return PlainTextResponse(content="Internal server exception", status_code=500)


@app.get("/download/instagram/mp4")
def download_instagram_mp4(url: str = Query(..., description="Instagram video URL")):
    try:
        print(f"{url = }")

        mp4_bytes = Services.youtube_downloader.download_instagram(url=url)
        log_download(url=url, fmt="instagram-mp4")

        return StreamingResponse(
            content=mp4_bytes,
            media_type="video/mp4",
            headers={"Content-Disposition": 'attachment; filename="instagram_video.mp4"'}
        )
    except Exception as e:
        print(f"Exception in download_instagram_mp4() - {e}")
        return PlainTextResponse(content="Internal server exception", status_code=500)


@app.get("/download/instagram/mp3")
def download_instagram_mp3(url: str = Query(..., description="Instagram video URL")):
    try:
        print(f"{url = }")

        mp3_bytes = Services.youtube_downloader.download_instagram_mp3(url=url)
        log_download(url=url, fmt="instagram-mp3")

        return StreamingResponse(
            content=mp3_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'attachment; filename="instagram_audio.mp3"'}
        )
    except Exception as e:
        print(f"Exception in download_instagram_mp3() - {e}")
        return PlainTextResponse(content="Internal server exception", status_code=500)
