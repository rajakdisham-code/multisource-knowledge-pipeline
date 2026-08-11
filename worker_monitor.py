import threading
import time
import os


_workers = {}
_lock = threading.Lock()
_monitor_started = False


def update_worker(worker_id, video="", status="", download="", transcription=""):
    with _lock:
        _workers[worker_id] = {
            "video": video,
            "status": status,
            "download": download,
            "transcription": transcription,
        }


def start_monitor():
    global _monitor_started

    if _monitor_started:
        return

    _monitor_started = True

    thread = threading.Thread(
        target=_monitor_loop,
        daemon=True
    )

    thread.start()


def _monitor_loop():
    while True:

        with _lock:
            workers = dict(_workers)

        os.system("clear")

        print("=" * 100)
        print("                    KNOWLEDGE PIPELINE - WORKERS")
        print("=" * 100)

        worker_ids = sorted(workers.keys())

        for i in range(0, len(worker_ids), 2):

            pair = worker_ids[i:i + 2]

            boxes = []

            for worker_id in pair:

                data = workers[worker_id]

                box = [
                    f"┌──────────── Worker {worker_id} ────────────┐",
                    f"│ Video: {data['video'][:30]:<30} │",
                    f"│ Download: {data['download'][:25]:<25} │",
                    f"│ Transcription: {data['transcription'][:20]:<20} │",
                    f"│ Status: {data['status'][:30]:<30} │",
                    "└────────────────────────────────────────────┘",
                ]

                boxes.append(box)

            for line_number in range(6):

                print("    ".join(
                    box[line_number]
                    for box in boxes
                ))

            print()

        time.sleep(0.5)
