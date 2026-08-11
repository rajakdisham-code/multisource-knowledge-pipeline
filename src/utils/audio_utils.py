import os
import shutil
import subprocess
from pathlib import Path


class AudioUtils:
    """
    Utilities for handling audio files.
    """

    @staticmethod
    def get_audio_duration(audio_path):
        """
        Returns duration of an audio file in seconds.
        Requires ffprobe (installed with ffmpeg).
        """

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        return float(result.stdout.strip())

    # ---------------------------------------------------------

    @staticmethod
    def split_audio(audio_path, chunk_minutes=10):
        """
        Splits an audio file into fixed-length chunks.

        Returns:
            List[str] -> paths of chunk files
        """

        chunk_seconds = chunk_minutes * 60

        audio_path = Path(audio_path)

        chunk_folder = audio_path.parent / "chunks"

        chunk_folder.mkdir(exist_ok=True)

        output_pattern = chunk_folder / "chunk_%03d.mp3"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(audio_path),
            "-f",
            "segment",
            "-segment_time",
            str(chunk_seconds),
            "-c",
            "copy",
            str(output_pattern),
        ]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        chunks = sorted(
            str(file)
            for file in chunk_folder.glob("chunk_*.mp3")
        )

        return chunks

    # ---------------------------------------------------------

    @staticmethod
    def cleanup_chunks(chunk_paths):
        """
        Deletes temporary chunk files.
        """

        if not chunk_paths:
            return

        chunk_folder = Path(chunk_paths[0]).parent

        if chunk_folder.exists():
            shutil.rmtree(chunk_folder)