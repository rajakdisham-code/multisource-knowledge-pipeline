from dataclasses import dataclass, field


@dataclass
class Document:

    title: str

    source: str

    source_type: str

    raw_text: str

    clean_text: str = ""

    language: str = "unknown"

    author: str = ""

    url: str = ""

    sections: dict = field(default_factory=dict)
    
    metadata: dict = field(default_factory=dict)