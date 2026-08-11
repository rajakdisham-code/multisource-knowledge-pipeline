import threading

from src.exporter.csv_export import CSVExporter
from src.exporter.excel_export import ExcelExporter
from src.exporter.json_export import JSONExporter

from src.utils.file_utils import safe_filename


class MetadataWriter:

    _instance = None

    _instance_lock = threading.Lock()

    # -----------------------------------------------------

    def __new__(cls):

        with cls._instance_lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)

        return cls._instance

    # -----------------------------------------------------

    def __init__(self):

        if hasattr(self, "_initialized"):

            return

        self.csv = CSVExporter()

        self.excel = ExcelExporter()

        self.json = JSONExporter()

        self.lock = threading.Lock()

        self._initialized = True

    # -----------------------------------------------------

    def write(

        self,

        metadata

    ):

        if not metadata:

            return

        with self.lock:

            self.csv.export(

                metadata

            )

            self.excel.export(

                metadata

            )

            self.json.export(

                safe_filename(

                    metadata["title"]

                ),

                metadata

            )