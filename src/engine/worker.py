from datetime import datetime

from src.pipeline import KnowledgePipeline
from src.writer.metadata_writer import MetadataWriter

from src.checkpoint.checkpoint_manager import CheckpointManager

class Worker:

    def __init__(
        self,
        worker_id,
        state_manager,
        translator
    ):
        self.worker_id = worker_id
        self.state = state_manager
        self.translator = translator

        self.writer = MetadataWriter()
        self.checkpoint = CheckpointManager()

    # -----------------------------------------------------

    def process(

        self,

        job

    ):

        pipeline = KnowledgePipeline(
            translator=self.translator
        )

        try:

            print(

                f"[Worker {self.worker_id}] "

                f"Started : {job.source}"

            )

            self.state.mark_running(

                job

            )

            result = pipeline.run(
                job.source,
                job=job,
                state=self.state,
                worker_id=self.worker_id
            )

            if result.duplicate:

                print(

                    f"[Worker {self.worker_id}] "

                    f"Duplicate : {job.source}"

                )

                return result

            self.writer.write(

                result.metadata

            )

            self.state.mark_completed(

                job,

                result.output_path

            )

            self.checkpoint.cleanup(job)

            print(

                f"[Worker {self.worker_id}] "

                f"Completed : {job.source}"

            )

            return result

        except Exception as e:

            self.state.mark_failed(

                job,

                str(e)

            )

            print(

                f"[Worker {self.worker_id}] "

                f"FAILED : {job.source}"

            )

            print(e)

            return None