import requests

from src.cache.download_cache import DownloadCache


class WebsiteDownloader:

    def __init__(self):

        self.cache = DownloadCache()

    def download(self, url):

        if self.cache.exists(url, "html"):

            print("Using cached webpage...")

            return str(
                self.cache.path(
                    url,
                    "html"
                )
            )

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        path = self.cache.path(
            url,
            "html"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(response.text)

        return str(path)