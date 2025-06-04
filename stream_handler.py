import os
import threading
import subprocess
import time

from config import OUTPUT_DIR, YTDLP_PATH, SEGMENT_TIMEOUT


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
        self.process = process

        last_size = 0
        last_size_time = time.time()

        while True:
            line = process.stdout.readline()
            if line:
                if self.progress_callback:
                    self.progress_callback(line.strip())
            if self._stop_event.is_set():
                process.terminate()
                break
            if not line and process.poll() is not None:
                break

            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                if size != last_size:
                    last_size = size
                    last_size_time = time.time()
            if time.time() - last_size_time > SEGMENT_TIMEOUT:
                self.log_callback("No new segments detected, stopping capture.")
                self.stop()
                process.terminate()
                break

            time.sleep(0.5)

        process.wait()
        if process.returncode == 0:
            self.log_callback(f"Download completed: {output_path}")
        else:
            self.log_callback(f"Download failed: {self.url}")

    def stop(self):
        self._stop_event.set()
        if hasattr(self, 'process') and self.process.poll() is None:
            self.process.terminate()

    @staticmethod
    def get_available_qualities(url):
        cmd = [YTDLP_PATH, '-F', url]
        try:
            output = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as e:
            return e.output
