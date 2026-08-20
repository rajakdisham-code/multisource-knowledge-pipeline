from pathlib import Path
import re
import subprocess

from langdetect import detect

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


class TranscriptTranslator:

    def __init__(self, device=None, batch_size=16):

        self.model_name = (
            "facebook/nllb-200-distilled-600M"
        )

        self.batch_size = batch_size

        # -------------------------------------------------
        # Automatically select GPU with most free VRAM.
        # -------------------------------------------------

        if device is None and torch.cuda.is_available():

            try:

                result = subprocess.run(
                    [
                        "nvidia-smi",
                        "--query-gpu=index,memory.free",
                        "--format=csv,noheader,nounits"
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )

                candidates = []

                for line in result.stdout.strip().splitlines():

                    parts = [
                        x.strip()
                        for x in line.split(",")
                    ]

                    if len(parts) != 2:
                        continue

                    gpu_id = int(parts[0])
                    free_mb = int(parts[1])

                    # NLLB-200 distilled 600M needs
                    # considerably less than Whisper large-v3,
                    # but keep a safety margin.
                    if free_mb >= 8192:

                        candidates.append(
                            (
                                free_mb,
                                gpu_id
                            )
                        )

                if candidates:

                    # Highest free VRAM first.
                    candidates.sort(
                        reverse=True
                    )

                    free_mb, gpu_id = candidates[0]

                    device = f"cuda:{gpu_id}"

                    print(
                        f"\n[Translator] "
                        f"Selected GPU {gpu_id} "
                        f"({free_mb} MB free)"
                    )

                else:

                    print(
                        "\n[Translator] "
                        "No GPU has enough free VRAM. "
                        "Using CPU."
                    )

                    device = "cpu"

            except Exception as e:

                print(
                    f"\n[Translator] "
                    f"GPU memory detection failed: {e}"
                )

                device = "cpu"

        elif device is None:

            device = "cpu"

        self.device = torch.device(device)

        print(
            f"\nLoading translator on "
            f"{self.device}...\n"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name
        )

        self.model.to(self.device)
        self.model.eval()

        self.language_map = {

            "en": "eng_Latn",
            "hi": "hin_Deva",
            "ur": "urd_Arab",
            "ar": "arb_Arab",
            "ja": "jpn_Jpan",
            "ta": "tam_Taml",
            "te": "tel_Telu",
            "bn": "ben_Beng",
            "gu": "guj_Gujr",
            "mr": "mar_Deva",
            "pa": "pan_Guru",
            "ml": "mal_Mlym",
            "kn": "kan_Knda",
            "or": "ory_Orya",
            "as": "asm_Beng",
            "ne": "npi_Deva",
            "si": "sin_Sinh",
            "ko": "kor_Hang",
            "zh-cn": "zho_Hans",
            "zh-tw": "zho_Hant",
            "th": "tha_Thai",
            "fr": "fra_Latn",
            "de": "deu_Latn",
            "es": "spa_Latn",
            "it": "ita_Latn",
            "pt": "por_Latn",
            "ru": "rus_Cyrl"
        }

        self.timestamp_pattern = re.compile(
            r"^(\d{2}:\d{2}:\d{2}\.\d{3})\s+(.*)$"
        )

    # ------------------------------------------------

    def detect_language(self, text):

        try:
            code = detect(text)
        except Exception:
            code = "en"

        return self.language_map.get(
            code,
            "eng_Latn"
        )

    # ------------------------------------------------

    def _translate_batch(self, texts, language):

        if not texts:
            return []

        self.tokenizer.src_lang = language

        encoded = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.inference_mode():

            generated = self.model.generate(

                **encoded,

                forced_bos_token_id=(
                    self.tokenizer.convert_tokens_to_ids(
                        "eng_Latn"
                    )
                ),

                max_length=512,

                num_beams=1
            )

        return self.tokenizer.batch_decode(
            generated,
            skip_special_tokens=True
        )

    # ------------------------------------------------

    def translate_timestamp_text(self, text):

        lines = text.splitlines()

        output = [""] * len(lines)

        pending = []

        def flush_batch():

            if not pending:
                return

            language = pending[0][2]

            texts = [
                item[1]
                for item in pending
            ]

            translated = self._translate_batch(
                texts,
                language
            )

            for item, result in zip(
                pending,
                translated
            ):

                index = item[0]
                timestamp = item[3]

                output[index] = (
                    f"{timestamp}  {result}"
                )

            pending.clear()

        for index, line in enumerate(lines):

            if not line.strip():

                flush_batch()

                output[index] = ""

                continue

            match = self.timestamp_pattern.match(line)

            if match:

                timestamp = match.group(1)
                sentence = match.group(2)

            else:

                timestamp = ""
                sentence = line

            sentence = sentence.strip()

            if not sentence:
                output[index] = line
                continue

            language = self.detect_language(
                sentence
            )

            # English does not need translation.
            if language == "eng_Latn":

                flush_batch()

                if timestamp:

                    output[index] = (
                        f"{timestamp}  {sentence}"
                    )

                else:

                    output[index] = sentence

                continue

            # Keep batches language-consistent.
            if pending and language != pending[0][2]:

                flush_batch()

            pending.append(
                (
                    index,
                    sentence,
                    language,
                    timestamp
                )
            )

            if len(pending) >= self.batch_size:

                flush_batch()

        flush_batch()

        return "\n".join(output)

    # ------------------------------------------------

    def translate_text(self, text):

        paragraphs = []

        chunk = []

        count = 0

        for line in text.splitlines():

            if line.strip():

                chunk.append(line)
                count += 1

            if count >= 20:

                paragraphs.append(
                    "\n".join(chunk)
                )

                chunk = []
                count = 0

        if chunk:

            paragraphs.append(
                "\n".join(chunk)
            )

        translated = []

        for paragraph in paragraphs:

            language = self.detect_language(
                paragraph
            )

            if language == "eng_Latn":

                translated.append(
                    paragraph
                )

            else:

                result = self._translate_batch(
                    [paragraph],
                    language
                )

                translated.append(
                    result[0]
                )

        return "\n\n".join(translated)

    # ------------------------------------------------

    def translate_file(
        self,
        input_file,
        output_file
    ):

        with open(
            input_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            text = f.read()

        translated = self.translate_text(
            text
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(translated)

    # ------------------------------------------------

    def translate_timestamp_file(
        self,
        input_file,
        output_file
    ):

        with open(
            input_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            text = f.read()

        translated = (
            self.translate_timestamp_text(
                text
            )
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(translated)