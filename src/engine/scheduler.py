from src.models.job import Job
from src.engine.worker_manager import WorkerManager
from pathlib import Path
import hashlib


class Scheduler:

    def __init__(

        self,

        state_manager,

        job_queue,

        max_retry=3

    ):

        self.state = state_manager

        self.queue = job_queue

        self.max_retry = max_retry

        self.worker_manager = WorkerManager(

            self.state

        )

    # -----------------------------------------------------
    def _processed_file(self, source):

        processed_dir = Path("processed_urls")

        processed_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        source_id = hashlib.md5(
            source.encode("utf-8")
        ).hexdigest()

        return processed_dir / f"{source_id}.txt"


    def add_sources(

        self,

        sources

    ):

        added = 0

        skipped = 0

        resumed = 0

        for source in sources:

            processed_file = self._processed_file(source)

            if processed_file.exists():

                print(
                    f"[SKIPPED - ALREADY PROCESSED] {source}"
                )

                skipped += 1
                continue

            record = self.state.get(
                source
            )

            # -----------------------------------------
            # Existing state
            # -----------------------------------------

            if record is not None:

                status = record["status"]

                # A COMPLETED job is considered processed
                # only when its processed_urls file exists.
                #
                # If that file was manually deleted,
                # allow the URL to be processed again.

                if status == "COMPLETED":

                    print(
                        f"[REPROCESS] {source}"
                    )

                else:

                    print(
                        f"[RESUME] {source}"
                    )

                    resumed += 1

            source_type = (

                "url"

                if source.startswith("http")

                else "file"

            )

            self.queue.put(

                Job(

                    source=source,

                    source_type=source_type

                )

            )

            added += 1

        print(

            f"\nJobs Added : {added}"

        )

        print(

            f"Jobs Skipped : {skipped}"

        )

        print(

            f"Jobs Resumed : {resumed}\n"

        )

    # -----------------------------------------------------

    def run(

        self

    ):

        summary = self.worker_manager.execute(

            self.queue

        )

        return summary