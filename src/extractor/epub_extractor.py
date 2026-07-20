from pathlib import Path
from ebooklib import epub
from bs4 import BeautifulSoup


class EPUBExtractor:

    def extract(self, path):

        book = epub.read_epub(path)

        text = []

        for item in book.get_items():

            if item.get_type() == 9:

                soup = BeautifulSoup(
                    item.get_content(),
                    "html.parser"
                )

                text.append(
                    soup.get_text(" ", strip=True)
                )

        return {
            "title": Path(path).stem,
            "text": "\n".join(text)
        }