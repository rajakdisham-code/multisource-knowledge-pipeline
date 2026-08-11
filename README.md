# Knowledge Extraction Pipeline

A modular, fault-tolerant Python pipeline for extracting, processing, translating, classifying, and structuring knowledge from multiple data sources.

The pipeline supports websites, YouTube videos, PDFs, DOCX, EPUB, and TXT files, and is designed for large-scale knowledge processing, AI knowledge bases, RAG systems, semantic search, dataset generation, and document intelligence.

---

## Overview

The Knowledge Extraction Pipeline converts raw heterogeneous sources into standardized, structured knowledge.

The pipeline handles the complete processing lifecycle:

```text
Source
  │
  ▼
Source Detection
  │
  ▼
Scheduling
  │
  ▼
Parallel Worker Processing
  │
  ├── Website Extraction
  ├── YouTube Download
  ├── Audio Transcription
  ├── PDF Extraction
  ├── DOCX Extraction
  ├── EPUB Extraction
  └── TXT Extraction
  │
  ▼
Text Cleaning
  │
  ▼
Duplicate Detection
  │
  ▼
Translation
  │
  ▼
Document Classification
  │
  ▼
Knowledge Extraction
  │
  ▼
Smart Chunking
  │
  ▼
Quality Validation
  │
  ▼
Metadata Generation
  │
  ▼
Structured Export
  │
  ├── TXT
  ├── JSON
  └── Reports / Statistics
```

---

# Key Features

### Multi-Source Processing

Supports:

* Websites
* YouTube videos
* PDF documents
* DOCX documents
* EPUB books
* TXT files

### Automatic Source Detection

Automatically identifies the input type and routes it to the appropriate extractor.

### Parallel Processing

Uses a worker-based architecture to process multiple independent sources concurrently.

The number of workers can be configured centrally.

### Job Scheduling

The scheduler manages:

* New jobs
* Previously completed jobs
* Failed jobs
* Resumable jobs
* Retry handling
* Duplicate URLs

### Persistent State Management

Pipeline state is maintained using SQLite.

The state system tracks job information such as:

* Source
* Status
* Progress
* Checkpoints
* Retry information
* Completion state

This allows interrupted jobs to be resumed rather than restarted from scratch.

### Checkpointing

Long-running extraction and transcription tasks support checkpoints.

This is particularly useful for:

* Long YouTube videos
* Chunked Whisper transcription
* Large documents
* EPUB processing

If processing is interrupted, the pipeline can resume from the last available checkpoint.

### YouTube Processing

YouTube videos can be:

1. Downloaded
2. Transcribed using Whisper
3. Processed in chunks for long audio
4. Translated when required
5. Cleaned
6. Converted into structured knowledge

### GPU-Based Translation

The pipeline supports local translation using:

```text
facebook/nllb-200-distilled-600M
```

Translation uses PyTorch and CUDA when available.

The translator supports multiple languages and translates content into English while preserving timestamps for timestamped transcripts.

Translation also supports batching to reduce the number of model inference calls.

### Duplicate Detection

The pipeline uses two levels of protection against repeated processing.

#### URL-Level Processing Tracking

Successfully completed sources are recorded in:

```text
processed_urls/
```

This prevents the same URL from being processed repeatedly.

The URL is converted into a deterministic hash:

```text
URL
 ↓
MD5
 ↓
processed_urls/<hash>.txt
```

Deleting the corresponding marker allows the URL to become eligible for processing again.

#### Content-Level Duplicate Detection

The pipeline also maintains:

```text
cache/duplicates.txt
```

This detects duplicate **complete documents** based on the SHA-256 hash of the cleaned document text.

This means:

```text
Same complete document → duplicate
Only some sentences shared → not a duplicate
Different documents → processed
```

This protects against cases where the same content is available from different URLs or sources.

### Intelligent Caching

The pipeline includes caching mechanisms for expensive operations, including:

