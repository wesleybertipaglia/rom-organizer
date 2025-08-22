import os
from datetime import datetime

class Logger:
    def __init__(self, output_dir: str, filename: str = "log.txt"):
        self.log_path = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)
        self._write_header()

    def _write_header(self):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write("=" * 60 + "\n")
            f.write(f"🕒 Log started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n")

    def log(self, message: str):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {message}\n")

    def path(self) -> str:
        return self.log_path
