import threading
import time
import queue
import random

# A simple task for threads to execute
def task(task_id):
    """A sample task that simulates some work by sleeping."""
    sleep_time = random.uniform(0.5, 1.5)
    print(f"Task {task_id}: Starting execution, will sleep for {sleep_time:.2f} seconds.")
    time.sleep(sleep_time)
    print(f"Task {task_id}: Finished execution.")

# --- Scheme 1: Thread-Per-Task ---
class ThreadPerTask:
    def __init__(self):
        self.threads = []
        print("\n--- Initializing Thread-Per-Task Scheme ---")

    def submit_task(self, task_id):
        print(f"Submitting Task {task_id}: Creating a new thread.")
        # A new thread is created for each task
        thread = threading.Thread(target=task, args=(task_id,))
        self.threads.append(thread)
        thread.start()

    def wait_for_completion(self):
        """Waits for all created threads to complete."""
        for thread in self.threads:
            thread.join()
        print("--- All tasks completed in Thread-Per-Task Scheme ---\n")


# --- Scheme 2: Thread-Pool ---
class ThreadPool:
    """Manages tasks using a fixed-size pool of worker threads."""
    def __init__(self, num_threads):
        # init a fixed size of pooling
        print(f"\n--- Initializing Thread-Pool Scheme with {num_threads} threads ---")
        self.task_queue = queue.Queue()
        self.num_threads = num_threads
        self.threads = []
        self._create_workers()

    def _create_workers(self):
        for i in range(self.num_threads):
            # Worker threads are created once and reused
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.threads.append(worker)

    def _worker_loop(self):
        while True:
            try:
                # Get a task from the queue and execute it
                task_id = self.task_queue.get()
                task(task_id)
                self.task_queue.task_done()
            except queue.Empty:
                # This part is generally not reached if queue.get() blocks
                continue

    def submit_task(self, task_id):
        """Adds a task to the queue for a worker to pick up."""
        print(f"Submitting Task {task_id}: Adding to the task queue.")
        self.task_queue.put(task_id)

    def wait_for_completion(self):
        """Waits for the queue to be empty."""
        self.task_queue.join()
        print("--- All tasks completed in Thread-Pool Scheme ---")


# --- Main Demonstration ---
if __name__ == "__main__":
    NUM_TASKS = 5

    # 1. Demonstrate Thread-Per-Task
    tpt_manager = ThreadPerTask()
    for i in range(NUM_TASKS):
        tpt_manager.submit_task(i)
    tpt_manager.wait_for_completion()

    # 2. Demonstrate Thread-Pool
    POOL_SIZE = 2
    tp_manager = ThreadPool(num_threads=POOL_SIZE)
    for i in range(NUM_TASKS):
        tp_manager.submit_task(i)
    tp_manager.wait_for_completion()