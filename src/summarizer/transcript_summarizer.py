import re
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)


class TranscriptSummarizer:

    _tokenizer = None
    _model = None

    # -----------------------------------------------------

    @classmethod
    def _load_model(cls):

        if cls._model is None:

            print("Loading FLAN-T5 Base summarizer...")

            cls._tokenizer = AutoTokenizer.from_pretrained(
                "google/flan-t5-base"
            )

            cls._model = AutoModelForSeq2SeqLM.from_pretrained(
                "google/flan-t5-base"
            )

            cls._model.eval()

            print("✓ Summarizer Loaded\n")

    # -----------------------------------------------------

    @staticmethod
    def _clean_transcript(text):

        # Remove timestamps like 00:00:00.000
        text = re.sub(
            r"\d{2}:\d{2}:\d{2}\.\d{3}\s+",
            "",
            text
        )

        # Remove empty lines
        text = re.sub(
            r"\n\s*\n",
            "\n",
            text
        )

        # Collapse multiple spaces
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        return text.strip()


    # -----------------------------------------------------

        # -----------------------------------------------------

    @classmethod
    def _summarize_chunk(
        cls,
        text,
        max_input_tokens=512
    ):

        prompt = (
            "Write a metadata description for the following "
            "lecture or transcript.\n\n"

            "Rules:\n"
            "- Write exactly 3 concise sentences.\n"
            "- Describe the lecture objectively.\n"
            "- Mention only the important topics.\n"
            "- Do NOT copy sentences.\n"
            "- Do NOT give advice.\n"
            "- Write like metadata for a digital library.\n\n"

            "Transcript:\n\n"

            + text
        )

        inputs = cls._tokenizer(

            prompt,

            return_tensors="pt",

            truncation=True,

            max_length=max_input_tokens

        )

        with torch.no_grad():

            outputs = cls._model.generate(

                **inputs,

                max_new_tokens=90,

                min_new_tokens=35,

                num_beams=5,

                no_repeat_ngram_size=3,

                repetition_penalty=1.3,

                length_penalty=1.2,

                early_stopping=True

            )

        return cls._tokenizer.decode(

            outputs[0],

            skip_special_tokens=True

        ).strip()

    # -----------------------------------------------------

    @classmethod
    def _split_into_chunks(
        cls,
        text,
        chunk_tokens=350,
        overlap=40
    ):

        token_ids = cls._tokenizer.encode(
            text,
            add_special_tokens=False
        )

        chunks = []

        start = 0

        while start < len(token_ids):

            end = min(
                start + chunk_tokens,
                len(token_ids)
            )

            chunk = cls._tokenizer.decode(
                token_ids[start:end],
                skip_special_tokens=True
            )

            chunks.append(chunk)

            if end == len(token_ids):
                break

            start = end - overlap

        return chunks
    
    # ----------------------------------------------------

    @classmethod
    def summarize(
        cls,
        text
    ):

        text = cls._clean_transcript(text)

        if not text:
            return ""

        cls._load_model()

        chunks = cls._split_into_chunks(text)

        print(f"Transcript split into {len(chunks)} chunk(s)")

        chunk_summaries = []

        for i, chunk in enumerate(chunks, start=1):

            print(
                f"Summarizing chunk "
                f"{i}/{len(chunks)}..."
            )

            summary = cls._summarize_chunk(chunk)

            chunk_summaries.append(summary)

        # --------------------------------------------
        # If only one chunk, we're done
        # --------------------------------------------

        if len(chunk_summaries) == 1:

            return chunk_summaries[0]

        # --------------------------------------------
        # Merge chunk summaries
        # --------------------------------------------

        merged_summary = "\n".join(
            chunk_summaries
        )

        merged_chunks = cls._split_into_chunks(
            merged_summary,
            chunk_tokens=250,
            overlap=30
        )

        print(
            "\nGenerating final summary..."
        )

        if len(merged_chunks) == 1:

            return cls._summarize_chunk(
                merged_chunks[0]
            )

        final_parts = []

        for chunk in merged_chunks:

            final_parts.append(
                cls._summarize_chunk(chunk)
            )

        return " ".join(final_parts)