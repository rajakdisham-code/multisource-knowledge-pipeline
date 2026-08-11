from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Job:

    # --------------------------------------------------
    # Source
    # --------------------------------------------------

    source: str

    source_type: str

    # --------------------------------------------------
    # Pipeline Status
    # --------------------------------------------------

    status: str = "PENDING"

    stage: str = "WAITING"

    progress: int = 0

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    output_path: str = ""

    error: str = ""

    # --------------------------------------------------
    # Resume Information
    # --------------------------------------------------

    current_page: int = 0

    total_pages: int = 0

    current_chunk: int = 0

    total_chunks: int = 0

    checkpoint: str = ""

    retry_count: int = 0

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    worker_id: int = 0

    started: bool = False

    completed: bool = False

    # --------------------------------------------------
    # Time
    # --------------------------------------------------

    created_at: str = field(

        default_factory=lambda: datetime.now().isoformat()

    )

    updated_at: str = field(

        default_factory=lambda: datetime.now().isoformat()

    )