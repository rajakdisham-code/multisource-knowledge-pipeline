import threading

import torch

from config.settings import WHISPER_DEVICE

from src.extractor.whisper_transcriber import WhisperTranscriber
from src.extractor.whisper_transcriber_gpu import GPUWhisperTranscriber


class WhisperFactory:

    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get(cls, worker_id=None):

        if cls._instance is not None:
            return cls._instance

        device = WHISPER_DEVICE.lower()

        # -------------------------------------------------
        # CPU
        # -------------------------------------------------

        if device == "cpu":

            with cls._lock:

                if cls._instance is None:

                    print(
                        "\nUsing CPU Whisper\n"
                    )

                    cls._instance = WhisperTranscriber()

            return cls._instance

        # -------------------------------------------------
        # GPU / AUTO
        # -------------------------------------------------

        if device in ("gpu", "auto"):

            if not torch.cuda.is_available():

                if device == "gpu":

                    raise RuntimeError(
                        "WHISPER_DEVICE='gpu' but CUDA is not available."
                    )

                print(
                    "\nGPU not found. Falling back to CPU.\n"
                )

                with cls._lock:

                    if cls._instance is None:
                        cls._instance = WhisperTranscriber()

                return cls._instance

            with cls._lock:

                if cls._instance is None:

                    gpu_count = torch.cuda.device_count()

                    print(
                        f"\nCUDA available: "
                        f"{gpu_count} GPU(s)\n"
                    )

                    cls._instance = (
                        GPUWhisperTranscriber(
                            gpu_count=gpu_count
                        )
                    )

            return cls._instance

        raise ValueError(
            f"Invalid WHISPER_DEVICE : {WHISPER_DEVICE}"
        )