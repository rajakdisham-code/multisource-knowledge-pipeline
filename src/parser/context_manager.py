class ContextManager:

    """
    Decides whether a document needs chunking
    based on the configured model context size.
    """

    def __init__(
        self,
        model_context_tokens=50000,
        safety_margin=5000
    ):

        self.model_context_tokens = model_context_tokens
        self.safety_margin = safety_margin

    def estimate_tokens(self, text):

        # Approximation:
        # 1 token ≈ 0.75 words
        words = len(text.split())

        return int(words * 1.33)

    def needs_chunking(self, text):

        tokens = self.estimate_tokens(text)

        return tokens > (
            self.model_context_tokens -
            self.safety_margin
        )

    def available_tokens(self):

        return (
            self.model_context_tokens -
            self.safety_margin
        )