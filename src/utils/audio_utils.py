import shutil
import subprocess
from pathlib import Path


class AudioUtils:
    """
    Utilities for handling audio files.
    """

    @staticmethod
    def get_audio_duration(audio_path):

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
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
    def split_audio(audio_path, chunk_minutes=15):
        """
        Split audio into Whisper-safe WAV chunks.

        IMPORTANT:
        The audio is re-encoded instead of using
        '-c copy'. This prevents MP3 chunk boundary
        and decoding problems.
        """

        chunk_seconds = chunk_minutes * 60

        audio_path = Path(audio_path)

        chunk_folder = (
            audio_path.parent
            / f"{audio_path.stem}_chunks"
        )

        # Remove old chunks from previous runs.
        if chunk_folder.exists():
            shutil.rmtree(chunk_folder)

        chunk_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_pattern = (
            chunk_folder
            / "chunk_%03d.wav"
        )

        command = [
            "ffmpeg",
            "-y",

            "-i",
            str(audio_path),

            "-map",
            "0:a:0",

            "-f",
            "segment",

            "-segment_time",
            str(chunk_seconds),

            # Force clean, independent audio
            "-ac",
            "1",

            "-ar",
            "16000",

            "-c:a",
            "pcm_s16le",

            str(output_pattern),
        ]

        print(
            "\n[Audio] Creating clean Whisper "
            "audio chunks..."
        )

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        chunks = sorted(
            str(file)
            for file in chunk_folder.glob(
                "chunk_*.wav"
            )
        )

        if not chunks:
            raise RuntimeError(
                f"No audio chunks created from: "
                f"{audio_path}"
            )

        print(
            f"[Audio] Created {len(chunks)} "
            f"chunk(s)"
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

        chunk_folder = Path(
            chunk_paths[0]
        ).parent

        if chunk_folder.exists():
            shutil.rmtree(
                chunk_folder
            )