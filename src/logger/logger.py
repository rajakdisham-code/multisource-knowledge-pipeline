from pathlib import Path
from datetime import datetime
import threading


class PipelineLogger:

    _lock = threading.Lock()

    def __init__(self):

        self.log_dir = Path("logs")

        self.log_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        today = datetime.now().strftime(

            "%Y-%m-%d"

        )

        self.log_file = self.log_dir / f"{today}.log"

    # --------------------------------------------------

    def log(

        self,

        message

    ):

        timestamp = datetime.now().strftime(

            "%H:%M:%S"

        )

        with self._lock:

            with open(

                self.log_file,

                "a",

                encoding="utf-8"

            ) as f:

                f.write(

                    f"[{timestamp}] {message}\n"

                )

                f.flush()