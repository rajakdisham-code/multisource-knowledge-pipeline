from pathlib import Path
from docx import Document


class DOCXExtractor:

    def extract(self, path):

        doc = Document(path)

        text = []

        for para in doc.paragraphs:

            if para.text.strip():

                text.append(para.text)

        return {
            "title": Path(path).stem,
            "text": "\n".join(text)
        }