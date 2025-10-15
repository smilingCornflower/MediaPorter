import io
import os
import tempfile
from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import yt_dlp

from database import log_download
from enums import PlatformEnum, FormatEnum
from exceptions import InvalidURLError, FileSizeError, VideoNotFoundError


class BaseDownloader(ABC):
    MAX_MP3_SIZE = 100 * 1024 * 1024  # 100 MB
    MAX_MP4_SIZE = 500 * 1024 * 1024  # 500 MB

    def __init__(self, ffmpeg_path: str | None = None):
        self.ffmpeg_path = ffmpeg_path

    def sanitize_url(self, url: str) -> str:
        url = url.strip()
        parsed = urlparse(url)

        if parsed.scheme not in ('http', 'https'):
            raise InvalidURLError("Only HTTP/HTTPS URLs are allowed")

        if not parsed.netloc:
            raise InvalidURLError("Invalid URL: missing domain")

        return url

    @abstractmethod
    def clean_url(self, url: str) -> str:
        pass

    @abstractmethod
    def get_platform_name(self) -> str:
        pass

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

    def _check_filesize_before_download(self, url: str, max_size: int, format: str):
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            filesize = info.get('filesize') or info.get('filesize_approx', 0)

            if filesize and filesize > max_size:
                raise FileSizeError(
                    f"File size (~{filesize / 1024 / 1024:.1f} MB) exceeds "
                    f"limit ({max_size / 1024 / 1024:.1f} MB)"
                )

    @abstractmethod
    def download_mp3(self, url: str) -> io.BytesIO:
        pass

    @abstractmethod
    def download_mp4(self, url: str) -> io.BytesIO:
        pass


class YoutubeDownloader(BaseDownloader):
    def get_platform_name(self) -> str:
        return "youtube"

    def clean_url(self, url: str) -> str:
        sanitized_url = self.sanitize_url(url)
        parsed = urlparse(sanitized_url)

        if 'youtube.com' not in parsed.netloc and 'youtu.be' not in parsed.netloc:
            raise InvalidURLError("Only YouTube URLs are allowed")

        # Short link youtu.be/VIDEO_ID
        if 'youtu.be' in parsed.netloc:
            video_id = parsed.path.strip('/')
            if not video_id:
                raise VideoNotFoundError("YouTube video ID not found in URL")
            return f"https://www.youtube.com/watch?v={video_id}"

        # Common link youtube.com/watch?v=VIDEO_ID
        qs = parse_qs(parsed.query)
        if "v" not in qs:
            raise VideoNotFoundError("YouTube video ID not found in URL")

        new_query = urlencode({"v": qs["v"][0]})
        return str(urlunparse(parsed._replace(query=new_query)))

    def download_mp3(self, url: str) -> io.BytesIO:
        url = self.clean_url(url)
        self._check_filesize_before_download(url, self.MAX_MP3_SIZE, 'mp3')

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

        log_download(platform=PlatformEnum.YOUTUBE, url=url, fmt=FormatEnum.MP3)
        return data

    def download_mp4(self, url: str) -> io.BytesIO:
        url = self.clean_url(url)
        self._check_filesize_before_download(url, self.MAX_MP4_SIZE, 'mp4')

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

        log_download(platform=PlatformEnum.YOUTUBE, url=url, fmt=FormatEnum.MP4)
        return data


class TiktokDownloader(BaseDownloader):
    def get_platform_name(self) -> str:
        return "tiktok"

    def clean_url(self, url: str) -> str:
        url = self.sanitize_url(url)
        parsed = urlparse(url)

        if 'tiktok.com' not in parsed.netloc:
            raise InvalidURLError("Only TikTok URLs are allowed")

        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def download_mp3(self, url: str) -> io.BytesIO:
        url = self.clean_url(url)
        self._check_filesize_before_download(url, self.MAX_MP3_SIZE, 'mp3')

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

        log_download(platform=PlatformEnum.TIKTOK, url=url, fmt=FormatEnum.MP3)
        return data

    def download_mp4(self, url: str) -> io.BytesIO:
        url = self.clean_url(url)
        self._check_filesize_before_download(url, self.MAX_MP4_SIZE, 'mp4')

        with tempfile.TemporaryDirectory() as tmpdir:
            fmt_opts = {
                "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
                "format": "best",
            }
            opts = self._get_opts(fmt_opts)

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)

            with open(filepath, "rb") as f:
                data = io.BytesIO(f.read())
                data.seek(0)

        log_download(platform=PlatformEnum.YOUTUBE, url=url, fmt=FormatEnum.MP4)
        return data
