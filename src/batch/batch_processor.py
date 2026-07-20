from pathlib import Path


class BatchProcessor:

    def get_sources(self, input_dir="input"):

        input_path = Path(input_dir)

        sources = []

        for file in input_path.iterdir():

            if file.is_file():

                if file.suffix.lower() == ".txt" and file.name == "urls.txt":

                    with open(file, "r", encoding="utf-8") as f:

                        for line in f:

                            line = line.strip().strip('"').strip("'")

                            if line:

                                sources.append(line)

                else:

                    sources.append(str(file).strip('"').strip("'"))

        return sources