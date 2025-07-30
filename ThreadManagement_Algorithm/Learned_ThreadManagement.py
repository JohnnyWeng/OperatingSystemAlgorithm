import threading
import time
import queue
import random

# A simple task for threads to execute
def task(task_id):
    sleep_time = random.uniform(0.5, 1.5)
    print(f"Task {task_id}: Starting execution, will sleep for {sleep_time:.2f} seconds.")
    time.sleep(sleep_time)
    print(f"Task {task_id}: Finished execution.")

# --- Scheme 1: Thread-Per-Task ---
class ThreadPerTask:
    def __init__(self):
        self.threads = [] # Store all created threads
        print("\n--- Initializing Thread-Per-Task Scheme ---")

    def submit_task(self, task_id):
        print(f"Submitting Task {task_id}: Creating a new thread.")
        thread = threading.Thread(target=task, args=(task_id,)) # Thread object
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
    def __init__(self, num_threads): # init
        # init a fixed size of pooling
        print(f"\n--- Initializing Thread-Pool Scheme with {num_threads} threads ---")
        # Create a queue to hold task IDs
        self.task_queue = queue.Queue()
        # Store number of worker threads
        self.num_threads = num_threads
        # List to keep worker thread references
        self.threads = []
        # Spawn the worker threads
        self._create_workers()

    def _create_workers(self):
        for i in range(self.num_threads): #Loop over Threads
            # Worker threads are created once and reused
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            # Start the thread immediately so it waits for tasks right away
            worker.start()
            # Keep a reference so we can manage or join threads later
            self.threads.append(worker)

    def _worker_loop(self):
        while True:
            try:
                # Get a task from the queue and execute it
                task_id = self.task_queue.get()
                # Execute the shared task function
                task(task_id)
                # Signal that task is done
                self.task_queue.task_done()
            except queue.Empty:
                # This part is generally not reached if queue.get() blocks
                continue

    def submit_task(self, task_id):
        print(f"Submitting Task {task_id}: Adding to the task queue.")
        # Place the task ID into the queue
        self.task_queue.put(task_id)
        print("task_queue = ", self.task_queue)

    def wait_for_completion(self):
        self.task_queue.join()
        print("--- All tasks completed in Thread-Pool Scheme ---")


# --- Main Demonstration ---
if __name__ == "__main__":
    NUM_TASKS = 5
    tpt_manager = ThreadPerTask() # Initialize per-task manager
    for i in range(NUM_TASKS):
        tpt_manager.submit_task(i) # Submit each task
    tpt_manager.wait_for_completion() # Wait for all finishes
    POOL_SIZE = 2
    tp_manager = ThreadPool(num_threads=POOL_SIZE) # Initialize pool manager
    for i in range(NUM_TASKS):
        tp_manager.submit_task(i)  # Queue tasks
    tp_manager.wait_for_completion() # Wait for pool to finish