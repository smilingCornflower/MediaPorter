MediaPorter is an educational web application designed as a lab exercise in secure web development. It functions as an HTTP server for downloading media from YouTube in MP3 and MP4 formats.

Application Features:
- Downloading YouTube videos as MP4 and audio as MP3.
- Converting audio to MP3 using ffmpeg.
- Serving downloaded files to clients via HTTP.
- Using temporary directories for safe file storage.

Lab Work Purpose:
- The application intentionally contains vulnerabilities for educational purposes:
- Exposure of internal information through unhandled exceptions.
- Hardcoded secrets in the code.
- Configuration files with secrets committed to the repository.

The goal is to learn how to identify and fix these issues without breaking the core functionality of the application.