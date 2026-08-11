from src.batch.batch_processor import BatchProcessor
from src.queue.job_queue import JobQueue
from src.state.state_manager import StateManager
from src.engine.scheduler import Scheduler


def main():

    print("\nLoading Knowledge Pipeline...\n")

    # ----------------------------------------------------

    batch = BatchProcessor()

    state = StateManager()

    queue = JobQueue()

    scheduler = Scheduler(

        state_manager=state,

        job_queue=queue

    )

    # ----------------------------------------------------

    sources = batch.get_sources()

    if not sources:

        print("No input files found.")

        return

    print(f"Found {len(sources)} source(s).\n")

    # ----------------------------------------------------

    scheduler.add_sources(

        sources

    )

    # ----------------------------------------------------

    summary = scheduler.run()

    # ----------------------------------------------------

    print("\n")

    print("=" * 60)

    print("PIPELINE FINISHED")

    print("=" * 60)

    print(f"Completed : {summary['completed']}")

    print(f"Failed    : {summary['failed']}")

    print(f"Duplicate : {summary['duplicates']}")

    print(f"Total     : {summary['total']}")

    print("=" * 60)

    state.close()


if __name__ == "__main__":

    main()