from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from config.settings import MAX_WORKERS
from config.settings import MAX_RETRIES

from src.engine.worker import Worker

from src.translator.translator import TranscriptTranslator

from pathlib import Path
import hashlib


class WorkerManager:

    def __init__(

        self,

        state_manager

    ):

        self.state = state_manager

    # -----------------------------------------------------

    def execute(

        self,

        job_queue

    ):

        completed = 0

        failed = 0

        duplicates = 0

        retry_queue = []

        translator = TranscriptTranslator()

        while True:

            futures = []

            with ThreadPoolExecutor(

                max_workers=MAX_WORKERS

            ) as executor:

                worker_id = 1

                while not job_queue.empty():

                    job = job_queue.get()

                    worker = Worker(

                        worker_id,

                        self.state ,

                        translator


                    )

                    futures.append(

                        (

                            job,

                            executor.submit(

                                worker.process,

                                job

                            )

                        )

                    )

                    worker_id += 1

                    if worker_id > MAX_WORKERS:

                        worker_id = 1

                for job, future in as_completed_dict(futures):

                    try:

                        result = future.result()

                        if result is None:

                            retry = getattr(

                                job,

                                "retry_count",

                                0

                            )

                            retry += 1

                            job.retry_count = retry

                            if retry <= MAX_RETRIES:

                                print(

                                    f"\nRetry {retry}/{MAX_RETRIES}"

                                    f" : {job.source}"

                                )

                                retry_queue.append(

                                    job

                                )

                            else:

                                failed += 1

                            continue

                        if result.duplicate:

                            duplicates += 1

                        else:
                            processed_dir = Path("processed_urls")

                            processed_dir.mkdir(
                                parents=True,
                                exist_ok=True
                            )

                            source_id = hashlib.md5(
                                job.source.encode("utf-8")
                            ).hexdigest()

                            processed_file = (
                                processed_dir / f"{source_id}.txt"
                            )

                            processed_file.write_text(
                                job.source,
                                encoding="utf-8"
                            )

                            completed += 1

                    except Exception as e:

                        retry = getattr(

                            job,

                            "retry_count",

                            0

                        )

                        retry += 1

                        job.retry_count = retry

                        print(

                            f"\nWorker Error : {e}"

                        )

                        if retry <= MAX_RETRIES:

                            retry_queue.append(

                                job

                            )

                        else:

                            failed += 1

            if not retry_queue:

                break

            while retry_queue:

                job_queue.put(

                    retry_queue.pop(0)

                )

        return {

            "completed": completed,

            "failed": failed,

            "duplicates": duplicates,

            "total": completed + failed + duplicates

        }


# ---------------------------------------------------------

def as_completed_dict(

    futures

):

    mapping = {

        future: job

        for job, future in futures

    }

    for future in as_completed(

        mapping

    ):

        yield mapping[future], future