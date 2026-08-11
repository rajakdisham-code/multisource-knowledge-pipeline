from pathlib import Path


class BatchProcessor:

    def __init__(

        self,

        input_dir="input"

    ):

        self.input_dir = Path(

            input_dir

        )

    # -----------------------------------------------------

    def get_sources(self):

        if not self.input_dir.exists():

            raise FileNotFoundError(

                f"Input directory not found : "

                f"{self.input_dir}"

            )

        sources = []

        for file in sorted(

            self.input_dir.iterdir()

        ):

            if not file.is_file():

                continue

            # -----------------------------------------
            # URL List
            # -----------------------------------------

            if (

                file.suffix.lower() == ".txt"

                and file.name.lower() == "urls.txt"

            ):

                with open(

                    file,

                    "r",

                    encoding="utf-8"

                ) as f:

                    for line in f:

                        line = (

                            line.strip()

                            .strip('"')

                            .strip("'")

                        )

                        if line:

                            sources.append(

                                line

                            )

            # -----------------------------------------
            # Local Files
            # -----------------------------------------

            else:

                sources.append(

                    str(file.resolve())

                )

        return sources