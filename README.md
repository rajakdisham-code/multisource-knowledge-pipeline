# Knowledge Extraction Pipeline

A modular Python pipeline for extracting structured knowledge from multiple data sources including websites, YouTube videos, PDFs, DOCX, EPUB, and TXT documents. The pipeline automatically processes raw content into standardized knowledge representations suitable for AI applications, RAG systems, search indexing, and knowledge bases.

---

## Features

- Multi-source data extraction
  - Websites
  - YouTube videos
  - PDF documents
  - DOCX documents
  - EPUB books
  - TXT files

- Automatic source detection

- Content cleaning and preprocessing

- AI-powered document classification
  - Knowledge
  - Song
  - Story
  - News
  - Conversation
  - Others

- Knowledge extraction using Gemini

- Smart chunking for large documents

- Quality validation

- Metadata generation

- Duplicate detection

- Gemini response caching

- Transcript caching

- Batch processing

- Resume processing after interruption

- Automatic retry mechanism

- Structured TXT and JSON export

---

# Architecture

```
                    Source
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Website        YouTube       Documents
                                      │
                          PDF DOCX EPUB TXT
                       │
                       ▼
              Source Detection
                       │
                       ▼
                 Downloader
                       │
                       ▼
                Text Extraction
                       │
                       ▼
               Text Cleaning
                       │
                       ▼
            Duplicate Detection
                       │
                       ▼
               Gemini Cache
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
           TXT + JSON Export
```

---

# Project Structure

```
KnowledgePipeline/

├── input/
├── raw/
│   ├── website/
│   └── youtube/
│
├── processed/
├── metadata/
├── cache/
├── logs/
│
├── main.py
├── requirements.txt
├── .env
│
└── src/
    ├── downloader/
    ├── extractor/
    ├── parser/
    ├── cleaner/
    ├── llm/
    ├── exporter/
    ├── validator/
    ├── metadata/
    ├── cache/
    ├── deduplication/
    ├── statistics/
    ├── utils/
    └── pipeline.py
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/knowledge-extraction-pipeline.git

cd knowledge-extraction-pipeline
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

# Usage

Add your sources inside the input file.

Example

```
https://en.wikipedia.org/wiki/Ayurveda

https://www.geeksforgeeks.org/deep-learning/adam-optimizer/

C:\Books\MachineLearning.pdf

https://youtu.be/example
```

Run

```bash
python main.py
```

---

# Output

The pipeline generates

```
processed/

Knowledge.txt
AI.txt
Ayurveda.txt
```

Metadata

```
metadata/

Knowledge.json
AI.json
Ayurveda.json
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

# Technologies Used

- Python
- Google Gemini API
- Whisper
- BeautifulSoup
- yt-dlp
- PyMuPDF
- python-docx
- EbookLib

---

# Pipeline Features

 Website Extraction

 YouTube Transcription

 PDF Parsing

 DOCX Parsing

 EPUB Parsing

 TXT Parsing

 Smart Chunking

 Knowledge Extraction

 Document Classification

 Duplicate Detection

 Transcript Cache

 Gemini Cache

 Metadata Generation

 Quality Validation

 Automatic Retry

 Batch Processing

 Resume Processing

---

# Applications

- AI Knowledge Bases

- Retrieval-Augmented Generation (RAG)

- Enterprise Knowledge Management

- Semantic Search

- Educational Content Processing

- Dataset Generation

- Document Intelligence

---

# Future Improvements

- OCR for scanned PDFs

- Semantic duplicate detection

- Additional LLM providers

- Cloud storage integration

- Parallel processing

---

# License

This project is licensed under the MIT License.

---

# Author

**Disham Rajak**

B.Tech Environmental Science & Engineering  
Indian Institute of Technology Bombay

GitHub: https://github.com/rajakdisham-code