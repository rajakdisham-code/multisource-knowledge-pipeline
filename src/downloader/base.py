from abc import ABC, abstractmethod


class BaseDownloader(ABC):
    """Abstract base class for all downloaders."""

    @abstractmethod
    def download(self, source: str):
        """
        Downloads the source and returns downloaded file path
        or raw content.
        """
        pass