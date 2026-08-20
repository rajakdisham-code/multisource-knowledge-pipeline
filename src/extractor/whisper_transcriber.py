from faster_whisper import WhisperModel


class WhisperTranscriber:

    def __init__(self):

        # Best model for 8 GB RAM
        self.model = WhisperModel(
            "medium",
            device="cpu",
            compute_type="int8"
        )

    # -------------------------------------------------

    def _format_timestamp(self, seconds):

        hours = int(seconds // 3600)

        minutes = int((seconds % 3600) // 60)

        secs = seconds % 60

        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

    # -------------------------------------------------

    def detect_language(self, audio_path):

        _, info = self.model.transcribe(

            audio_path,

            beam_size=3,

            vad_filter=True

        )

        print(

            f"\nDetected language : {info.language}"

            f" ({info.language_probability:.2f})"

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

        # ------------------------------------------
        # Detect language (only if not supplied)
        # ------------------------------------------

        if language is None:

            language = self.detect_language(
                audio_path
            )

        # ------------------------------------------
        # Final transcription
        # ------------------------------------------

        segments, _ = self.model.transcribe(

            audio_path,

            language=language,

            beam_size=3,

            best_of=3,

            temperature=0.0,

            condition_on_previous_text=False,

            vad_filter=True

        )

        transcript = []

        timestamp_transcript = []

        for segment in segments:

            print(
                f"{segment.start:.2f}s -> {segment.end:.2f}s"
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

        print("\n========== ORIGINAL TRANSCRIPT ==========\n")
        print("\n".join(transcript)[:1000])
        print("\n=========================================\n")

        return {

            "language": language,

            "transcript": "\n".join(transcript),

            "timestamp_transcript": "\n\n".join(
                timestamp_transcript
            )

        }