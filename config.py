import os

from dotenv import load_dotenv

load_dotenv('.env')

FFMPEG_PATH = os.getenv("FFMPEG_PATH")
DB_DSN = os.getenv("DB_DSN")
