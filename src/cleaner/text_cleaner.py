import re


class TextCleaner:

    def clean(self, document):

        text = document.clean_text

        text = text.replace("\r\n", "\n")

        text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)

        text = re.sub(r'^-+$', '', text, flags=re.MULTILINE)

        text = re.sub(r'[ \t]+', ' ', text)

        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

        text = re.sub(r'\n{3,}', '\n\n', text)

        text = re.sub(r' *\n *', '\n', text)

        document.clean_text = text.strip()

        return document