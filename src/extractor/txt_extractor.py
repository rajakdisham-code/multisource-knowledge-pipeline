from pathlib import Path


class TXTExtractor:

    def extract(self, path):

        path = Path(path)

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        title = path.stem

        paragraphs = [

            p.strip()

            for p in text.split("\n")

            if p.strip()

        ]

        description = ""

        if paragraphs:

            description = paragraphs[0][:250]

        return {

            "title": title,

            "text": text,

            "author": "Unknown",

            "publisher": "Unknown",

            "description": description,

            "file_name": path.name,

            "file_extension": path.suffix,

            "file_size": path.stat().st_size

        }