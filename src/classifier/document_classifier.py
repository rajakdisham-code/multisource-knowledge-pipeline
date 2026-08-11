import json


class DocumentClassifier:

    def __init__(self, llm):

        self.llm = llm

    def classify(self, text):

        prompt = f"""
You are an expert AI document classifier.

Analyze the document and return ONLY valid JSON.

Schema:

{{
    "type": "",
    "confidence": 0.0,
    "reason": ""
}}

Allowed document types:

knowledge
song
story
conversation
news
poem
code
research_paper
book
medical
legal
other

Rules:

- confidence must be between 0 and 1.
- reason should be less than 15 words.
- Return ONLY JSON.
- Never use markdown.

Document:

{text[:8000]}
"""

        response = self.llm.generate(prompt)

        try:

            data = json.loads(response)

            data.setdefault("confidence", 0.5)
            data.setdefault("reason", "")

            return data

        except Exception:

            return {
                "type": "other",
                "confidence": 0.0,
                "reason": "Invalid JSON"
            }