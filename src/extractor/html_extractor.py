from pathlib import Path
import trafilatura
from bs4 import BeautifulSoup


class HTMLExtractor:

    def extract(self, html_path):

        html_path = Path(html_path)

        html = html_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        # -------- Get Title --------

        soup = BeautifulSoup(html, "lxml")

        title = ""

        if soup.title:
            title = soup.title.text.strip()

        # -------- Extract Main Text --------

        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            include_links=False,
            favor_precision=True,
            deduplicate=True
        )

        if not text:
            text = soup.get_text(
                separator="\n",
                strip=True
            )

        return {
            "title": title,
            "text": text
        }