import json
from pathlib import Path
from collections import Counter
from datetime import datetime


class ReportGenerator:

    def __init__(self):

        self.report_json = Path("reports/json")
        self.report_csv = Path("reports/csv")

        self.report_json.mkdir(
            parents=True,
            exist_ok=True
        )

        self.report_csv.mkdir(
            parents=True,
            exist_ok=True
        )

        self.total_documents = 0

        self.total_words = 0

        self.total_tokens = 0

        self.total_characters = 0

        self.total_reading_time = 0

        self.sources = Counter()

        self.languages = Counter()

        self.domains = Counter()

        self.subdomains = Counter()

        self.publishers = Counter()

    # --------------------------------------------------

    def add(self, metadata):

        self.total_documents += 1

        self.total_words += metadata.get(
            "word_count",
            0
        )

        self.total_tokens += metadata.get(
            "token_count",
            0
        )

        self.total_characters += metadata.get(
            "character_count",
            0
        )

        self.total_reading_time += metadata.get(
            "reading_time_minutes",
            0
        )

        self.sources[
            metadata.get(
                "source_type",
                "Unknown"
            )
        ] += 1

        self.languages[
            metadata.get(
                "language",
                "Unknown"
            )
        ] += 1

        self.domains[
            metadata.get(
                "domain",
                "Unknown"
            )
        ] += 1

        self.subdomains[
            metadata.get(
                "subdomain",
                "Unknown"
            )
        ] += 1

        self.publishers[
            metadata.get(
                "publisher",
                "Unknown"
            )
        ] += 1

    # --------------------------------------------------

    def _save_counter_csv(
        self,
        filename,
        title,
        counter
    ):

        file = self.report_csv / filename

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(f"{title},Count\n")

            for key, value in sorted(

                counter.items(),

                key=lambda x: x[1],

                reverse=True

            ):

                f.write(
                    f"{key},{value}\n"
                )

    # --------------------------------------------------

    def generate(self):

        average_words = 0

        average_tokens = 0

        average_characters = 0

        average_reading = 0

        if self.total_documents > 0:

            average_words = round(
                self.total_words /
                self.total_documents,
                2
            )

            average_tokens = round(
                self.total_tokens /
                self.total_documents,
                2
            )

            average_characters = round(
                self.total_characters /
                self.total_documents,
                2
            )

            average_reading = round(
                self.total_reading_time /
                self.total_documents,
                2
            )

        summary = {

            "generated_at": datetime.now().isoformat(),

            "total_documents": self.total_documents,

            "total_words": self.total_words,

            "total_tokens": self.total_tokens,

            "total_characters": self.total_characters,

            "total_reading_time_minutes": self.total_reading_time,

            "average_words_per_document": average_words,

            "average_tokens_per_document": average_tokens,

            "average_characters_per_document": average_characters,

            "average_reading_time_minutes": average_reading,

            "sources": dict(self.sources),

            "languages": dict(self.languages),

            "domains": dict(self.domains),

            "subdomains": dict(self.subdomains),

            "publishers": dict(self.publishers),

            "top_publishers": dict(
                self.publishers.most_common(10)
            ),

            "top_domains": dict(
                self.domains.most_common(10)
            ),

            "top_subdomains": dict(
                self.subdomains.most_common(10)
            )

        }

        with open(

            self.report_json /
            "summary.json",

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                summary,

                f,

                indent=4,

                ensure_ascii=False

            )

        self._save_counter_csv(

            "source_distribution.csv",

            "Source",

            self.sources

        )

        self._save_counter_csv(

            "language_distribution.csv",

            "Language",

            self.languages

        )

        self._save_counter_csv(

            "domain_distribution.csv",

            "Domain",

            self.domains

        )

        self._save_counter_csv(

            "subdomain_distribution.csv",

            "Subdomain",

            self.subdomains

        )

        self._save_counter_csv(

            "publisher_distribution.csv",

            "Publisher",

            self.publishers

        )

        print("\n========== REPORT ==========")

        print(
            f"Documents          : {self.total_documents}"
        )

        print(
            f"Words              : {self.total_words}"
        )

        print(
            f"Tokens             : {self.total_tokens}"
        )

        print(
            f"Characters         : {self.total_characters}"
        )

        print(
            f"Reading Time (min) : {self.total_reading_time}"
        )

        print(
            "Reports saved in reports/"
        )

        print("============================\n")