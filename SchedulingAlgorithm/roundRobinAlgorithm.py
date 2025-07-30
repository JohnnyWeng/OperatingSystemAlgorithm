from dataclasses import dataclass
from collections import deque

# Define a Process class to represent each process
@dataclass
class Process:
    id: str              # Unique identifier for the process
    burst_time: int      # Total CPU time required
    priority: int = 0    # Priority level (not used in RR, but included for consistency)
    remaining_time: int = None  # Time left to complete, initialized to burst_time

    def __post_init__(self):
        # Set remaining_time to burst_time if not specified
        if self.remaining_time is None:
            self.remaining_time = self.burst_time

# Round Robin Scheduling Algorithm
def round_robin(processes, quantum):
    queue = deque(processes)  # Use a deque for efficient queue operations
    current_time = 0         # Track the current time
    execution_order = []     # Store (process_id, start_time, end_time) tuples
    completion_times = {}    # Store when each process completes

    while queue:
        process = queue.popleft()  # Get the next process
        print("process.remaining_time = ", process.remaining_time)
        if process.remaining_time <= quantum:
            print("process.id = ", process.id)
            # Process finishes within quantum
            start_time = current_time
            end_time = current_time + process.remaining_time
            execution_order.append((process.id, start_time, end_time))
            current_time = end_time
            completion_times[process.id] = end_time
        else:
            # Process runs for quantum and is preempted
            start_time = current_time
            end_time = current_time + quantum
            execution_order.append((process.id, start_time, end_time))
            current_time = end_time
            process.remaining_time -= quantum
            queue.append(process)  # Move to end of queue

    return execution_order, completion_times

def calculate_waiting_times(processes, completion_times):
    """Calculate waiting time for each process."""
    waiting_times = {}
    for process in processes:
        # Waiting time = completion time - burst time (arrival time is 0)
        waiting_times[process.id] = completion_times[process.id] - process.burst_time
    return waiting_times

def calculate_average_waiting_time(waiting_times):
    """Compute the average waiting time."""
    total = sum(waiting_times.values())
    return total / len(waiting_times)

def print_results(execution_order, waiting_times):
    """Display the execution order and waiting times."""
    print("Execution Order (Process: Start - End):")
    for proc, start, end in execution_order:
        print(f"{proc}: {start} - {end}")
    print("\nWaiting Times:")
    for proc, wait in waiting_times.items():
        print(f"{proc}: {wait}")
    avg_wait = calculate_average_waiting_time(waiting_times)
    print(f"Average Waiting Time: {avg_wait:.2f}\n")

def create_processes():
    return [
        Process('P1', 10, 3),  # Burst time: 10, Priority: 3 (priority unused)
        Process('P2', 3, 1),   # Burst time: 3, Priority: 1
        Process('P3', 2, 4),   # Burst time: 2, Priority: 4
        Process('P4', 1, 5)    # Burst time: 1, Priority: 5
    ]

# Main execution for Round Robin
if __name__ == "__main__":
    print("Round Robin Scheduling with Quantum = 2")
    print("==========================================")
    processes = create_processes()
    execution_order, completion_times = round_robin(processes, quantum=2)
    waiting_times = calculate_waiting_times(processes, completion_times)
    print_results(execution_order, waiting_times)