from config import FFMPEG_PATH
from downloaders import YoutubeDownloader, TiktokDownloader


class Services:
    youtube_downloader = YoutubeDownloader(ffmpeg_path=FFMPEG_PATH)
    tiktok_downloader = TiktokDownloader(ffmpeg_path=FFMPEG_PATH)
