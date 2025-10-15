from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions import DownloadError
from routes import youtube, tiktok

app = FastAPI()


@app.exception_handler(DownloadError)
async def download_error_handler(request: Request, exc: DownloadError):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    print(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


app.include_router(youtube.router)
app.include_router(tiktok.router)