* Transcript caching
* LLM/Gemini responses
* Intermediate processing results

Caching reduces unnecessary computation and API calls.

### Document Classification

Documents can be classified into categories such as:

* Knowledge
* Song
* Story
* News
* Conversation
* Others

Classification is performed automatically during processing.

### Knowledge Extraction

The pipeline uses LLM-based knowledge extraction to convert unstructured content into structured knowledge representations.

### Smart Chunking

Large documents are divided into manageable chunks before expensive processing stages.

This helps with:

* LLM context limits
* Memory usage
* Long documents
* Reliable processing

### Quality Validation

Extracted outputs are validated before being exported.

### Metadata Generation

Metadata is generated for processed documents, including information such as:

* Title
* Source
* Source type
* Document type
* Confidence
* Reason
* Word count
* Pipeline version

### Structured Export

Processed knowledge can be exported into structured formats including:

* TXT
* JSON
* CSV
* Excel

### Monitoring and Statistics

The pipeline maintains processing statistics and worker monitoring information.

Typical statistics include:

```text
Completed
Failed
Skipped
Duplicate
Resumed
Total
```

Worker monitoring provides visibility into active processing tasks.

---

# Architecture

```text
                         INPUT SOURCES
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          Websites         YouTube         Documents
                                             │
                                   ┌─────────┼─────────┐
                                   │         │         │
                                  PDF       DOCX      EPUB/TXT
             │                │                │
             └────────────────┴────────────────┘
                              │
                              ▼
                     Source Detection
                              │
                              ▼
                         Scheduler
                              │
                              ▼
                      Job Queue / Jobs
                              │
                              ▼
                    Parallel Worker Pool
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        Extraction       Transcription      Parsing
             │                │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                        Text Cleaning
                              │
                              ▼
                     Duplicate Detection
                              │
                              ▼
                       Translation
                              │
                              ▼
                    Document Classification
                              │
                              ▼
                     Knowledge Extraction
                              │
                              ▼
                       Smart Chunking
                              │
                              ▼
                      Quality Validation
                              │
                              ▼
                      Metadata Generation
                              │
                              ▼
                         Exporters
                              │
                ┌─────────────┼─────────────┐
                │             │             │
               TXT           JSON       CSV / Excel
```

---

# Project Structure

```text
KnowledgePipeline/
│
├── input/
│
├── raw/
│   ├── website/
│   └── youtube/
│
├── processed/
├── translated/
├── metadata/
├── reports/
├── logs/
├── state/
├── cache/
│   ├── checkpoints/
│   ├── json/
│   └── duplicates.txt
│
├── processed_urls/
│
├── main.py
├── requirements.txt
├── .env
│
└── src/
    │
    ├── downloader/
    │   ├── detector.py
    │   ├── website.py
    │   └── youtube.py
    │
    ├── extractor/
    │   ├── html_extractor.py
    │   ├── pdf_extractor.py
    │   ├── docx_extractor.py
    │   ├── epub_extractor.py
    │   ├── txt_extractor.py
    │   ├── whisper_transcriber.py
    │   ├── whisper_transcriber_gpu.py
    │   ├── chunked_whisper_transcriber.py
    │   └── whisper_factory.py
    │
    ├── parser/
    │   └── document_parser.py
    │
    ├── cleaner/
    │   └── text_cleaner.py
    │
    ├── llm/
    │
    ├── translator/
    │   └── translator.py
    │
    ├── classifier/
    │   └── document_classifier.py
    │
    ├── metadata/
    │   ├── metadata_generator.py
    │   └── metadata_validator.py
    │
    ├── deduplication/
    │   └── duplicate_detector.py
    │
    ├── cache/
    │   ├── cache_manager.py
    │   └── transcript_cache.py
    │
    ├── checkpoint/
    │   └── checkpoint_manager.py
    │
    ├── state/
    │   └── state_manager.py
    │
    ├── engine/
    │   ├── scheduler.py
    │   ├── worker.py
    │   └── worker_manager.py
    │
    ├── exporter/
    │   ├── txt_export.py
    │   ├── json_export.py
    │   ├── csv_export.py
    │   └── excel_export.py
    │
    ├── validator/
    │
    ├── statistics/
    │   └── statistics.py
    │
    ├── report/
    │   └── report_generator.py
    │
    ├── utils/
    │
    ├── models/
    │   ├── job.py
    │   └── processing_result.py
    │
    └── pipeline.py
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/knowledge-extraction-pipeline.git
cd knowledge-extraction-pipeline
```

