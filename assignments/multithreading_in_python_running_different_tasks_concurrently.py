"""Multithreading in Python: Running Different Tasks Concurrently

This program compares three tasks running one after another with the same
three tasks running in separate threads.

Run: python multithreading_in_python_running_different_tasks_concurrently.py
"""

import os
import tempfile
import threading
import time


# All threads write their progress to this shared list.
results = []
results_lock = threading.Lock()
run_started_at = 0.0


def start_new_run():
    """Clear the previous log and start the timer for the next run."""
    global run_started_at

    with results_lock:
        results.clear()
        run_started_at = time.perf_counter()


def record_result(task_name, message):
    """Add a message to the shared results list without a race condition."""
    with results_lock:
        elapsed = time.perf_counter() - run_started_at
        entry = f"[{elapsed:5.2f}s] {task_name:<10} {message}"
        results.append(entry)
        print(entry)


def compute_squares(count=5, delay=0.3):
    """Calculate the sum of squares, pausing briefly at each step."""
    record_result("Compute", "started")

    total = 0
    for number in range(1, count + 1):
        total += number ** 2
        time.sleep(delay)

    record_result("Compute", f"finished; sum of squares from 1 to {count} = {total}")


def write_file(file_path, line_count=5, delay=0.2):
    """Write a few lines to a text file to represent a file I/O task."""
    record_result("FileWrite", "started")

    with open(file_path, "w", encoding="utf-8") as output_file:
        for line_number in range(1, line_count + 1):
            output_file.write(f"Line {line_number}: File task completed.\n")
            time.sleep(delay)

    record_result("FileWrite", f"finished; wrote {line_count} lines to the file")


def fake_download(file_name="report.pdf", delay=1.0):
    """Simulate the waiting time of a network download."""
    record_result("Download", f"started downloading {file_name}")
    time.sleep(delay)
    record_result("Download", f"finished downloading {file_name}")


def run_sequential(file_path):
    """Execute all three tasks one after another and return the time taken."""
    start_new_run()
    start_time = time.perf_counter()

    compute_squares()
    write_file(file_path)
    fake_download()

    return time.perf_counter() - start_time


def run_threaded(file_path):
    """Run the three tasks concurrently and wait for every thread to finish."""
    start_new_run()
    start_time = time.perf_counter()

    threads = [
        threading.Thread(
            target=compute_squares,
            args=(5,),
            kwargs={"delay": 0.3},
            name="ComputeThread",
        ),
        threading.Thread(
            target=write_file,
            args=(file_path,),
            kwargs={"line_count": 5, "delay": 0.2},
            name="FileThread",
        ),
        threading.Thread(
            target=fake_download,
            kwargs={"file_name": "data.zip", "delay": 1.0},
            name="DownloadThread",
        ),
    ]

    # Start all the threads before waiting for any one of them.
    for thread in threads:
        thread.start()

    # join() makes the main thread wait until each task is complete.
    for thread in threads:
        thread.join()

    return time.perf_counter() - start_time


def main():
    output_path = os.path.join(tempfile.gettempdir(), "threading_lab_output.txt")

    print("=" * 62)
    print("MULTITHREADING: RUNNING DIFFERENT TASKS CONCURRENTLY")
    print("=" * 62)

    print("\nA) SEQUENTIAL EXECUTION")
    sequential_time = run_sequential(output_path)

    print("\nB) THREADED EXECUTION")
    threaded_time = run_threaded(output_path)

    print("\nC) TIME COMPARISON")
    print(f"Sequential time : {sequential_time:.2f} seconds")
    print(f"Threaded time   : {threaded_time:.2f} seconds")

    if threaded_time > 0:
        print(f"Speed-up        : {sequential_time / threaded_time:.2f}x")

    print(f"Output file     : {output_path}")
    print(f"Active threads  : {threading.active_count()} (main thread after join)")

    print("\nConclusion: Threading allows waiting tasks to overlap, reducing the total")
    print("execution time for this I/O-style demonstration. For CPU-heavy Python")
    print("work, multiprocessing may be a better choice because of the GIL.")


if __name__ == "__main__":
    main()
