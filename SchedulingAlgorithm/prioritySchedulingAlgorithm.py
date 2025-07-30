from dataclasses import dataclass

@dataclass
class Process:
    id: str              # Unique identifier for the process
    burst_time: int      # Total CPU time required
    priority: int = 0    # Priority level (lower number = higher priority)
    remaining_time: int = None  # Not used in Priority Scheduling, but included

    def __post_init__(self):
        # Set remaining_time to burst_time if not specified (unused here)
        if self.remaining_time is None:
            self.remaining_time = self.burst_time

# Priority Scheduling Algorithm (Non-Preemptive)
def priority_scheduling(processes):
    # Sort by priority (lower number = higher priority)
    sorted_processes = sorted(processes, key=lambda p: p.priority)
    print("sorted_processes = ", sorted_processes)
    current_time = 0
    execution_order = []
    completion_times = {}

    for process in sorted_processes:
        start_time = current_time
        end_time = current_time + process.burst_time
        execution_order.append((process.id, start_time, end_time))
        current_time = end_time
        completion_times[process.id] = end_time
    print("execution_order = ", execution_order) # The order is based on the priority
    return execution_order, completion_times

# Calculate waiting times for each process
def calculate_waiting_times(processes, completion_times):
    """Calculate waiting time for each process."""
    waiting_times = {}
    for process in processes:
        waiting_times[process.id] = completion_times[process.id] - process.burst_time
    return waiting_times

# Calculate average waiting time
def calculate_average_waiting_time(waiting_times):
    """Compute the average waiting time."""
    total = sum(waiting_times.values())
    return total / len(waiting_times)

# Print execution order and waiting times
def print_results(execution_order, waiting_times):
    print("Execution Order (Process: Start - End):")
    for proc, start, end in execution_order:
        print(f"{proc}: {start} - {end}")
    print("\nWaiting Times:")
    for proc, wait in waiting_times.items():
        print(f"{proc}: {wait}")
    avg_wait = calculate_average_waiting_time(waiting_times)
    print(f"Average Waiting Time: {avg_wait:.2f}\n") # Unit

# Create sample processes
def create_processes():
    """Generate a list of sample processes."""
    return [
        Process('P1', 10, 3),  # Burst time: 10, Priority: 3 -> second execution
        Process('P2', 3, 1),   # Burst time: 3, Priority: 1 (highest) -> first execution
        Process('P3', 2, 4),   # Burst time: 2, Priority: 4 -> third execution
        Process('P4', 1, 5)    # Burst time: 1, Priority: 5 (lowest) -> forth execution
    ]

# Main execution for Priority Scheduling
if __name__ == "__main__":
    print("Priority Scheduling (Non-Preemptive)")
    print("=====================================")
    processes = create_processes()
    execution_order, completion_times = priority_scheduling(processes)
    print("completion_times =  ",  completion_times)
    waiting_times = calculate_waiting_times(processes, completion_times)
    print_results(execution_order, waiting_times)