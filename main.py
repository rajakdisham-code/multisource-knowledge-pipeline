from src.pipeline import KnowledgePipeline
from src.batch.batch_processor import BatchProcessor
from src.state.state_manager import StateManager
from src.logger.logger import PipelineLogger

pipeline = KnowledgePipeline()

batch = BatchProcessor()

state = StateManager()

logger = PipelineLogger()

sources = batch.get_sources()

if not sources:

    print("No files found.")

    logger.log("No input sources found.")

else:

    total = len(sources)

    success = 0
    failed = 0
    skipped = 0

    logger.log("=" * 60)
    logger.log("Pipeline Started")

    for index, source in enumerate(sources, start=1):

        if state.is_completed(source):

            skipped += 1

            print(f"[SKIPPED] {source}")

            logger.log(f"SKIPPED : {source}")

            continue

        print("\n" + "=" * 60)
        print(f"[{index}/{total}]")
        print(source)
        print("=" * 60)

        logger.log(f"START : {source}")

        try:

            output = pipeline.run(source)

            state.mark_completed(source)

            success += 1

            logger.log(f"SUCCESS : {output}")

            print(f"\n✅ Saved : {output}")

        except Exception as e:

            failed += 1

            logger.log(f"FAILED : {source}")

            logger.log(str(e))

            print(f"\n❌ Failed : {e}")

    logger.log("-" * 60)
    logger.log(f"Total : {total}")
    logger.log(f"Success : {success}")
    logger.log(f"Failed : {failed}")
    logger.log(f"Skipped : {skipped}")
    logger.log("Pipeline Finished")
    logger.log("=" * 60)

    print("\n========== SUMMARY ==========")
    print(f"Total    : {total}")
    print(f"Success  : {success}")
    print(f"Failed   : {failed}")
    print(f"Skipped  : {skipped}")
    print("=============================\n")