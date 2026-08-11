import re
import unicodedata
import json


class TextCleaner:

    def clean(self, document):

        text = document.clean_text

        # -------------------------------------------------
        # Ensure text is a string
        # -------------------------------------------------

        if text is None:

            text = ""

        elif isinstance(text, dict):

            text = json.dumps(
                text,
                ensure_ascii=False,
                indent=2
            )

        elif not isinstance(text, str):

            text = str(text)

        # -------------------------------------------------
        # Unicode Normalization
        # -------------------------------------------------

        text = unicodedata.normalize(
            "NFKC",
            text
        )

        # -------------------------------------------------
        # Line Endings
        # -------------------------------------------------

        text = text.replace(
            "\r\n",
            "\n"
        ).replace(
            "\r",
            "\n"
        )

        # -------------------------------------------------
        # Remove Zero Width Characters
        # -------------------------------------------------

        text = re.sub(
            r"[\u200B-\u200D\uFEFF]",
            "",
            text
        )

        # -------------------------------------------------
        # Replace Tabs
        # -------------------------------------------------

        text = text.replace(
            "\t",
            " "
        )

        # -------------------------------------------------
        # Remove Markdown Tables
        # -------------------------------------------------

        text = re.sub(
            r"^\|.*\|$",
            "",
            text,
            flags=re.MULTILINE
        )

        # -------------------------------------------------
        # Remove Horizontal Rules
        # -------------------------------------------------

        text = re.sub(
            r"^[-=_]{3,}$",
            "",
            text,
            flags=re.MULTILINE
        )

        # -------------------------------------------------
        # Remove Page Numbers
        # -------------------------------------------------

        text = re.sub(
            r"^\s*Page\s+\d+\s*$",
            "",
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        text = re.sub(
            r"^\s*\d+\s*$",
            "",
            text,
            flags=re.MULTILINE
        )

        # -------------------------------------------------
        # OCR Hyphenated Words
        # -------------------------------------------------

        text = re.sub(
            r"(\w)-\n(\w)",
            r"\1\2",
            text
        )

        # -------------------------------------------------
        # Split camelCase
        # -------------------------------------------------

        text = re.sub(
            r"([a-z])([A-Z])",
            r"\1 \2",
            text
        )

        # -------------------------------------------------
        # Normalize Quotes
        # -------------------------------------------------

        replacements = {

            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "–": "-",
            "—": "-",
            "…": "..."

        }

        for old, new in replacements.items():

            text = text.replace(
                old,
                new
            )

        # -------------------------------------------------
        # Remove Multiple Spaces
        # -------------------------------------------------

        text = re.sub(
            r"[ ]{2,}",
            " ",
            text
        )

        # -------------------------------------------------
        # Remove Spaces Around Newline
        # -------------------------------------------------

        text = re.sub(
            r" *\n *",
            "\n",
            text
        )

        # -------------------------------------------------
        # Maximum Two Blank Lines
        # -------------------------------------------------

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        # -------------------------------------------------
        # Remove Duplicate Empty Lines
        # -------------------------------------------------

        lines = []

        previous_blank = False

        for line in text.split("\n"):

            line = line.rstrip()

            if line:

                lines.append(line)
                previous_blank = False

            else:

                if not previous_blank:

                    lines.append("")
                    previous_blank = True

        document.clean_text = "\n".join(lines).strip()

        return document