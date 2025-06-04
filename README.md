# Live Stream Downloader

Simple tkinter application for downloading live streams using `yt-dlp`.

## Features

- Manage a list of favorite streams with quality and auto capture flag.
- Start/stop manual downloads.
- Automatic capturing of favorites when they go live.
- Detection of stalled downloads: if no new segments are generated for `SEGMENT_TIMEOUT` seconds the capture stops, but auto capture will start again when the stream returns.
