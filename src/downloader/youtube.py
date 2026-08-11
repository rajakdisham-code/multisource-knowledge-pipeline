from pathlib import Path

import yt_dlp

from src.utils.file_utils import safe_filename


class YouTubeDownloader:

    def __init__(self):
        self.output_dir = Path("raw/youtube")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def download(self, url):

        url = url.strip()
        print(f"Downloading URL: {repr(url)}")

        output_template = str(
            self.output_dir / "%(id)s.%(ext)s"
        )

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": False,
            "noplaylist": True,
            "extractaudio": True,
            "retries": 10,
            "fragment_retries": 10,
            "socket_timeout": 30,

            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]
                }
            },

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192"
                }
            ]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=True
            )

            downloaded_file = Path(
                ydl.prepare_filename(info)
            )

        audio_path = downloaded_file.with_suffix(".mp3")

        title = safe_filename(
            info.get("title", "Untitled")
        )

        author = info.get(
            "uploader",
            "Unknown"
        )

        publisher = info.get(
            "channel",
            author
        )

        description = info.get(
            "description",
            ""
        )

        tags = ", ".join(
            info.get("tags", [])
        )

        upload_date = info.get(
            "upload_date",
            ""
        )

        if upload_date and len(upload_date) == 8:
            upload_date = (
                f"{upload_date[:4]}-"
                f"{upload_date[4:6]}-"
                f"{upload_date[6:]}"
            )

        return {
            "title": title,
            "url": url,
            "audio": str(audio_path),
            "duration": info.get("duration", 0),
            "author": author,
            "publisher": publisher,
            "description": description,
            "channel": publisher,
            "channel_id": info.get("channel_id", ""),
            "upload_date": upload_date,
            "tags": tags,
            "thumbnail": info.get("thumbnail", ""),
            "view_count": info.get("view_count", 0),
            "like_count": info.get("like_count", 0),
            "comment_count": info.get("comment_count", 0),
            "duration_seconds": info.get("duration", 0),
            "categories": ", ".join(
                info.get("categories", [])
            ),
            "webpage_url": info.get(
                "webpage_url",
                url
            )
        }