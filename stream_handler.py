import os
import threading
import subprocess
import time

from config import OUTPUT_DIR, YTDLP_PATH


class StreamDownloader(threading.Thread):
    def __init__(self, url, quality='best', output_name=None, progress_callback=None, log_callback=None):
        super().__init__(daemon=True)
        self.url = url
        self.quality = quality
        self.output_name = output_name or f"download_{int(time.time())}.mp4"
        self.progress_callback = progress_callback or (lambda msg: None)
        self.log_callback = log_callback or (lambda msg: None)
        self._stop_event = threading.Event()

    def run(self):
        output_path = os.path.join(OUTPUT_DIR, self.output_name)
        cmd = [YTDLP_PATH, '-f', self.quality, '-o', output_path, self.url]
        self.log_callback(f"Running: {' '.join(cmd)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            if self._stop_event.is_set():
                process.terminate()
                break
            if self.progress_callback:
                self.progress_callback(line.strip())

        process.wait()
        if process.returncode == 0:
            self.log_callback(f"Download completed: {output_path}")
        else:
            self.log_callback(f"Download failed: {self.url}")

    def stop(self):
        self._stop_event.set()

    @staticmethod
    def get_available_qualities(url):
        cmd = [YTDLP_PATH, '-F', url]
        try:
            output = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as e:
            return e.output
