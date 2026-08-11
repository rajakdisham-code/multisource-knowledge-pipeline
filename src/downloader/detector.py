from pathlib import Path


class SourceDetector:

    @staticmethod
    def detect(source):

        source = source.strip()

        # ---------- YouTube ----------
        if (
            "youtube.com" in source
            or "youtu.be" in source
        ):
            return "youtube"

        # ---------- Website ----------
        if (
            source.startswith("http://")
            or source.startswith("https://")
        ):
            return "website"

        # ---------- Local File ----------
        suffix = Path(source).suffix.lower()

        if suffix == ".pdf":
            return "pdf"

        if suffix == ".docx":
            return "docx"

        if suffix == ".epub":
            return "epub"

        if suffix == ".txt":
            return "txt"

        if suffix in [".mp3", ".wav", ".m4a"]:
            return "audio"

        if suffix in [".mp4", ".avi", ".mov", ".mkv"]:
            return "video"

        return "unknown"