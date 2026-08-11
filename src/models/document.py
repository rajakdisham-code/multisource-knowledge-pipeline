from dataclasses import dataclass, field


@dataclass
class Document:

    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------

    title: str

    source: str

    source_type: str

    raw_text: str

    clean_text: str = ""

    # -------------------------------------------------
    # Language
    # -------------------------------------------------

    language: str = "Unknown"

    language_code: str = ""

    # -------------------------------------------------
    # Author Information
    # -------------------------------------------------

    author: str = "Unknown"

    publisher: str = "Unknown"

    # -------------------------------------------------
    # Source Information
    # -------------------------------------------------

    url: str = ""

    canonical_url: str = ""

    # -------------------------------------------------
    # File Information
    # -------------------------------------------------

    file_name: str = ""

    file_extension: str = ""

    file_size: int = 0

    page_count: int = 0

    chapter_count: int = 0

    # -------------------------------------------------
    # Classification
    # -------------------------------------------------

    domain: str = "Unknown"

    subdomain: str = "Unknown"

    # -------------------------------------------------
    # Content Metadata
    # -------------------------------------------------

    description: str = ""

    keywords: str = ""

    published_date: str = ""

    modified_date: str = ""

    license: str = ""

    isbn: str = ""

    edition: str = ""

    version: str = ""

    # -------------------------------------------------
    # YouTube Metadata
    # -------------------------------------------------

    channel: str = ""

    channel_id: str = ""

    upload_date: str = ""

    duration_seconds: int = 0

    duration_minutes: float = 0.0

    thumbnail: str = ""

    tags: str = ""

    categories: str = ""

    view_count: int = 0

    like_count: int = 0

    comment_count: int = 0

    # -------------------------------------------------
    # Additional Metadata
    # -------------------------------------------------

    sections: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)