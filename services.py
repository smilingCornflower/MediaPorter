import io
import os
import tempfile
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import yt_dlp

from config import FFMPEG_PATH


def clean_youtube_url(url: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "v" in qs:
        new_query = urlencode({"v": qs["v"][0]})
        return str(urlunparse(parsed._replace(query=new_query)))
    return url


class YoutubeDownloader:
    def __init__(self, ffmpeg_path: str | None = None):
        self.ffmpeg_path = ffmpeg_path

    def _get_opts(self, fmt_opts: dict) -> dict:
        opts = {
            "quiet": True,
            "noprogress": False,
            "noplaylist": True,
            "retries": 10,
            "fragment_retries": 10,
            "ignoreerrors": True,
            **fmt_opts,
        }
        if self.ffmpeg_path:
            opts["ffmpeg_location"] = self.ffmpeg_path
        return opts

    def download_mp3(self, url: str) -> io.BytesIO:
        with tempfile.TemporaryDirectory() as tmpdir:
            fmt_opts = {
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
            opts = self._get_opts(fmt_opts)

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"

            with open(filepath, "rb") as f:
                data = io.BytesIO(f.read())
                data.seek(0)
                return data

    def download_mp4(self, url: str) -> io.BytesIO:
        with tempfile.TemporaryDirectory() as tmpdir:
            fmt_opts = {
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
            }
            opts = self._get_opts(fmt_opts)

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)

            with open(filepath, "rb") as f:
                data = io.BytesIO(f.read())
                data.seek(0)
                return data
            
    def download_instagram(self, url: str) -> io.BytesIO:
        with tempfile.TemporaryDirectory() as tmpdir:
            fmt_opts = {
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "format": "best[ext=mp4]/best",
                "merge_output_format": "mp4",
                "quiet": True,
                "noplaylist": False,
            }
            opts = self._get_opts(fmt_opts)

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)

            with open(filepath, "rb") as f:
                data = io.BytesIO(f.read())
                data.seek(0)
                return data



class Services:
    youtube_downloader = YoutubeDownloader(ffmpeg_path=FFMPEG_PATH)
