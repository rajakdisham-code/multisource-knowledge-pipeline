import json

from src.llm.prompt import SYSTEM_PROMPT


class LLMFormatter:

    def __init__(self, llm):

        self.llm = llm

    def format(self, text):

        prompt = f"""

{SYSTEM_PROMPT}

DOCUMENT

{text}

"""

        response = self.llm.generate(prompt)

        return json.loads(response)