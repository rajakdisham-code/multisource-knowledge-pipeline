from src.models.document import Document


class DocumentParser:

    def parse(
        self,
        title,
        source,
        source_type,
        text,
        url=""
    ):

        title = self.clean_title(title)

        return Document(
            title=title,
            source=source,
            source_type=source_type,
            raw_text=text,
            clean_text=text,
            url=url
        )

    def clean_title(self, title):

        title = title.strip()

        suffixes = [
            " - Wikipedia",
            " | Wikipedia",
            " - YouTube",
            " | YouTube",
            " - Google Books",
            " | Google Books",
            " - Britannica",
            " | Britannica",
        ]

        for suffix in suffixes:

            if title.endswith(suffix):

                title = title[:-len(suffix)].strip()

        return title