from pathlib import Path

from src.utils.file_utils import (
    safe_filename,
    ensure_directory
)


class TXTExporter:

    def __init__(self, output_dir="processed"):

        self.output_dir = Path(output_dir)

        ensure_directory(self.output_dir)

    # -------------------------------------------------

    def export(self, document, text=None, suffix=""):

        filename = safe_filename(document.title)

        if suffix:

            filename += suffix

        output_file = self.output_dir / f"{filename}.txt"

        if text is None:

            text = document.clean_text

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as f:

            f.write("TITLE\n")
            f.write(document.title)

            f.write("\n\nSOURCE\n")
            f.write(document.source)

            if document.url:

                f.write("\n\nURL\n")
                f.write(document.url)

            f.write("\n\nCONTENT\n\n")
            f.write(text)

        return output_file