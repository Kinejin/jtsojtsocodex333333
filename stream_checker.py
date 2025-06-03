import threading
import subprocess
import time

from config import YTDLP_PATH, CHECK_INTERVAL


class StreamChecker(threading.Thread):
    def __init__(self, favorites_manager, on_live_callback, log_callback=None):
        super().__init__(daemon=True)
        self.fav_manager = favorites_manager
        self.on_live_callback = on_live_callback
        self.log_callback = log_callback or (lambda msg: None)
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            for fav in self.fav_manager.favorites:
                if not fav.get('auto_capture'):
                    continue
                url = fav['url']
                cmd = [YTDLP_PATH, '--no-playlist', '--simulate', url]
                try:
                    subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                    self.log_callback(f"Live detected: {fav['name']}")
                    self.on_live_callback(fav)
                except subprocess.CalledProcessError:
                    pass
            for _ in range(CHECK_INTERVAL):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def stop(self):
        self._stop_event.set()
