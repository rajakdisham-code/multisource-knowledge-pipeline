from threading import Lock

from faster_whisper import WhisperModel


class GPUWhisperTranscriber:

    _model = None

    _lock = Lock()

    # -------------------------------------------------

    def __init__(self):

        if GPUWhisperTranscriber._model is None:

            with GPUWhisperTranscriber._lock:

                if GPUWhisperTranscriber._model is None:

                    print("\nLoading GPU Whisper Model...\n")

                    GPUWhisperTranscriber._model = WhisperModel(

                        "medium",

                        device="cuda",

                        compute_type="float16"

                    )

        self.model = GPUWhisperTranscriber._model

    # -------------------------------------------------

    def _format_timestamp(

        self,

        seconds

    ):

        hours = int(

            seconds // 3600

        )

        minutes = int(

            (seconds % 3600) // 60

        )

        secs = seconds % 60

        return (

            f"{hours:02d}:"

            f"{minutes:02d}:"

            f"{secs:06.3f}"

        )

    # -------------------------------------------------

    def detect_language(

        self,

        audio_path

    ):

        _, info = self.model.transcribe(

            audio_path,

            beam_size=3,

            vad_filter=True

        )

        print(

            f"\nDetected language : "

            f"{info.language} "

            f"({info.language_probability:.2f})"

        )

        return info.language

    # -------------------------------------------------

    def transcribe(
        self,
        audio_path,
        language=None,
        job=None,
        state=None
    ):

        if language is None:
            language = self.detect_language(audio_path)

        segments, _ = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            best_of=5,
            temperature=0.0,
            condition_on_previous_text=True,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500
            )
        )

        transcript = []
        timestamp_transcript = []

        for segment in segments:

            print(
                f"{segment.start:.2f}s -> "
                f"{segment.end:.2f}s"
            )

            text = segment.text.strip()

            if not text:
                continue

            transcript.append(text)

            timestamp = self._format_timestamp(
                segment.start
            )

            timestamp_transcript.append(
                f"{timestamp}  {text}"
            )

        print(
            "\n========== ORIGINAL TRANSCRIPT ==========\n"
        )

        print(
            "\n".join(transcript)[:1000]
        )

        print(
            "\n=========================================\n"
        )

        return {
            "language": language,
            "transcript": "\n".join(transcript),
            "timestamp_transcript": "\n\n".join(
                timestamp_transcript
            )
        }