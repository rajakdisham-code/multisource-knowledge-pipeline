from pathlib import Path

from src.utils.file_utils import (
    safe_filename,
    ensure_directory
)


class TXTExporter:

    def __init__(self, output_dir="processed"):

        self.output_dir = Path(output_dir)

        ensure_directory(
            self.output_dir
        )

    def export(self, document):

        filename = safe_filename(
            document.title
        )

        output_file = self.output_dir / f"{filename}.txt"

        data = document.clean_text

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            # ---------------------------------------
            # Non-Knowledge Documents
            # ---------------------------------------
            if isinstance(data, str):

                f.write("TITLE\n")
                f.write(document.title)

                f.write("\n\nSOURCE\n")
                f.write(document.source)

                if document.url:

                    f.write("\n\nURL\n")
                    f.write(document.url)

                f.write("\n\nCONTENT\n\n")
                f.write(data)

                return output_file

            # ---------------------------------------
            # Knowledge Documents
            # ---------------------------------------

            f.write("TITLE\n")
            f.write(document.title)

            f.write("\n\nSOURCE\n")
            f.write(document.source)

            if document.url:

                f.write("\n\nURL\n")
                f.write(document.url)

            f.write("\n\nDEFINITION\n")
            f.write(
                data.get(
                    "definition",
                    "Not Available"
                )
            )

            f.write("\n\nOVERVIEW\n")
            f.write(
                data.get(
                    "overview",
                    "Not Available"
                )
            )

            f.write("\n\nKEY COMPONENTS/ASPECTS\n")
            f.write(
                data.get(
                    "key_components",
                    "Not Available"
                )
            )

            f.write("\n\nMECHANISM/PROCESS/APPLICATION\n")
            f.write(
                data.get(
                    "mechanism",
                    "Not Available"
                )
            )

            f.write("\n\nEXAMPLES\n")
            f.write(
                data.get(
                    "examples",
                    "Not Available"
                )
            )

            f.write("\n\nRELATIONSHIPS/CONNECTIONS\n")
            f.write(
                data.get(
                    "relationships",
                    "Not Available"
                )
            )

            f.write("\n\nIMPORTANT DISTINCTIONS\n")
            f.write(
                data.get(
                    "important_distinctions",
                    "Not Available"
                )
            )

            f.write("\n\nSUMMARY/KEY TAKEAWAYS\n")
            f.write(
                data.get(
                    "summary",
                    "Not Available"
                )
            )

        return output_file