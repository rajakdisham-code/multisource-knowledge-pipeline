import hashlib
import json
import shutil

from pathlib import Path


class CheckpointManager:

    def __init__(self):

        self.root = Path("cache") / "checkpoints"

        self.root.mkdir(

            parents=True,

            exist_ok=True

        )

    # ---------------------------------------------------------

    def _job_id(

        self,

        job

    ):

        return hashlib.sha256(

            job.source.encode(

                "utf-8"

            )

        ).hexdigest()

    # ---------------------------------------------------------

    def _job_dir(

        self,

        job

    ):

        path = self.root / self._job_id(

            job

        )

        path.mkdir(

            parents=True,

            exist_ok=True

        )

        return path

    # ---------------------------------------------------------

    def transcript_file(

        self,

        job

    ):

        return self._job_dir(

            job

        ) / "transcript.txt"

    # ---------------------------------------------------------

    def timestamp_file(

        self,

        job

    ):

        return self._job_dir(

            job

        ) / "timestamps.txt"

    # ---------------------------------------------------------

    def metadata_file(

        self,

        job

    ):

        return self._job_dir(

            job

        ) / "checkpoint.json"

    # ---------------------------------------------------------

    def append_chunk(

        self,

        job,

        transcript,

        timestamp_text

    ):

        with open(

            self.transcript_file(

                job

            ),

            "a",

            encoding="utf-8"

        ) as f:

            f.write(

                transcript

            )

            f.write(

                "\n\n"

            )

        with open(

            self.timestamp_file(

                job

            ),

            "a",

            encoding="utf-8"

        ) as f:

            f.write(

                timestamp_text

            )

            f.write(

                "\n\n"

            )

    # ---------------------------------------------------------

    def load_transcript(

        self,

        job

    ):

        path = self.transcript_file(

            job

        )

        if not path.exists():

            return ""

        return path.read_text(

            encoding="utf-8"

        )

    # ---------------------------------------------------------

    def load_timestamp(

        self,

        job

    ):

        path = self.timestamp_file(

            job

        )

        if not path.exists():

            return ""

        return path.read_text(

            encoding="utf-8"

        )

    # ---------------------------------------------------------

    def save_metadata(

        self,

        job,

        data

    ):

        with open(

            self.metadata_file(

                job

            ),

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False

            )

    # ---------------------------------------------------------

    def load_metadata(

        self,

        job

    ):

        path = self.metadata_file(

            job

        )

        if not path.exists():

            return None

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(

                f

            )

    # ---------------------------------------------------------

    def exists(

        self,

        job

    ):

        return self._job_dir(

            job

        ).exists()

    # ---------------------------------------------------------

    def cleanup(

        self,

        job

    ):

        folder = self._job_dir(

            job

        )

        if folder.exists():

            shutil.rmtree(

                folder

            )