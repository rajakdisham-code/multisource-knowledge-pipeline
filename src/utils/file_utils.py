import re
from pathlib import Path


INVALID_CHARS = r'[<>:"/\\|?*\x00-\x1F]'


def safe_filename(name: str, max_length=150):

    if not name:
        return "Untitled"

    name = re.sub(
        INVALID_CHARS,
        "",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    name = name.replace(
        " ",
        "_"
    )

    name = name.strip("._")

    if len(name) > max_length:

        name = name[:max_length]

    return name or "Untitled"


def ensure_directory(path):

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )