from src.extractor.whisper_factory import WhisperFactory
from src.utils.audio_utils import AudioUtils
from src.checkpoint.checkpoint_manager import CheckpointManager
from config.settings import WHISPER_CHUNK_MINUTES

class ChunkedWhisperTranscriber:

    def __init__(self, worker_id=None):

        self.transcriber = WhisperFactory.get(
            worker_id=worker_id
        )

        self.checkpoint = CheckpointManager()

    # ---------------------------------------------------------

    def transcribe(

        self,

        audio_path,

        job=None,

        state=None

    ):

        chunk_paths = AudioUtils.split_audio(

            audio_path,

            chunk_minutes=15

        )

        language = self.transcriber.detect_language(

            chunk_paths[0]

        )

        # -----------------------------------------------------
        # Resume previous transcript
        # -----------------------------------------------------

        if job is not None and self.checkpoint.exists(job):

            full_transcript = [

                self.checkpoint.load_transcript(job)

            ]

            full_timestamp_transcript = [

                self.checkpoint.load_timestamp(job)

            ]

        else:

            full_transcript = []

            full_timestamp_transcript = []

        CHUNK_MINUTES = WHISPER_CHUNK_MINUTES

        chunk_duration = CHUNK_MINUTES * 60

        total_chunks = len(chunk_paths)

        start_chunk = 0

        # -----------------------------------------------------
        # Resume metadata
        # -----------------------------------------------------

        if job is not None:

            metadata = self.checkpoint.load_metadata(

                job

            )

            if metadata:

                start_chunk = metadata.get(

                    "current_chunk",

                    0

                )

                print(

                    f"\nResuming from chunk "

                    f"{start_chunk + 1}/{total_chunks}"

                )

        try:

            for index in range(

                start_chunk,

                total_chunks

            ):

                chunk = chunk_paths[index]

                print(

                    f"\nProcessing chunk "

                    f"{index + 1}/{total_chunks}"

                )

                result = self.transcriber.transcribe(

                    chunk,

                    language=language

                )

                full_transcript.append(

                    result["transcript"]

                )

                offset = index * chunk_duration

                timestamp_output = []

                for line in result[

                    "timestamp_transcript"

                ].split("\n\n"):

                    if not line.strip():

                        continue

                    timestamp, text = line.split(

                        "  ",

                        1

                    )

                    h, m, s = timestamp.split(":")

                    seconds = (

                        int(h) * 3600

                        + int(m) * 60

                        + float(s)

                    )

                    seconds += offset

                    new_timestamp = (

                        self.transcriber._format_timestamp(

                            seconds

                        )

                    )

                    timestamp_output.append(

                        f"{new_timestamp}  {text}"

                    )

                full_timestamp_transcript.extend(

                    timestamp_output

                )

                # -------------------------------------------------
                # Save checkpoint
                # -------------------------------------------------

                if job is not None:

                    self.checkpoint.append_chunk(

                        job,

                        result["transcript"],

                        "\n\n".join(

                            timestamp_output

                        )

                    )

                    self.checkpoint.save_metadata(

                        job,

                        {

                            "current_chunk": index + 1,

                            "total_chunks": total_chunks,

                            "language": language

                        }

                    )

                if job is not None and state is not None:

                    state.update_progress(

                        job,

                        stage="TRANSCRIBING",

                        progress=int(

                            (

                                (index + 1)

                                / total_chunks

                            )

                            * 100

                        )

                    )

        finally:

            AudioUtils.cleanup_chunks(

                chunk_paths

            )

        # -----------------------------------------------------
        # Final transcript
        # -----------------------------------------------------

        if job is not None:

            transcript = self.checkpoint.load_transcript(

                job

            )

            timestamp = self.checkpoint.load_timestamp(

                job

            )

        else:

            transcript = "\n".join(

                full_transcript

            )

            timestamp = "\n\n".join(

                full_timestamp_transcript

            )

        return {

            "language": language,

            "transcript": transcript,

            "timestamp_transcript": timestamp

        }