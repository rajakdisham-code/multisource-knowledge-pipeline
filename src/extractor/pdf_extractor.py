from pathlib import Path
from PyPDF2 import PdfReader


class PDFExtractor:

    def extract(self, pdf_path):

        reader = PdfReader(pdf_path)

        text = []

        for page in reader.pages:

            content = page.extract_text()

            if content:

                text.append(content)

        return {
            "title": Path(pdf_path).stem,
            "text": "\n".join(text)
        }