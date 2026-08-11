from pathlib import Path

import trafilatura
from bs4 import BeautifulSoup


class HTMLExtractor:

    def __init__(self):

        self.author_tags = [
            {"name": "author"},
            {"property": "author"},
            {"property": "article:author"},
            {"name": "article:author"},
            {"name": "parsely-author"},
            {"name": "twitter:creator"},
            {"property": "og:author"}
        ]

        self.publisher_tags = [
            {"property": "og:site_name"},
            {"name": "application-name"},
            {"name": "publisher"},
            {"property": "publisher"}
        ]

        self.description_tags = [
            {"name": "description"},
            {"property": "og:description"},
            {"name": "twitter:description"}
        ]

        self.keyword_tags = [
            {"name": "keywords"},
            {"property": "article:tag"}
        ]

        self.publish_date_tags = [
            {"property": "article:published_time"},
            {"name": "publish_date"},
            {"name": "date"},
            {"itemprop": "datePublished"},
            {"property": "og:published_time"}
        ]

        self.modified_date_tags = [
            {"property": "article:modified_time"},
            {"itemprop": "dateModified"},
            {"property": "og:updated_time"}
        ]

        self.canonical_tags = [
            {"rel": "canonical"}
        ]

    # -----------------------------------------------------

    def _get_meta(self, soup, tags):

        for tag in tags:

            meta = soup.find("meta", attrs=tag)

            if meta and meta.get("content"):

                value = meta["content"].strip()

                if value:

                    return value

        return ""

    # -----------------------------------------------------

    def _get_link(self, soup, tags):

        for tag in tags:

            link = soup.find("link", attrs=tag)

            if link and link.get("href"):

                value = link["href"].strip()

                if value:

                    return value

        return ""

    # -----------------------------------------------------

    def extract(self, html_path):

        html_path = Path(html_path)

        html = html_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        # ----------------------------------
        # Title
        # ----------------------------------

        title = ""

        if soup.title:

            title = soup.title.get_text(
                strip=True
            )

        if not title:

            og_title = soup.find(
                "meta",
                property="og:title"
            )

            if og_title and og_title.get("content"):

                title = og_title["content"].strip()

        # ----------------------------------
        # Metadata
        # ----------------------------------

        author = self._get_meta(
            soup,
            self.author_tags
        ) or "Unknown"

        publisher = self._get_meta(
            soup,
            self.publisher_tags
        ) or "Unknown"

        description = self._get_meta(
            soup,
            self.description_tags
        )

        keywords = self._get_meta(
            soup,
            self.keyword_tags
        )

        published_date = self._get_meta(
            soup,
            self.publish_date_tags
        )

        modified_date = self._get_meta(
            soup,
            self.modified_date_tags
        )

        canonical_url = self._get_link(
            soup,
            self.canonical_tags
        )

        # ----------------------------------
        # Main Content
        # ----------------------------------

        text = trafilatura.extract(

            html,

            include_comments=False,

            include_tables=False,

            include_links=False,

            favor_precision=True,

            deduplicate=True

        )

        if not text:

            text = soup.get_text(

                separator="\n",

                strip=True

            )

        # ----------------------------------
        # Better Description Fallback
        # ----------------------------------

        if not description:

            paragraphs = [

                p.strip()

                for p in text.split("\n")

                if p.strip()

            ]

            if paragraphs:

                description = paragraphs[0][:300]

        return {

            "title": title,

            "text": text,

            "author": author,

            "publisher": publisher,

            "description": description,

            "keywords": keywords,

            "published_date": published_date,

            "modified_date": modified_date,

            "canonical_url": canonical_url

        }