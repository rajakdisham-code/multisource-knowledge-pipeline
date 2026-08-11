from src.downloader.detector import SourceDetector
from src.downloader.website import WebsiteDownloader
from src.downloader.youtube import YouTubeDownloader

from src.extractor.html_extractor import HTMLExtractor
from src.extractor.whisper_factory import WhisperFactory

from src.extractor.pdf_extractor import PDFExtractor
from src.extractor.docx_extractor import DOCXExtractor
from src.extractor.txt_extractor import TXTExtractor
from src.extractor.epub_extractor import EPUBExtractor

from src.parser.document_parser import DocumentParser

from src.cleaner.text_cleaner import TextCleaner

from src.exporter.txt_export import TXTExporter
from src.exporter.json_export import JSONExporter
from src.exporter.excel_export import ExcelExporter
from src.exporter.csv_export import CSVExporter

from src.metadata.metadata_generator import MetadataGenerator
from src.metadata.metadata_validator import MetadataValidator

from src.cache.transcript_cache import TranscriptCache

from src.deduplication.duplicate_detector import DuplicateDetector

from src.utils.file_utils import safe_filename

from src.statistics.statistics import Statistics

from src.models.processing_result import ProcessingResult

from src.report.report_generator import ReportGenerator

from src.translator.translator import TranscriptTranslator

from src.utils.audio_utils import AudioUtils

from src.extractor.chunked_whisper_transcriber import ChunkedWhisperTranscriber

from worker_monitor import update_worker, start_monitor

start_monitor()

