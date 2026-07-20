from typing import List


class SmartChunker:

    def __init__(self, max_tokens=40000):

        self.max_tokens = max_tokens

    def split(self, text: str) -> List[str]:

        words = text.split()

        approx_words = int(self.max_tokens / 1.33)

        chunks = []

        for i in range(0, len(words), approx_words):

            chunks.append(
                " ".join(
                    words[i:i + approx_words]
                )
            )

        return chunks