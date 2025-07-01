import pyautogui
import subprocess
import os
import time

# Global variable to track last folder open time
last_folder_open_time = 0  # Initialized to 0

def handle_system_actions(fingers):
    global last_folder_open_time
    current_time = time.time()

    # Open folder (Index and Pinky up) - only once every 5 seconds
    if fingers == [0, 1, 0, 0, 1]:
        if current_time - last_folder_open_time >= 5:
            if os.name == 'nt':
                subprocess.Popen('explorer')
            else:
                subprocess.Popen(['open', '.'])
            last_folder_open_time = current_time  # Update last open time

    # Simulate spacebar press (All fingers up)
    elif fingers == [1, 1, 1, 1, 1]:
        pyautogui.press('space')
        time.sleep(1)
