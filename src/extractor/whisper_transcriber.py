from faster_whisper import WhisperModel


class WhisperTranscriber:

    def __init__(self):

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(
            audio_path
        )

        text = []

        for segment in segments:

            text.append(
                segment.text.strip()
            )

        return "\n".join(text)