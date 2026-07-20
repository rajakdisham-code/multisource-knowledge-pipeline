import json
from pathlib import Path


class StateManager:

    def __init__(self):

        self.state_file = Path("state.json")

        if not self.state_file.exists():

            with open(
                self.state_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {"completed": []},
                    f,
                    indent=4
                )

    def _load(self):

        with open(
            self.state_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def _save(self, data):

        with open(
            self.state_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def is_completed(self, source):

        data = self._load()

        return source in data["completed"]

    def mark_completed(self, source):

        data = self._load()

        if source not in data["completed"]:

            data["completed"].append(source)

            self._save(data)