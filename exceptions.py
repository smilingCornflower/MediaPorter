class DownloadError(Exception):
    pass


class InvalidURLError(DownloadError):
    pass


class FileSizeError(DownloadError):
    pass


class VideoNotFoundError(DownloadError):
    pass
