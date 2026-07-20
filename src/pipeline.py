from src.config import Config

from src.downloader.detector import SourceDetector
from src.downloader.website import WebsiteDownloader
from src.downloader.youtube import YouTubeDownloader

from src.extractor.html_extractor import HTMLExtractor
from src.extractor.whisper_transcriber import WhisperTranscriber

from src.extractor.pdf_extractor import PDFExtractor
from src.extractor.docx_extractor import DOCXExtractor
from src.extractor.txt_extractor import TXTExtractor
from src.extractor.epub_extractor import EPUBExtractor

from src.parser.document_parser import DocumentParser
from src.parser.smart_chunker import SmartChunker
from src.parser.context_manager import ContextManager

from src.cleaner.text_cleaner import TextCleaner

from src.exporter.txt_export import TXTExporter

from src.llm.gemini import GeminiLLM
from src.llm.formatter import LLMFormatter
from src.llm.knowledge_extractor import KnowledgeExtractor

from src.validator.json_merger import JSONMerger
from src.validator.quality_checker import QualityChecker

from src.metadata.metadata_generator import MetadataGenerator
from src.exporter.json_export import JSONExporter

from src.cache.cache_manager import CacheManager
from src.cache.cache_service import CacheService

from src.cache.transcript_cache import TranscriptCache

from src.deduplication.duplicate_detector import DuplicateDetector

from src.utils.file_utils import safe_filename

from src.statistics.statistics import Statistics


class KnowledgePipeline:

    def __init__(self):

        self.config = Config()

        self.detector = SourceDetector()

        self.document_parser = DocumentParser()

        self.cleaner = TextCleaner()

        self.exporter = TXTExporter()

        self.chunker = SmartChunker()

        self.context = ContextManager()

        self.metadata = MetadataGenerator()

        self.json_exporter = JSONExporter()

        self.cache = CacheManager()

        self.transcript_cache = TranscriptCache()

        self.duplicate = DuplicateDetector()

        self.stats = Statistics()

        self.llm = GeminiLLM(
            api_key=self.config.api_key,
            model=self.config.llm_model
        )

        self.formatter = LLMFormatter(
            self.llm
        )

        self.knowledge = KnowledgeExtractor(
            self.formatter
        )

        self.cache_service = CacheService(
            self.cache,
            self.knowledge,
            self.stats
        )

        self.merger = JSONMerger()

        self.quality = QualityChecker()

    # =====================================================

    def run(self, source):

        source_type = self.detector.detect(source)

        if source_type == "website":
            return self._website(source)

        if source_type == "youtube":
            return self._youtube(source)

        if source_type == "pdf":
            return self._pdf(source)

        if source_type == "docx":
            return self._docx(source)

        if source_type == "txt":
            return self._txt(source)

        if source_type == "epub":
            return self._epub(source)

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
        url=""
    ):

        self.stats.add_total()

        document = self.document_parser.parse(
            title=title,
            source=source,
            source_type=source_type,
            text=text,
            url=url
        )

        document = self.cleaner.clean(document)

        # -----------------------------
        # Duplicate Detection
        # -----------------------------
        if self.duplicate.is_duplicate(
            document.clean_text
        ):

            print("\nDuplicate document detected. Skipping.\n")

            self.stats.add_duplicate()

            return "DUPLICATE"

        # -----------------------------
        # Gemini + Cache
        # -----------------------------
        result = self.cache_service.get(
            document.clean_text
        )

        doc_type = {
            "type": result.get("type", "unknown"),
            "confidence": result.get("confidence", 0),
            "reason": result.get("reason", "")
        }

        # Statistics
        self.stats.add_document(
            doc_type["type"]
        )

        print("\n========== DOCUMENT ==========")
        print("Type :", doc_type["type"])
        print("Confidence :", doc_type["confidence"])
        print("Reason :", doc_type["reason"])
        print("==============================\n")

        # -----------------------------
        # Skip non-knowledge documents
        # -----------------------------
        if doc_type["type"] != "knowledge":

            print("Skipping Knowledge Extraction.\n")

            self.duplicate.add(
                document.clean_text
            )

            self.stats.add_skipped()

            return self.exporter.export(document)

        # -----------------------------
        # Chunking
        # -----------------------------
        if self.context.needs_chunking(
            document.clean_text
        ):

            chunks = self.chunker.split(
                document.clean_text
            )

            outputs = []

            for i, chunk in enumerate(chunks):

                print(
                    f"Chunk {i+1}/{len(chunks)}"
                )

                outputs.append(
                    self.cache_service.get(chunk)
                )

            document.clean_text = self.merger.merge(
                outputs
            )

        else:

            knowledge_content = result.get("knowledge", "")

            document.clean_text = self.knowledge.validator.validate(
                knowledge_content
            )

        # -----------------------------
        # Quality Check
        # -----------------------------
        report = self.quality.check(
            document.clean_text
        )

        print("\nQuality Report\n")

        for k, v in report.items():

            print(f"{k:30} {v}")

        # -----------------------------
        # Export TXT
        # -----------------------------
        txt_path = self.exporter.export(document)

        # -----------------------------
        # Metadata
        # -----------------------------
        metadata = self.metadata.generate(document)

        metadata["document_type"] = doc_type["type"]
        metadata["confidence"] = doc_type["confidence"]
        metadata["reason"] = doc_type["reason"]
        metadata["pipeline_version"] = "1.1"
        metadata["llm"] = self.config.llm_model

        self.json_exporter.export(
            safe_filename(document.title),
            metadata
        )

        # -----------------------------
        # Save hash for duplicate detection
        # -----------------------------
        self.duplicate.add(
            document.clean_text
        )

        self.stats.add_processed()

        return txt_path

    # =====================================================

    def _website(self, url):

        downloader = WebsiteDownloader(stats=self.stats)

        html = downloader.download(url)

        extractor = HTMLExtractor()

        result = extractor.extract(html)

        return self._process_document(
            title=result["title"],
            text=result["text"],
            source="Website",
            source_type="website",
            url=url
        )

    # =====================================================

    def _youtube(self, url):

        downloader = YouTubeDownloader()

        result = downloader.download(url)

        audio = result["audio"]

        if self.transcript_cache.exists(audio):

            print("Using cached transcript...")

            self.stats.add_transcript_cache_hit()

            transcript = self.transcript_cache.load(audio)

        else:

            whisper = WhisperTranscriber()

            transcript = whisper.transcribe(audio)

            self.transcript_cache.save(
                audio,
                transcript
            )

        return self._process_document(
            title=result["title"],
            text=transcript,
            source="YouTube",
            source_type="youtube",
            url=url
        )

    # =====================================================

    def _pdf(self, path):

        result = PDFExtractor().extract(path)

        return self._process_document(
            title=result["title"],
            text=result["text"],
            source="PDF",
            source_type="pdf"
        )

    # =====================================================

    def _docx(self, path):

        result = DOCXExtractor().extract(path)

        return self._process_document(
            title=result["title"],
            text=result["text"],
            source="DOCX",
            source_type="docx"
        )

    # =====================================================

    def _txt(self, path):

        result = TXTExtractor().extract(path)

        return self._process_document(
            title=result["title"],
            text=result["text"],
            source="TXT",
            source_type="txt"
        )

    # =====================================================

    def _epub(self, path):

        result = EPUBExtractor().extract(path)

        return self._process_document(
            title=result["title"],
            text=result["text"],
            source="EPUB",
            source_type="epub"
        )