import psutil
import time
import keyboard  # Optional, for simulating key presses

# Set the idle threshold in seconds (4 minutes 50 seconds)
idle_threshold = 290

def get_idle_time():
    """
    Gets the system's idle time in seconds using psutil.boot_time().
    """
    return time.time() - psutil.boot_time()

def reset_timeout():
    """
    Simulates a keyboard press (Shift) using the keyboard module (optional).
    """
    # You can customize this action to keep your team status active.
    # For example, simulate a mouse movement or other activity.
    keyboard.press('shift')

def get_active_hours():
    """
    Prompts the user to enter the active hours.
    """
    active_hours_start = int(input("Enter the start hour (0-23): "))
    active_hours_end = int(input("Enter the end hour (0-23): "))
    return active_hours_start, active_hours_end

def is_within_active_hours():
    """
    Checks if the current time is within the active hours.
    """
    current_hour = time.localtime().tm_hour
    return active_hours_start <= current_hour < active_hours_end

def get_timeout():
    """
    Checks the idle time and sets the next timeout.
    """
    idle_time = get_idle_time()

    if is_within_active_hours():
        if idle_time >= idle_threshold:
            reset_timeout()
            print(f'System Idle for {idle_time:.2f} seconds. Resetting...')
            next_timeout = idle_threshold + 5
        else:
            remaining_time = idle_threshold - idle_time
            next_timeout = max(0, remaining_time)  # Ensure non-negative timeout
            print(f'... Not enough time to reset. Will check in {next_timeout:.2f} seconds.')
    else:
        print(f'Outside active hours. Will check again at {active_hours_start}:00.')

        # Sleep until the next active hour
        current_hour = time.localtime().tm_hour
        next_active_hour = active_hours_start if current_hour < active_hours_start else active_hours_end
        next_timeout = (next_active_hour - current_hour) * 3600

    time.sleep(next_timeout)  # Wait before calling get_timeout() again

# Get user input for active hours
active_hours_start, active_hours_end = get_active_hours()

# Start the process
print('Started')
get_timeout()
