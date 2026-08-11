"""
=========================================================
Knowledge Pipeline Configuration
=========================================================
Change values here only.

No other file needs modification.
=========================================================
"""

# ------------------------------------------------------
# Parallel Processing
# ------------------------------------------------------

# Number of parallel workers.

MAX_WORKERS = 20

# ------------------------------------------------------
# Whisper
# ------------------------------------------------------

# Audio longer than this (minutes)
# will use chunked transcription.

LONG_AUDIO_THRESHOLD_MINUTES = 15

# Minutes per chunk.

WHISPER_CHUNK_MINUTES = 15

# ------------------------------------------------------
# Checkpoint
# ------------------------------------------------------

# Save checkpoint after every completed chunk.

SAVE_CHECKPOINT_EVERY_CHUNK = True

# Folder for checkpoint files.

CHECKPOINT_FOLDER = "cache/checkpoints"

# ------------------------------------------------------
# Resume / Retry
# ------------------------------------------------------

# Skip already completed jobs.

SKIP_COMPLETED = True

# Automatically retry failed jobs.

RETRY_FAILED = True

# Retry count before marking failed.

MAX_RETRIES = 3

# ------------------------------------------------------
# Logging
# ------------------------------------------------------

ENABLE_LOGGING = True

LOG_LEVEL = "INFO"

# ------------------------------------------------------
# Duplicate Detection
# ------------------------------------------------------

ENABLE_DUPLICATE_DETECTION = True

# ------------------------------------------------------
# Metadata Export
# ------------------------------------------------------

EXPORT_TXT = True

EXPORT_JSON = True

EXPORT_CSV = True

EXPORT_EXCEL = True

# ------------------------------------------------------
# Report
# ------------------------------------------------------

GENERATE_REPORT = True

# ------------------------------------------------------
# Translation
# ------------------------------------------------------

TRANSLATE_TO_ENGLISH = True

# ------------------------------------------------------
# Cache
# ------------------------------------------------------

USE_TRANSCRIPT_CACHE = True

# ------------------------------------------------------
# Thread Pool
# ------------------------------------------------------

USE_THREAD_POOL = True

# ------------------------------------------------------
# Whisper Device
# ------------------------------------------------------

WHISPER_DEVICE = "auto"

# Options:
# auto
# gpu
# cpu