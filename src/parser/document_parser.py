from src.models.document import Document


class DocumentParser:

    def parse(
        self,
        title,
        source,
        source_type,
        text,
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
        channel="",
        channel_id="",
        upload_date="",
        duration_seconds=0,
        duration_minutes=0.0,
        thumbnail="",
        tags="",
        categories="",
        view_count=0,
        like_count=0,
        comment_count=0
    ):

        title = self.clean_title(title)

        return Document(

            title=title,

            source=source,

            source_type=source_type,

            raw_text=text,

            clean_text=text,

            author=author,

            publisher=publisher,

            url=url,

            canonical_url=canonical_url,

            description=description,

            keywords=keywords,

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

            channel=channel,

            channel_id=channel_id,

            upload_date=upload_date,

            duration_seconds=duration_seconds,

            duration_minutes=duration_minutes,

            thumbnail=thumbnail,

            tags=tags,

            categories=categories,

            view_count=view_count,

            like_count=like_count,

            comment_count=comment_count

        )

    # --------------------------------------------------

    def clean_title(self, title):

        if not title:

            return "Untitled"

        title = title.strip()

        suffixes = [

            " - Wikipedia",
            " | Wikipedia",

            " - YouTube",
            " | YouTube",

            " - Google Books",
            " | Google Books",

            " - Britannica",
            " | Britannica",

            " - Wiktionary",
            " | Wiktionary",

            " - Wikibooks",
            " | Wikibooks",

            " - Encyclopedia",
            " | Encyclopedia"

        ]

        for suffix in suffixes:

            if title.endswith(suffix):

                title = title[:-len(suffix)].strip()

        return title