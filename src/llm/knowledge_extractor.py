from src.utils.retry import RetryRunner
from src.validator.json_validator import JSONValidator
from src.postprocessor.text_postprocessor import TextPostProcessor


class KnowledgeExtractor:

    def __init__(self, formatter):

        self.formatter = formatter

        self.retry = RetryRunner()

        self.validator = JSONValidator()

        self.postprocessor = TextPostProcessor()

    def extract(self, text):

        result = self.retry.run(
            self.formatter.format,
            text
        )

        return result