import subprocess
import threading
import time

from faster_whisper import WhisperModel


class GPUWhisperTranscriber:

    # =========================================================
    # GPU MODEL POOL
    # =========================================================

    _models = {}
    _gpu_locks = {}
    _init_lock = threading.Lock()

    # 8 GB minimum free VRAM
    MIN_FREE_VRAM_MB = 8192

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self, gpu_count=1):

        self.gpu_count = gpu_count

        print(
            "\nInitializing GPU Whisper pool..."
        )

        print(
            f"Available GPUs: {gpu_count}"
        )

    # =========================================================
    # GPU MEMORY
    # =========================================================

    def _get_gpu_memory(self):

        try:

            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=index,memory.free,memory.total",
                    "--format=csv,noheader,nounits"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            gpus = {}

            for line in result.stdout.strip().splitlines():

                parts = [
                    x.strip()
                    for x in line.split(",")
                ]

                if len(parts) != 3:
                    continue

                gpu_id = int(parts[0])
                free_mb = int(parts[1])
                total_mb = int(parts[2])

                gpus[gpu_id] = {
                    "free": free_mb,
                    "total": total_mb
                }

            return gpus

        except Exception as e:

            print(
                f"[Whisper GPU] "
                f"Unable to query GPU memory: {e}"
            )

            return {}

    # =========================================================
    # LOAD MODEL
    # =========================================================

    def _get_model(self, gpu_id):

        with self._init_lock:

            if gpu_id not in self._models:

                print(
                    f"\n[Whisper GPU {gpu_id}] "
                    f"Loading large-v3...\n"
                )

                model = WhisperModel(
                    "large-v3",
                    device="cuda",
                    device_index=gpu_id,
                    compute_type="float16"
                )

                self._models[gpu_id] = model

                print(
                    f"[Whisper GPU {gpu_id}] "
                    f"large-v3 loaded.\n"
                )

        return self._models[gpu_id]

    # =========================================================
    # ACQUIRE GPU
    # =========================================================

    def _acquire_gpu(self):

        while True:

            memory = self._get_gpu_memory()

            candidates = []

            for gpu_id in range(self.gpu_count):

                lock = self._gpu_locks.get(
                    gpu_id
                )

                # GPU already reserved by another worker.
                if (
                    lock is not None
                    and lock.locked()
                ):
                    continue

                info = memory.get(
                    gpu_id
                )

                if info is None:
                    continue

                # GPU does not have enough free VRAM.
                if (
                    info["free"]
                    < self.MIN_FREE_VRAM_MB
                ):
                    continue

                candidates.append(
                    (
                        info["free"],
                        gpu_id
                    )
                )

            if candidates:

                # Most free VRAM first.
                candidates.sort(
                    reverse=True
                )

                for _, gpu_id in candidates:

                    if gpu_id not in self._gpu_locks:

                        with self._init_lock:

                            if (
                                gpu_id
                                not in self._gpu_locks
                            ):

                                self._gpu_locks[gpu_id] = (
                                    threading.Lock()
                                )

                    lock = self._gpu_locks[
                        gpu_id
                    ]

                    if lock.acquire(
                        blocking=False
                    ):

                        # Re-check VRAM after reservation.
                        current_memory = (
                            self._get_gpu_memory()
                        )

                        current = (
                            current_memory.get(
                                gpu_id
                            )
                        )

                        if (
                            current is not None
                            and
                            current["free"]
                            >= self.MIN_FREE_VRAM_MB
                        ):

                            print(
                                f"\n[Whisper] "
                                f"Reserved GPU {gpu_id} "
                                f"({current['free']} MB free)"
                            )

                            model = self._get_model(
                                gpu_id
                            )

                            return (
                                gpu_id,
                                model,
                                lock
                            )

                        lock.release()

            print(
                "\n[Whisper] "
                "All GPUs are busy or "
                "have insufficient VRAM. "
                "Waiting..."
            )

            time.sleep(1)

    # =========================================================
    # RELEASE GPU
    # =========================================================

    def _release_gpu(
        self,
        gpu_id,
        lock
    ):

        lock.release()

        print(
            f"[Whisper] "
            f"Released GPU {gpu_id}"
        )

    # =========================================================
    # TIMESTAMP
    # =========================================================

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

    # =========================================================
    # LANGUAGE DETECTION
    # =========================================================

    def detect_language(
        self,
        audio_path
    ):

        gpu_id, model, lock = (
            self._acquire_gpu()
        )

        try:

            print(
                f"\n[Whisper] "
                f"Detecting language on GPU {gpu_id}"
            )

            _, info = model.transcribe(
                audio_path,

                beam_size=5,

                vad_filter=True,

                vad_parameters={
                    "min_silence_duration_ms": 700
                }
            )

            print(
                f"\nDetected language : "
                f"{info.language} "
                f"({info.language_probability:.2f}) "
                f"on GPU {gpu_id}"
            )

            return info.language

        finally:

            self._release_gpu(
                gpu_id,
                lock
            )

    # =========================================================
    # TRANSCRIPTION
    # =========================================================

    def transcribe(
        self,
        audio_path,
        language=None,
        job=None,
        state=None
    ):

        # -----------------------------------------------------
        # Language
        # -----------------------------------------------------

        if language is None:

            language = self.detect_language(
                audio_path
            )

        # -----------------------------------------------------
        # GPU
        # -----------------------------------------------------

        gpu_id, model, lock = (
            self._acquire_gpu()
        )

        try:

            print(
                f"\n[Whisper] "
                f"Transcribing on GPU {gpu_id}"
            )

            print(
                f"[Whisper] "
                f"Model: large-v3"
            )

            print(
                f"[Whisper] "
                f"Language: {language}"
            )

            # =================================================
            # EXACT SAME DECODING CONFIGURATION
            # THAT YOU TESTED DIRECTLY
            # =================================================

            segments, info = model.transcribe(

                audio_path,

                language=language,

                beam_size=5,

                best_of=5,

                temperature=0.0,

                condition_on_previous_text=False,

                vad_filter=True,

                vad_parameters={
                    "min_silence_duration_ms": 700
                }
            )

            # -------------------------------------------------
            # Collect output
            # -------------------------------------------------

            transcript = []

            timestamp_transcript = []

            for segment in segments:

                print(
                    f"{segment.start:.2f}s -> "
                    f"{segment.end:.2f}s | "
                    f"avg_logprob="
                    f"{segment.avg_logprob:.3f} | "
                    f"no_speech_prob="
                    f"{segment.no_speech_prob:.3f} | "
                    f"compression_ratio="
                    f"{segment.compression_ratio:.3f} | "
                    f"temperature="
                    f"{segment.temperature}"
                )

                text = segment.text.strip()

                if not text:
                    continue

                transcript.append(
                    text
                )

                timestamp = (
                    self._format_timestamp(
                        segment.start
                    )
                )

                timestamp_transcript.append(
                    f"{timestamp}  {text}"
                )

            # -------------------------------------------------
            # Debug output
            # -------------------------------------------------

            print(
                "\n========== ORIGINAL TRANSCRIPT ==========\n"
            )

            print(
                "\n".join(
                    transcript
                )[:2000]
            )

            print(
                "\n=========================================\n"
            )

            # -------------------------------------------------
            # Return
            # -------------------------------------------------

            return {

                "language": info.language,

                "transcript": "\n".join(
                    transcript
                ),

                "timestamp_transcript": (
                    "\n\n".join(
                        timestamp_transcript
                    )
                )

            }

        finally:

            self._release_gpu(
                gpu_id,
                lock
            )