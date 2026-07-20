import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    def __init__(self):

        # -----------------------------
        # API
        # -----------------------------
        self.api_key = os.getenv("GEMINI_API_KEY")

        self.llm_model = "gemini-3.5-flash"

        # -----------------------------
        # Cache
        # -----------------------------
        self.enable_cache = True

        self.enable_transcript_cache = True

        self.enable_duplicate_detection = True

        # -----------------------------
        # Processing
        # -----------------------------
        self.enable_chunking = True

        self.enable_quality_check = True

        self.enable_metadata = True

        self.enable_logging = True

        # -----------------------------
        # Retry
        # -----------------------------
        self.max_retry = 6

        self.retry_delay = 5

        # -----------------------------
        # Chunking
        # -----------------------------
        self.max_words = 12000

        self.chunk_size = 1200

        # -----------------------------
        # Output
        # -----------------------------
        self.output_directory = "processed"

        self.metadata_directory = "metadata"

        self.log_directory = "logs"