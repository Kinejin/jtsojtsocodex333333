import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
OUTPUT_DIR = os.path.join(BASE_DIR, 'downloads')
FAVORITES_FILE = os.path.join(BASE_DIR, 'favorites.json')

FFMPEG_PATH = 'ffmpeg'
YTDLP_PATH = 'yt-dlp'

CHECK_INTERVAL = 60  # seconds

for directory in (CACHE_DIR, OUTPUT_DIR):
    os.makedirs(directory, exist_ok=True)