Create and activate a virtual environment:

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Python Compatibility

The pipeline is currently designed to support Python 3.9+.

For Python 3.9, Python 3.10-specific type-union syntax such as:

```python
dict | None
```

should be replaced with:

```python
Optional[dict]
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

The API key is used for LLM-based processing where configured.

---

# Configuration

Pipeline configuration is centralized so that processing parameters can be modified without changing the core pipeline implementation.

Typical configuration includes:

* Maximum number of parallel workers
* Whisper configuration
* Long-audio threshold
* Translation configuration
* Retry configuration
* Processing options

---

# Input

Sources are provided through the configured input file.

Example:

```text
https://en.wikipedia.org/wiki/Ayurveda

https://www.geeksforgeeks.org/deep-learning/adam-optimizer/

C:\Books\MachineLearning.pdf

https://youtu.be/example
```

The pipeline automatically detects the source type.

---

# Running the Pipeline

From the project root:

```bash
python main.py
```

The scheduler discovers the input sources and creates jobs.

Example output:

```text
Loading Knowledge Pipeline...

Found 4 source(s).

Jobs Added : 4
Jobs Skipped : 0
Jobs Resumed : 0
```

Workers then process the jobs concurrently.

---

# Job Lifecycle

Each source follows a managed job lifecycle.

```text
NEW
 │
 ▼
QUEUED
 │
 ▼
RUNNING
 │
 ├───────────────┐
 │               │
 ▼               ▼
COMPLETED       FAILED
 │               │
 ▼               ▼
Processed       Retry
```

Completed jobs are recorded so that the same source does not need to be processed again.

Failed or interrupted jobs can be resumed according to the available state and checkpoint information.

---

# Resume and Checkpoint Processing

The pipeline maintains persistent state in:

```text
state/pipeline.db
```

Long-running processing can additionally use:

```text
cache/checkpoints/
```

This allows processing to continue after interruptions without unnecessarily repeating completed work.

---

# Parallel Processing

The pipeline uses a worker manager and job queue to process multiple sources concurrently.

The maximum worker count can be configured centrally.

For example:

```python
MAX_WORKERS = 20
```

The worker architecture separates:

* Job scheduling
* Job execution
* Pipeline processing
* State management
* Result tracking

This allows the pipeline to scale to multiple independent sources.

---

# YouTube and Long-Audio Processing

Long YouTube audio can be processed using chunked transcription.

The pipeline can:

```text
YouTube URL
     ↓
Download audio
     ↓
Detect duration
     ↓
Short audio ────────► Direct transcription
     │
     ▼
Long audio
     ↓
Split into chunks
     ↓
Transcribe chunks
     ↓
Save checkpoints
     ↓
Merge transcript
```

This reduces the risk of losing all progress if a long transcription is interrupted.

---

# Translation

The pipeline supports local neural machine translation using:

```text
facebook/nllb-200-distilled-600M
```

Translation uses:

```text
PyTorch
CUDA
Hugging Face Transformers
```

when GPU acceleration is available.

Supported source languages include multiple Indian and international languages.

For timestamped transcripts:

```text
00:01:15.000  नमस्ते, आज हम इस विषय पर चर्चा करेंगे।
```

the timestamp is preserved while the text is translated:

```text
00:01:15.000  Hello, today we will discuss this topic.
```

Translation also uses batching to reduce repeated model inference calls.

---

# Duplicate Detection

The pipeline implements two separate mechanisms.

## 1. Source-Level Duplicate Prevention

Successfully processed URLs are stored in:

```text
processed_urls/
```

Each URL is represented using a deterministic hash.

If the same URL is submitted again:

```text
URL
 ↓
