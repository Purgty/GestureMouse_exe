# Gesture Control Assistant

Gesture Control Assistant is a desktop application that uses real-time hand gesture recognition through a webcam to control various system-level functions such as cursor movement, volume adjustment, brightness control, folder access, and media playback.

This application is built using OpenCV, MediaPipe, Pycaw, and other Python libraries, and provides a graphical interface via Tkinter for ease of use.

<p align="center">
   <img src="https://github.com/user-attachments/assets/fe9ce960-147f-456a-ad1e-4d5fef282d92" alt="Add Contact" width="500"/>
</p>
## Features

- Cursor Control – Move the mouse using the index finger.
- Click Simulation – Simulate left-click by bringing index and middle fingers together.
- Volume Control – Adjust system volume using thumb and index finger distance.
- Brightness Control – Adjust screen brightness using thumb and pinky distance.
- Open File Explorer – Open system file explorer with a specific gesture.
- Play/Pause Media – Simulate spacebar press using five-finger gesture.
- Pause/Resume Tracking – Control gesture tracking status from GUI.
- Multithreaded Execution – Gesture tracking runs independently of the UI thread.

## Requirements

- Python 3.7 or above  
- Webcam  
- Windows OS (for full system-level control compatibility)

### Python Dependencies

Install required packages using:

```bash
pip install -r requirements.txt
```

**Key Libraries:**
- opencv-python
- mediapipe
- pycaw
- screen_brightness_control
- pyautogui
- autopy
- tkinter (comes with most Python installations)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gesture-control-assistant.git
cd gesture-control-assistant
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Use the GUI buttons:
   - Launch Tracker: Start gesture detection.
   - Resume: Resume gesture control if paused.
   - Pause: Pause gesture tracking.
   - Exit: Safely exit the application.

3. Gesture Instructions:
   - Instructions are displayed within the application’s interface.

## Folder Structure

```
gesture-control-assistant/
├── gesture_controller/
│   ├── hand_detector.py
│   ├── system_actions.py (optional)
├── tracker.py
├── main.py
├── requirements.txt
├── app_instructions.txt
└── README.md
```

## Building the Executable (Using PyInstaller)

To create a standalone `.exe` file for Windows using PyInstaller:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build the executable:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "app_instructions.txt;." main.py
```

> ⚠️ Note:
> - Use a semicolon (`;`) between file and folder when on **Windows**.
> - Use a colon (`:`) instead of semicolon if you're on **Linux/macOS** (e.g., `"file:."`).
> - The `--windowed` flag hides the console window. Remove it if you want to see logs for debugging.

3. After the build completes:
   - Navigate to the `dist` folder.
   - Run `main.exe` to launch the app.

## Notes

- Some features like brightness control may not work on systems that do not support software-based brightness adjustments.
- Cursor movement assumes a 2D desktop screen; performance may vary on multi-monitor setups.
- Gesture control requires a clear view of the hand; ensure good lighting and a clean background.

## License

This project is licensed under the MIT License. See LICENSE for more details.
