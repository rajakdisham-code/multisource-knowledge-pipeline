import hashlib
from pathlib import Path


class DuplicateDetector:

    def __init__(self):

        self.db = Path("cache/duplicates.txt")

        self.db.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.db.exists():

            self.db.touch()

    def _hash(self, text):

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def is_duplicate(self, text):

        h = self._hash(text)

        with open(
            self.db,
            "r",
            encoding="utf-8"
        ) as f:

            hashes = {
                line.strip()
                for line in f
            }

        return h in hashes

    def add(self, text):

        h = self._hash(text)

        with open(
            self.db,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(h + "\n")