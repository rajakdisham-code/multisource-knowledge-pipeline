import json
from pathlib import Path

from src.utils.file_utils import (
    safe_filename,
    ensure_directory
)


class JSONExporter:

    def __init__(self, output_dir="metadata"):

        self.output = Path(output_dir)

        ensure_directory(
            self.output
        )

    def export(
        self,
        filename,
        metadata
    ):

        filename = safe_filename(
            filename
        )

        path = self.output / f"{filename}.json"

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

        return path