class KnowledgePipeline:

    def __init__(self, translator=None):

        self.detector = SourceDetector()

        self.document_parser = DocumentParser()
        self.cleaner = TextCleaner()

        self.txt_exporter = TXTExporter()
        self.json_exporter = JSONExporter()
        self.excel_exporter = ExcelExporter()
        self.csv_exporter = CSVExporter()

        self.metadata = MetadataGenerator()
        self.validator = MetadataValidator()

        self.transcript_cache = TranscriptCache()
        self.duplicate = DuplicateDetector()

        self.stats = Statistics()
        self.report = ReportGenerator()

        self.translator = translator

    # =====================================================

    def run(

        self,

        source,

        job=None,

        state=None,

        worker_id=None

    ):

        source_type = self.detector.detect(source)

        if source_type == "website":

            return self._website(

                source,

                job=job,

                state=state

            )

        if source_type == "youtube":

            return self._youtube(

                source,

                job=job,

                state=state,

                worker_id=worker_id

            )

        if source_type == "pdf":

            return self._pdf(

                source,

                job=job,

                state=state

            )

        if source_type == "docx":

            return self._docx(

                source,

                job=job,

                state=state

            )

        if source_type == "txt":

            return self._txt(

                source,

                job=job,

                state=state

            )

        if source_type == "epub":

            return self._epub(

                source,

                job=job,

                state=state

            )

        raise ValueError(

            f"Unsupported source type: {source_type}"

        )

    # =====================================================

    def _process_document(
        self,
        title,
        text,
        source,
        source_type,
        url="",
        author="Unknown",
        publisher="Unknown",
        description="",
        keywords="",
        canonical_url="",
        published_date="",
        modified_date="",
        file_name="",
        file_extension="",
        file_size=0,
        page_count=0,
        chapter_count=0,
        license="",
        isbn="",
        edition="",
        version="",
        duration_minutes=0.0,
        channel="",
        channel_id="",
        upload_date="",
        duration_seconds=0,
        thumbnail="",
        tags="",
        categories="",
        view_count=0,
        like_count=0,
        comment_count=0
    ):

        self.stats.add_total()

        print("\n========== BEFORE PARSE ==========")
        print("type(text):", type(text))
        print("type(title):", type(title))
        print("text preview:", str(text)[:200])
        print("=================================\n")

        document = self.document_parser.parse(
            title=title,
            source=source,
            source_type=source_type,
            text=text,
            url=url,
            author=author,
            publisher=publisher,
            description=description,
            keywords=keywords,
            canonical_url=canonical_url,
            published_date=published_date,
            modified_date=modified_date,
            file_name=file_name,
            file_extension=file_extension,
            file_size=file_size,
            page_count=page_count,
            chapter_count=chapter_count,
            license=license,
            isbn=isbn,
            edition=edition,
            version=version,
            duration_minutes=duration_minutes,
            channel=channel,
            channel_id=channel_id,
            upload_date=upload_date,
            duration_seconds=duration_seconds,
            thumbnail=thumbnail,
            tags=tags,
            categories=categories,
            view_count=view_count,
            like_count=like_count,
            comment_count=comment_count
        )

        print("\n========== DOCUMENT ==========")
        print("type(document.raw_text) =", type(document.raw_text))
        print("type(document.clean_text) =", type(document.clean_text))
        print("==============================\n")

        document = self.cleaner.clean(document)

        # -------------------------------------------------
        # Duplicate Detection
        # -------------------------------------------------

        if self.duplicate.is_duplicate(
            document.clean_text
        ):

            print("\nDuplicate document detected. Skipping.\n")

            self.stats.add_duplicate()

            self.stats.add_skipped()

            return ProcessingResult(

                status="DUPLICATE",

                duplicate=True

            )

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        metadata = self.metadata.generate(
            document
        )

        metadata = self.validator.validate(
            metadata
        )

        self.report.add(
            metadata
        )

        document.metadata = metadata

        # -------------------------------------------------
        # Export TXT
        # -------------------------------------------------

        txt_path = self.txt_exporter.export(
            document
        )

        self.duplicate.add(
            document.clean_text
        )

        self.stats.add_processed()

        return ProcessingResult(

            status="SUCCESS",

            output_path=str(txt_path),

            metadata=metadata,

            duplicate=False

        )
    # =====================================================

    def _website(self, url):

        downloader = WebsiteDownloader()

        html = downloader.download(url)

        result = HTMLExtractor().extract(html)

        return self._process_document(

            title=result["title"],

            text=result["text"],

            source="Website",

            source_type="website",

            url=url,

            author=result.get("author", "Unknown"),

            publisher=result.get("publisher", "Unknown"),

            description=result.get("description", ""),

            keywords=result.get("keywords", ""),

            canonical_url=result.get("canonical_url", ""),

            published_date=result.get("published_date", ""),

            modified_date=result.get("modified_date", "")

        )

    # =====================================================

    def _youtube(

        self,

        url,

        job=None,

        state=None,

        worker_id=None

    ):

        downloader = YouTubeDownloader()

        downloader = YouTubeDownloader()

        if worker_id is not None:

            update_worker(
                worker_id,
                url.split("/")[-1][:35],
                "RUNNING",
                "Downloading..."
            )

        result = downloader.download(url)

        if worker_id is not None:

            update_worker(
                worker_id,
                result.get("title", url)[:35],
                "RUNNING",
                "Download complete"
            )

        audio = result["audio"]

        if self.transcript_cache.exists(audio):

            print("Using cached transcript...")

            self.stats.add_transcript_cache_hit()

            transcript_data = self.transcript_cache.load(
                audio
            )

        else:

            duration = AudioUtils.get_audio_duration(audio)

            if worker_id is not None:

                update_worker(
                    worker_id,
                    result.get("title", url)[:35],
                    "RUNNING",
                    "Transcription starting..."
                )

            if duration <= 15 * 60:

                transcript_data = WhisperFactory.get().transcribe(
                    audio,
                    job=job,
                    state=state
                )

            else:

                print("\nLong audio detected. Splitting into chunks...\n")

                transcriber = ChunkedWhisperTranscriber()

                transcript_data = transcriber.transcribe(

                    audio_path=audio,

                    job=job,

                    state=state

                )

            self.transcript_cache.save(

                audio,

                transcript_data

            )

            if worker_id is not None:

                update_worker(
                    worker_id,
                    result.get("title", url)[:35],
                    "RUNNING",
                    "Transcription complete"
                )

        language = transcript_data["language"]

        original_transcript = transcript_data["transcript"]

        timestamp_transcript = transcript_data["timestamp_transcript"]

        if language in ["en", "hi"]:

            english_transcript = timestamp_transcript

        else:

            english_transcript = self.translator.translate_timestamp_text(

                timestamp_transcript

            )

        print("\n========== YOUTUBE DEBUG ==========")
        print("language:", language)
        print("type(transcript_data):", type(transcript_data))
        print("type(original_transcript):", type(original_transcript))
        print("type(english_transcript):", type(english_transcript))
        print("===================================\n")

        if worker_id is not None:

            update_worker(
                worker_id,
                result.get("title", url)[:35],
                "RUNNING",
                "Processing document..."
            )
        processing_result = self._process_document(

            title=result["title"],

            text=english_transcript,

            source="YouTube",

            source_type="youtube",

            url=url,

            author=result.get("author", "Unknown"),

            publisher=result.get("publisher", "Unknown"),

            description=result.get("description", ""),

            channel=result.get("channel", ""),

            channel_id=result.get("channel_id", ""),

            upload_date=result.get("upload_date", ""),

            duration_seconds=result.get("duration_seconds", 0),

            duration_minutes=result.get("duration_seconds", 0) / 60,

            thumbnail=result.get("thumbnail", ""),

            tags=result.get("tags", ""),

            categories=result.get("categories", ""),

            view_count=result.get("view_count", 0),

            like_count=result.get("like_count", 0),

            comment_count=result.get("comment_count", 0)

        )

        if worker_id is not None:

            update_worker(
                worker_id,
                result.get("title", url)[:35],
                "DONE",
                "Completed"
            )

        return processing_result

    # =====================================================

    def _pdf(

            self,

            path,

            job=None,

            state=None

        ):

        result = PDFExtractor().extract(

            path,

            job=job,

            state=state

        )

        return self._process_document(

            title=result["title"],

            text=result["text"],

            source="PDF",

            source_type="pdf",

            author=result.get("author", "Unknown"),

            publisher=result.get("publisher", "Unknown"),

            description=result.get("description", ""),

            published_date=result.get("published_date", ""),

            modified_date=result.get("modified_date", ""),

            file_name=result.get("file_name", ""),

            file_extension=result.get("file_extension", ""),

            file_size=result.get("file_size", 0),

            page_count=result.get("page_count", 0)

        )

    # =====================================================

    def _docx(self, path):

        result = DOCXExtractor().extract(path)

        return self._process_document(

            title=result["title"],

            text=result["text"],

            source="DOCX",

            source_type="docx",

            author=result.get("author", "Unknown"),

            publisher=result.get("publisher", "Unknown"),

            description=result.get("description", ""),

            file_name=result.get("file_name", ""),

            file_extension=result.get("file_extension", ""),

            file_size=result.get("file_size", 0)

        )

    # =====================================================

    def _txt(self, path):

        result = TXTExtractor().extract(path)

        return self._process_document(

            title=result["title"],

            text=result["text"],

            source="TXT",

            source_type="txt",

            author=result.get("author", "Unknown"),

            publisher=result.get("publisher", "Unknown"),

            description=result.get("description", ""),

            file_name=result.get("file_name", ""),

            file_extension=result.get("file_extension", ""),

            file_size=result.get("file_size", 0)

        )

    # =====================================================

    def _epub(self, path , job = None , state = None):

        result = EPUBExtractor().extract(

            path,

            job=job,

            state=state

        )

        return self._process_document(

            title=result["title"],

            text=result["text"],

            source="EPUB",

            source_type="epub",

            author=result.get("author", "Unknown"),

            publisher=result.get("publisher", "Unknown"),

            description=result.get("description", ""),

            file_name=result.get("file_name", ""),

            file_extension=result.get("file_extension", ""),

            file_size=result.get("file_size", 0)

        )