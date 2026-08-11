import re

import spacy
import yake


class KeywordExtractor:

    _nlp = None
    _extractor = None

    # -----------------------------------------------------

    @classmethod
    def _load_models(cls):

        if cls._nlp is None:

            print("Loading spaCy...")

            cls._nlp = spacy.load(
                "en_core_web_sm"
            )

            print("✓ spaCy Loaded")

        if cls._extractor is None:

            print("Loading YAKE...")

            cls._extractor = yake.KeywordExtractor(

                lan="en",

                n=2,

                dedupLim=0.9,

                top=20

            )

            print("✓ YAKE Loaded\n")

    # -----------------------------------------------------

    @staticmethod
    def _clean(text):

        text = re.sub(

            r"\d{2}:\d{2}:\d{2}\.\d{3}",

            "",

            text

        )

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text[:5000]

    # -----------------------------------------------------

    @classmethod
    def extract(
        cls,
        text,
        top_n=8
    ):

        cls._load_models()

        text = cls._clean(text)

        doc = cls._nlp(text)

        noun_phrases = {

            chunk.text.strip()

            for chunk in doc.noun_chunks

            if len(chunk.text.split()) <= 3
        }

        yake_keywords = {

            kw

            for kw, score in cls._extractor.extract_keywords(
                text
            )
        }

        keywords = list(

            noun_phrases.union(
                yake_keywords
            )

        )

        keywords = [

            k

            for k in keywords

            if len(k) > 2

        ]

        keywords = sorted(keywords)

        return keywords[:top_n]