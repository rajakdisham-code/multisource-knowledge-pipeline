from dataclasses import dataclass


@dataclass
class ProcessingResult:

    status: str

    output_path: str = ""

    from typing import Optional

    metadata: Optional[dict] = None

    duplicate: bool = False

    error: str = ""