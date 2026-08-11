from pathlib import Path

from ebooklib import epub
from ebooklib import ITEM_DOCUMENT

from bs4 import BeautifulSoup


class EPUBExtractor:

    def extract(

        self,

        path,

        job=None,

        state=None

    ):

        path = Path(path)

        book = epub.read_epub(path)

        text = []

        # ---------------------------------
        # Metadata
        # ---------------------------------

        title = path.stem

        author = "Unknown"

        publisher = "Unknown"

        description = ""

        if book.get_metadata("DC", "title"):

            title = book.get_metadata(

                "DC",

                "title"

            )[0][0]

        if book.get_metadata("DC", "creator"):

            author = book.get_metadata(

                "DC",

                "creator"

            )[0][0]

        if book.get_metadata("DC", "publisher"):

            publisher = book.get_metadata(

                "DC",

                "publisher"

            )[0][0]

        if book.get_metadata("DC", "description"):

            description = book.get_metadata(

                "DC",

                "description"

            )[0][0]

        # ---------------------------------
        # Resume
        # ---------------------------------

        documents = [

            item

            for item in book.get_items()

            if item.get_type() == ITEM_DOCUMENT

        ]

        total_chapters = len(

            documents

        )

        start_chapter = 0

        if job is not None and state is not None:

            checkpoint = state.load_checkpoint(

                job.source

            )

            if checkpoint:

                start_chapter = checkpoint.get(

                    "current_page",

                    0

                )

                print(

                    f"\nResuming EPUB chapter "

                    f"{start_chapter + 1}/{total_chapters}"

                )

        # ---------------------------------
        # Extract
        # ---------------------------------

        for index in range(

            start_chapter,

            total_chapters

        ):

            item = documents[index]

            soup = BeautifulSoup(

                item.get_content(),

                "html.parser"

            )

            content = soup.get_text(

                " ",

                strip=True

            )

            if content:

                text.append(

                    content

                )

            if job is not None and state is not None:

                state.save_checkpoint(

                    job,

                    stage="EPUB_EXTRACT",

                    current_page=index + 1,

                    total_pages=total_chapters

                )

                state.update_progress(

                    job,

                    stage="EPUB_EXTRACT",

                    progress=int(

                        (

                            (index + 1)

                            / total_chapters

                        )

                        * 100

                    )

                )

        full_text = "\n".join(

            text

        )

        # ---------------------------------
        # Description
        # ---------------------------------

        if not description:

            paragraphs = [

                p.strip()

                for p in full_text.split("\n")

                if p.strip()

            ]

            if paragraphs:

                description = paragraphs[0][:250]

        return {

            "title": title,

            "text": full_text,

            "author": author,

            "publisher": publisher,

            "description": description,

            "file_name": path.name,

            "file_extension": path.suffix,

            "file_size": path.stat().st_size

        }