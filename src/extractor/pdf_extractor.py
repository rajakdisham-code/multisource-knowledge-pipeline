from pathlib import Path

from PyPDF2 import PdfReader


class PDFExtractor:

    def extract(

        self,

        pdf_path,

        job=None,

        state=None

    ):

        pdf_path = Path(pdf_path)

        reader = PdfReader(pdf_path)

        text = []

        metadata = reader.metadata or {}

        total_pages = len(

            reader.pages

        )

        # -----------------------------------------
        # Resume Support
        # -----------------------------------------

        start_page = 0

        if job is not None and state is not None:

            checkpoint = state.load_checkpoint(

                job.source

            )

            if checkpoint:

                start_page = checkpoint.get(

                    "current_page",

                    0

                )

                print(

                    f"\nResuming PDF from page "

                    f"{start_page + 1}/{total_pages}"

                )

        # -----------------------------------------
        # Extract Text
        # -----------------------------------------

        for page_number in range(

            start_page,

            total_pages

        ):

            try:

                page = reader.pages[

                    page_number

                ]

                content = page.extract_text()

                if content:

                    text.append(

                        content

                    )

                if job is not None and state is not None:

                    state.save_checkpoint(

                        job,

                        stage="PDF_EXTRACT",

                        current_page=page_number + 1,

                        total_pages=total_pages

                    )

                    state.update_progress(

                        job,

                        stage="PDF_EXTRACT",

                        progress=int(

                            (

                                (page_number + 1)

                                / total_pages

                            )

                            * 100

                        )

                    )

            except Exception:

                continue

        full_text = "\n".join(

            text

        )

        # -----------------------------------------
        # Metadata
        # -----------------------------------------

        title = metadata.get(

            "/Title"

        ) or pdf_path.stem

        author = metadata.get(

            "/Author",

            "Unknown"

        )

        publisher = metadata.get(

            "/Producer",

            metadata.get(

                "/Creator",

                "Unknown"

            )

        )

        description = metadata.get(

            "/Subject",

            ""

        )

        if not description:

            paragraphs = [

                p.strip()

                for p in full_text.split(

                    "\n"

                )

                if p.strip()

            ]

            if paragraphs:

                description = paragraphs[

                    0

                ][

                    :300

                ]

        creation_date = metadata.get(

            "/CreationDate",

            ""

        )

        modification_date = metadata.get(

            "/ModDate",

            ""

        )

        stat = pdf_path.stat()

        return {

            "title": title,

            "text": full_text,

            "author": author,

            "publisher": publisher,

            "description": description,

            "published_date": creation_date,

            "modified_date": modification_date,

            "page_count": total_pages,

            "file_name": pdf_path.name,

            "file_extension": pdf_path.suffix.lower(),

            "file_size": stat.st_size

        }