processed_urls/<hash>.txt exists
 ↓
SKIP
```

Removing the corresponding marker allows that URL to become eligible for processing again.

## 2. Content-Level Duplicate Detection

The pipeline additionally stores SHA-256 hashes of processed cleaned documents in:

```text
cache/duplicates.txt
```

This detects complete-document duplicates even when they originate from different sources.

For example:

```text
Video A → Document X
Website B → Document X
```

If the complete cleaned text is identical, the second document can be identified as a duplicate.

Partial overlap does not trigger this mechanism.

---

# Caching

The pipeline uses caching to reduce repeated computation.

### Transcript Cache

Stores previously generated transcripts.

### LLM Cache

Stores responses from expensive LLM operations where applicable.

### Checkpoint Cache

Stores intermediate progress for long-running jobs.

Caching improves both processing speed and reliability.

---

# Output

Processed documents are stored under the configured output directories.

Typical outputs include:

```text
processed/

Knowledge.txt
AI.txt
Ayurveda.txt
```

Metadata:

```text
metadata/

Knowledge.json
AI.json
Ayurveda.json
```

Additional outputs may include:

```text
reports/
logs/
translated/
```

---

# Metadata Example

```json
{
    "title": "Ayurveda",
    "source": "Website",
    "source_type": "website",
    "document_type": "knowledge",
    "confidence": 0.98,
    "reason": "Educational article",
    "word_count": 8540,
    "pipeline_version": "1.1"
}
```

---

# Statistics

The pipeline maintains processing statistics such as:

```text
Completed
Failed
Skipped
Duplicate
Resumed
Total
```

A final processing summary is displayed after execution.

Example:

```text
Completed : 18
Failed    : 1
Duplicate : 2
Total     : 21
```

---

# Technologies

The pipeline is built using:

* Python
* PyTorch
* Hugging Face Transformers
* Google Gemini API
* Whisper
* yt-dlp
* BeautifulSoup
* PyMuPDF
* python-docx
* EbookLib
* SQLite
* pandas
* CUDA

---

# Applications

The pipeline can be used for:

* AI knowledge bases
* Retrieval-Augmented Generation (RAG)
* Enterprise knowledge management
* Semantic search
* Dataset generation
* Educational content processing
* Document intelligence
* Research corpus creation
* Large-scale content ingestion
* Knowledge graph preparation

---

# Design Principles

The pipeline is designed around the following principles:

### Modularity

Each processing stage is implemented as an independent component.

### Fault Tolerance

Failures in individual jobs should not stop the entire batch.

### Resumability

Long-running jobs can resume using persistent state and checkpoints.

### Scalability

Independent sources can be processed concurrently using the worker architecture.

### Reproducibility

Caching, persistent state, and deterministic source identifiers help avoid unnecessary repeated work.

### Separation of Concerns

Scheduling, extraction, processing, translation, validation, state management, and exporting are separated into independent modules.

---

# Future Improvements

Potential future improvements include:

* OCR for scanned PDFs
* Semantic duplicate detection
* Additional translation models
* Additional LLM providers
* Cloud storage integration
* Distributed worker execution
* Improved GPU scheduling
* Vector database integration
* Knowledge graph generation
* Advanced monitoring dashboard
* Web-based pipeline management interface

---

# License

This project is licensed under the MIT License.

---

# Author

**Disham Rajak**

B.Tech Environmental Science & Engineering
Indian Institute of Technology Bombay

GitHub: https://github.com/rajakdisham-code
