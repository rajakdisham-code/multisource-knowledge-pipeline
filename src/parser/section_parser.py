import re


class SectionParser:

    SECTION_MAPPING = {
        "definition": "Definition",

        "overview": "Overview",
        "introduction": "Overview",
        "background": "Overview",

        "key components": "Key Components/Aspects",
        "components": "Key Components/Aspects",
        "key aspects": "Key Components/Aspects",
        "aspects": "Key Components/Aspects",

        "mechanism": "Mechanism/Process/Application",
        "process": "Mechanism/Process/Application",
        "application": "Mechanism/Process/Application",
        "working": "Mechanism/Process/Application",
        "how it works": "Mechanism/Process/Application",

        "examples": "Examples",
        "example": "Examples",

        "relationships": "Relationships/Connections",
        "connections": "Relationships/Connections",
        "related concepts": "Relationships/Connections",

        "important distinctions": "Important Distinctions",
        "distinctions": "Important Distinctions",
        "limitations": "Important Distinctions",

        "summary": "Summary/Key Takeaways",
        "key takeaways": "Summary/Key Takeaways",
        "conclusion": "Summary/Key Takeaways"
    }

    def parse(self, document):

        sections = {}

        current = "Overview"

        sections[current] = []

        for line in document.clean_text.split("\n"):

            line = line.strip()

            if not line:
                continue

            heading = self.normalize_heading(line)

            if heading:

                current = heading

                if current not in sections:
                    sections[current] = []

                continue

            sections[current].append(line)

        document.sections = sections

        return document

    def normalize_heading(self, line):

        key = line.lower().strip()

        return self.SECTION_MAPPING.get(key)