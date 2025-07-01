import cv2
import numpy as np
import time
import autopy
import os
import math
import threading
import subprocess
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import pyautogui
from gesture_controller.hand_detector import handDetector
from gesture_controller.system_actions import handle_system_actions


is_tracking = True
should_exit = False
tracker_thread = None
time.sleep(1)  # Let GUI settle
def run_tracker():
    global is_tracking, should_exit
    print("[INFO] Tracker thread started")
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = autopy.screen.size()
    cap.set(3, 640)
    cap.set(4, 480)

    # Volume setup
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    minVol, maxVol = volume.GetVolumeRange()[0], volume.GetVolumeRange()[1]
    detector = handDetector(maxHands=1)
    pTime = 0
    prev_x, prev_y = 0, 0
    smoothening = 8

    while not should_exit:
        success, img = cap.read()
        if not success:
            print("[WARNING] Frame read failed")
            continue
        print("[INFO] Frame read successful")
        if not is_tracking:
            # Show paused screen
            cv2.putText(img, "Tracking Paused", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            cv2.imshow("Gesture Control", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        img = cv2.resize(img, (screen_width, screen_height))  # Resize to fit full screen
        img = detector.findHands(img)  # Finding the hand
        cv2.imshow("Gesture Control", img)
        lmlist, bbox = detector.findPosition(img)  # Getting position of hand
        print("[INFO] Landmarks found:", len(lmlist))

        if len(lmlist) != 0:
            fingers = detector.fingersUp()  # Checking if fingers are upwards
            # Change rectangle color to white for all boxes
            cv2.rectangle(img, (100, 100), (screen_width, screen_height), (255, 255, 255), 2)  # Boundary box for cursor control
            last_click_time = 0  # Initialize to 0 (no click has occurred yet)
            click_cooldown = 0.5
            
            # Cursor Control (using only index finger)
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:  # Forefinger up, others down
                x1, y1 = lmlist[8][1:]
                x2, y2 = lmlist[12][1:]
                x3 = np.interp(x1, (100, screen_width - 100), (0, screen_width))  # Map to screen size
                y3 = np.interp(y1, (100, screen_height - 100), (0, screen_height))  # Map to screen size

                curr_x = prev_x + (x3 - prev_x) / smoothening
                curr_y = prev_y + (y3 - prev_y) / smoothening

                try:
                    autopy.mouse.move(screen_width - curr_x, curr_y)
                except Exception as e:
                    print(f"[ERROR] Mouse move failed: {e}")
                cv2.circle(img, (x1, y1), 7, (255, 255, 255), cv2.FILLED)  # White color for keypoints
                prev_x, prev_y = curr_x, curr_y
            
            # Click Simulation (Index & Middle Finger Up)
            elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:  # Index & middle finger up
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 40:
                    current_time = time.time()
                    if current_time - last_click_time >= click_cooldown:  # Ensure 2 seconds have passed
                        # Perform click
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (255, 255, 255), cv2.FILLED)
                        autopy.mouse.click()  # Perform the click action
                        last_click_time = current_time  # Update click time
                        time.sleep(click_cooldown)
            
            # Volume Control (Thumb and Index Finger Up)
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                x1, y1 = lmlist[4][1], lmlist[4][2]
                x2, y2 = lmlist[8][1], lmlist[8][2]
                cv2.circle(img, (x1, y1), 15, (255, 255, 255))  # White keypoint color
                cv2.circle(img, (x2, y2), 15, (255, 255, 255))  # White keypoint color
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)  # White line for volume control
                length = math.hypot(x2 - x1, y2 - y1)  # Distance between thumb and index

                vol = np.interp(length, [15, 220], [minVol, maxVol])
                volBar = np.interp(length, [50, 220], [400, 150])
                volPer = np.interp(length, [50, 220], [0, 100])
                volume.SetMasterVolumeLevel(vol, None)

                # Draw volume bar
                cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)
                cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)
                time.sleep(0.2)
  
            # Brightness Control (Thumb and Pinky Finger Up)
            elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                x_1, y_1 = lmlist[4][1], lmlist[4][2]
                x_2, y_2 = lmlist[20][1], lmlist[20][2]
                cv2.circle(img, (x_1, y_1), 7, (255, 255, 255), cv2.FILLED)  # White circle on thumb
                cv2.circle(img, (x_2, y_2), 7, (255, 255, 255), cv2.FILLED)  # White circle on pinky
                cv2.line(img, (x_1, y_1), (x_2, y_2), (255, 255, 255), 3)  # White line connecting thumb and pinky
                L = hypot(x_2 - x_1, y_2 - y_1)  # Distance between thumb and pinky

                b_level = np.interp(L, [15, 220], [0, 100])  # Map to brightness level
                sbc.set_brightness(int(b_level))

                b_level_Bar = np.interp(L, [50, 220], [400, 150])
                b_level_per = np.interp(L, [50, 220], [0, 100])
                cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)
                cv2.rectangle(img, (50, int(b_level_Bar)), (85, 400), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, f'{int(b_level_per)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

            #Folder open gesture (Index and Pinky up)
            elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                if os.name == 'nt':  # For Windows
                    subprocess.Popen('explorer')
                elif os.name == 'posix':  # For macOS/Linux
                    subprocess.Popen(['open', '.'])  # Opens the current directory in macOS
                    time.sleep(0.5)

            # Spacebar press gesture (All fingers up)
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                pyautogui.press('space')  # Simulate space bar press
                time.sleep(1)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Gesture Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def launch():
    run_tracker()

def start_tracking():
    global is_tracking
    is_tracking = True

def pause_tracking():
    global is_tracking
    is_tracking = False

def stop_tracking():
    global should_exit, is_tracking
    should_exit = True
    is_tracking = False