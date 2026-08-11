from config.settings import WHISPER_DEVICE

from src.extractor.whisper_transcriber import WhisperTranscriber
from src.extractor.whisper_transcriber_gpu import GPUWhisperTranscriber


class WhisperFactory:

    _instance = None

    @classmethod
    def get(cls):

        if cls._instance is not None:

            return cls._instance

        device = WHISPER_DEVICE.lower()

        # ------------------------------------
        # Force CPU
        # ------------------------------------

        if device == "cpu":

            print("\nUsing CPU Whisper\n")

            cls._instance = WhisperTranscriber()

            return cls._instance

        # ------------------------------------
        # Force GPU
        # ------------------------------------

        if device == "gpu":

            print("\nUsing GPU Whisper\n")

            cls._instance = GPUWhisperTranscriber()

            return cls._instance

        # ------------------------------------
        # AUTO
        # ------------------------------------

        if device == "auto":

            try:

                import torch

                if torch.cuda.is_available():

                    print("\nGPU detected. Using GPU Whisper.\n")

                    cls._instance = GPUWhisperTranscriber()

                else:

                    print("\nGPU not found. Falling back to CPU.\n")

                    cls._instance = WhisperTranscriber()

            except Exception:

                print("\nUnable to detect GPU. Falling back to CPU.\n")

                cls._instance = WhisperTranscriber()

            return cls._instance

        raise ValueError(

            f"Invalid WHISPER_DEVICE : {WHISPER_DEVICE}"

        )