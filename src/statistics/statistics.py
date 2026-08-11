from collections import defaultdict
from datetime import datetime


class Statistics:

    def __init__(self):

        self.start_time = datetime.now()

        self.total = 0

        self.processed = 0

        self.failed = 0

        self.skipped = 0

        self.duplicates = 0

        self.cache_hits = 0

        self.transcript_cache_hits = 0

        self.download_cache_hits = 0

        self.document_types = defaultdict(int)

    # ---------------------------------

    def add_total(self):

        self.total += 1

    # ---------------------------------

    def add_processed(self):

        self.processed += 1

    # ---------------------------------

    def add_failed(self):

        self.failed += 1

    # ---------------------------------

    def add_duplicate(self):

        self.duplicates += 1

    # ---------------------------------

    def add_skipped(self):

        self.skipped += 1

    # ---------------------------------

    def add_cache_hit(self):

        self.cache_hits += 1

    # ---------------------------------

    def add_transcript_cache_hit(self):

        self.transcript_cache_hits += 1

    # ---------------------------------

    def add_download_cache_hit(self):

        self.download_cache_hits += 1

    # ---------------------------------

    def add_document(self, doc_type):

        self.document_types[doc_type] += 1

    # ---------------------------------

    def summary(self):

        elapsed = datetime.now() - self.start_time

        print()

        print("=" * 60)

        print("Knowledge Pipeline Statistics")

        print("=" * 60)

        print(f"Total Sources           : {self.total}")

        print(f"Processed               : {self.processed}")

        print(f"Duplicates              : {self.duplicates}")

        print(f"Skipped                 : {self.skipped}")

        print(f"Failed                  : {self.failed}")

        print()

        print("Document Types")

        print("--------------------------")

        for k, v in sorted(self.document_types.items()):

            print(f"{k:25} {v}")

        print()

        print(f"Gemini Cache Hits       : {self.cache_hits}")

        print(f"Transcript Cache Hits   : {self.transcript_cache_hits}")

        print(f"Download Cache Hits     : {self.download_cache_hits}")

        print()

        print(f"Elapsed Time            : {elapsed}")

        print("=" * 60)