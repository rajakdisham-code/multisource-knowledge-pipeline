from pathlib import Path

from docx import Document


class DOCXExtractor:

    def extract(self, path):

        path = Path(path)

        doc = Document(path)

        text = []

        for para in doc.paragraphs:

            if para.text.strip():

                text.append(
                    para.text.strip()
                )

        props = doc.core_properties

        title = props.title

        if not title:

            title = path.stem

        author = props.author

        if not author:

            author = "Unknown"

        publisher = props.company

        if not publisher:

            publisher = "Unknown"

        description = props.subject

        if not description:

            paragraphs = [

                p.strip()

                for p in text

                if p.strip()

            ]

            description = (

                paragraphs[0][:250]

                if paragraphs

                else ""

            )

        return {

            "title": title,

            "text": "\n".join(text),

            "author": author,

            "publisher": publisher,

            "description": description,

            "file_name": path.name,

            "file_extension": path.suffix,

            "file_size": path.stat().st_size

        }