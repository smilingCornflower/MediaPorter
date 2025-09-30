import os

from dotenv import load_dotenv

load_dotenv('.env')

FFMPEG_PATH = r"C:\Users\Smile\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin"
DB_DSN = os.getenv("DB_DSN")
