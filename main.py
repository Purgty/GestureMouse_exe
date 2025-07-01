import sys
import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import tracker

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_instructions():
    try:
        instruction_file = resource_path("app_instructions.txt")
        with open(instruction_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "❌ Failed to load instructions:\n" + str(e)

def launch_tracker():
    tracker.run_tracker()
    root.deiconify()  # Show the main window again after tracker exits

def start():
    tracker.start_tracking()

def pause():
    tracker.pause_tracking()

def exit_app():
    tracker.stop_tracking()
    root.destroy()

root = tk.Tk()
root.title("Gesture Control Assistant")
root.geometry("600x500")
root.resizable(False, False)

# Headingq
title = tk.Label(root, text="👋 Gesture Control Assistant", font=("Helvetica", 18, "bold"))
title.pack(pady=10)

# Instruction box
instruction_label = tk.Label(root, text="Gesture Instructions", font=("Helvetica", 14, "bold"))
instruction_label.pack()

instruction_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 11))
instruction_box.pack(pady=10)
instruction_box.insert(tk.END, load_instructions())
instruction_box.configure(state='disabled')

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="▶ Launch Tracker", font=("Helvetica", 12), width=15, command=launch_tracker)
start_btn.grid(row=0, column=0, padx=10)

resume_btn = tk.Button(btn_frame, text="▶ Resume", font=("Helvetica", 12), width=15, command=tracker.start_tracking)
resume_btn.grid(row=0, column=1, padx=10)

pause_btn = tk.Button(btn_frame, text="⏸ Pause", font=("Helvetica", 12), width=15, command=tracker.pause_tracking)
pause_btn.grid(row=0, column=2, padx=10)

exit_btn = tk.Button(btn_frame, text="❌ Exit", font=("Helvetica", 12), width=15, command=tracker.stop_tracking)
exit_btn.grid(row=0, column=3, padx=10)

root.mainloop()