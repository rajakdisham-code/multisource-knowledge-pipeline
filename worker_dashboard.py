import threading
import time
from collections import defaultdict

from rich.live import Live
from rich.table import Table
from rich.panel import Panel


worker_status = {}
lock = threading.Lock()


def update_worker(worker_id, video, status, progress=""):
    with lock:
        worker_status[worker_id] = {
            "video": video,
            "status": status,
            "progress": progress,
        }


def create_dashboard():
    table = Table.grid(expand=True, padding=(1, 1))

    workers = sorted(worker_status.keys())

    # 2 workers per row
    for i in range(0, len(workers), 2):
        row = []

        for worker_id in workers[i:i + 2]:
            data = worker_status[worker_id]

            content = (
                f"Video: {data['video']}\n"
                f"{data['progress']}\n"
                f"Status: {data['status']}"
            )

            row.append(
                Panel(
                    content,
                    title=f"Worker {worker_id}",
                    border_style="green"
                    if data["status"] == "RUNNING"
                    else "yellow",
                )
            )

        while len(row) < 2:
            row.append("")

        table.add_row(*row)

    return table


def start_monitor():
    def monitor():
        with Live(create_dashboard(), refresh_per_second=4) as live:
            while True:
                live.update(create_dashboard())
                time.sleep(0.25)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()