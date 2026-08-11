import json
import sqlite3
import threading

from pathlib import Path
from datetime import datetime


class StateManager:

    def __init__(self):

        self.lock = threading.Lock()

        self.db_dir = Path("state")

        self.db_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        self.db_path = self.db_dir / "pipeline.db"

        self.conn = sqlite3.connect(

            self.db_path,

            check_same_thread=False

        )

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self._create_table()

    # -----------------------------------------------------

    def _create_table(self):

        with self.lock:

            self.cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS jobs(

                    source TEXT PRIMARY KEY,

                    status TEXT,

                    stage TEXT,

                    progress INTEGER,

                    output_path TEXT,

                    current_page INTEGER DEFAULT 0,

                    total_pages INTEGER DEFAULT 0,

                    current_chunk INTEGER DEFAULT 0,

                    total_chunks INTEGER DEFAULT 0,

                    checkpoint TEXT,

                    retry_count INTEGER DEFAULT 0,

                    error TEXT,

                    updated_at TEXT

                )
                """

            )

            self.conn.commit()

    # -----------------------------------------------------

    def is_completed(

        self,

        source

    ):

        with self.lock:

            self.cursor.execute(

                """

                SELECT status

                FROM jobs

                WHERE source=?

                """,

                (

                    source,

                )

            )

            row = self.cursor.fetchone()

            return (

                row is not None

                and row["status"] == "COMPLETED"

            )

    # -----------------------------------------------------

    def save(

        self,

        job

    ):

        with self.lock:

            self.cursor.execute(

                """

                INSERT OR REPLACE INTO jobs(

                    source,

                    status,

                    stage,

                    progress,

                    output_path,

                    current_page,

                    total_pages,

                    current_chunk,

                    total_chunks,

                    checkpoint,

                    retry_count,

                    error,

                    updated_at

                )

                VALUES(

                    ?,?,?,?,?,?,?,?,?,?,?,?,?

                )

                """,

                (

                    job.source,

                    job.status,

                    job.stage,

                    job.progress,

                    job.output_path,

                    job.current_page,

                    job.total_pages,

                    job.current_chunk,

                    job.total_chunks,

                    job.checkpoint,

                    job.retry_count,

                    job.error,

                    datetime.now().isoformat()

                )

            )

            self.conn.commit()

        # -----------------------------------------------------

    def get(

        self,

        source

    ):

        with self.lock:

            self.cursor.execute(

                """

                SELECT *

                FROM jobs

                WHERE source=?

                """,

                (

                    source,

                )

            )

            row = self.cursor.fetchone()

            return dict(row) if row else None

    # -----------------------------------------------------

    def update_progress(

        self,

        job,

        stage,

        progress

    ):

        job.stage = stage

        job.progress = progress

        self.save(job)

    # -----------------------------------------------------

    def save_checkpoint(

        self,

        job,

        stage,

        current_page=None,

        total_pages=None,

        current_chunk=None,

        total_chunks=None,

        checkpoint=None

    ):

        job.stage = stage

        if current_page is not None:

            job.current_page = current_page

        if total_pages is not None:

            job.total_pages = total_pages

        if current_chunk is not None:

            job.current_chunk = current_chunk

        if total_chunks is not None:

            job.total_chunks = total_chunks

        if checkpoint is not None:

            job.checkpoint = json.dumps(

                checkpoint

            )

        self.save(

            job

        )

    # -----------------------------------------------------

    def load_checkpoint(

        self,

        source

    ):

        with self.lock:

            self.cursor.execute(

                """

                SELECT *

                FROM jobs

                WHERE source=?

                """,

                (

                    source,

                )

            )

            row = self.cursor.fetchone()

            if row is None:

                return None

            data = dict(

                row

            )

            if data["checkpoint"]:

                try:

                    data["checkpoint"] = json.loads(

                        data["checkpoint"]

                    )

                except Exception:

                    data["checkpoint"] = None

            return data

    # -----------------------------------------------------

    def mark_completed(

        self,

        job,

        output_path=""

    ):

        job.status = "COMPLETED"

        job.stage = "FINISHED"

        job.progress = 100

        job.output_path = output_path

        self.save(

            job

        )

    # -----------------------------------------------------

    def mark_failed(

        self,

        job,

        error=""

    ):

        job.status = "FAILED"

        job.stage = "FAILED"

        job.error = str(

            error

        )

        job.retry_count += 1

        self.save(

            job

        )

    # -----------------------------------------------------

    def mark_running(

        self,

        job

    ):

        job.status = "RUNNING"

        job.stage = "PROCESSING"

        self.save(

            job

        )

    # -----------------------------------------------------

    def close(

        self

    ):

        with self.lock:

            self.conn.close()