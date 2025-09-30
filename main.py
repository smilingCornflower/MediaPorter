from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from starlette.responses import PlainTextResponse

from database import log_download
from services import Services, clean_youtube_url

app = FastAPI(title="Media Porter")


@app.get("/mp3/download")
def download_mp3(url: str = Query(..., description="YouTube URL")):
    try:
        cleaned_url = clean_youtube_url(url)
        print(f"{cleaned_url = }")
        mp3_bytes = Services.youtube_downloader.download_mp3(url=cleaned_url)

        log_download(url=cleaned_url, fmt='mp3')

        return StreamingResponse(
            content=mp3_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'attachment; filename="download.mp3"'}
        )
    except Exception as e:
        print(f"Exception in download_mp3() - {e}")
        return PlainTextResponse(content="Internal server exception", status_code=500)


@app.get("/mp4/download")
def download_mp4(url: str = Query(..., description="YouTube URL")):
    try:
        cleaned_url = clean_youtube_url(url)
        print(f"{cleaned_url = }")
        mp4_bytes = Services.youtube_downloader.download_mp4(url=cleaned_url)

        log_download(url=cleaned_url, fmt='mp4')

        return StreamingResponse(
            content=mp4_bytes,
            media_type="video/mp4",
            headers={"Content-Disposition": 'attachment; filename="download.mp4"'}
        )
    except Exception as e:
        print(f"Exception in download_mp4() - {e}")
        return PlainTextResponse(content="Internal server exception", status_code=500)
