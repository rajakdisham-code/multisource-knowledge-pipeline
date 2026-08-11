from typing import List


class Chunker:

    def __init__(self, chunk_size=1200):

        self.chunk_size = chunk_size

    def split(self, text: str) -> List[str]:

        words = text.split()

        chunks = []

        for i in range(0, len(words), self.chunk_size):

            chunk = " ".join(words[i:i + self.chunk_size])

            chunks.append(chunk)

        return chunks