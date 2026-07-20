from pathlib import Path


class TXTExtractor:

    def extract(self, path):

        text = Path(path).read_text(
            encoding="utf-8"
        )

        return {
            "title": Path(path).stem,
            "text": text
        }