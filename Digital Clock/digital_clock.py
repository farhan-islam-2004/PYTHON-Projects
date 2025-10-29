import tkinter as tk
from time import strftime
import threading
import time
import pygame
import os
from datetime import datetime, timedelta

# Global states
sound_enabled = True
alarm = None
repeat_enabled = False

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    sound_btn.config(text="🔊 Sound: ON" if sound_enabled else "🔇 Sound: OFF")

def play_alarm(filename):
    if not sound_enabled:
        return
    full_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(full_path):
        print(f"Sound file not found: {full_path}")
        return
    try:
        print("Playing sound:", full_path)
        pygame.mixer.init()
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)


def toggle_repeat():
    global repeat_enabled
    repeat_enabled = not repeat_enabled
    repeat_btn.config(text="Repeat: ON" if repeat_enabled else "Repeat: OFF")

def update_alarm_display():
    print("Updating alarm display. Current alarm:", alarm)
    if alarm:
        alarm_list_label.config(text=f"{alarm['time']} → {alarm['label']}")
    else:
        alarm_list_label.config(text="No active alarm")

alarm_triggered = False
def snooze_alarm():
    global alarm
    if not alarm:
        return
    now = datetime.now()
    snoozed = now + timedelta(minutes=5)
    alarm["time"] = snoozed.strftime('%H:%M:%S')
    alarm_label.config(text=f"Snoozed to {alarm['time']}")
    update_alarm_display()

alarm_triggered = False
def stop_repeat():
    global repeat_enabled, alarm
    alarm = None
    repeat_enabled = False
    alarm_label.config(text="Alarm stopped")
    repeat_btn.config(text="Repeat: OFF")
    update_alarm_display()

def start_countdown():
    try:
        seconds = int(entry.get())
        threading.Thread(target=lambda: run_countdown(seconds), daemon=True).start()
    except ValueError:
        countdown_label.config(text="Enter valid seconds")

def run_countdown(seconds):
    for remaining in range(seconds, -1, -1):
        countdown_label.config(text=f"{remaining} seconds")
        time.sleep(1)
    countdown_label.config(text="Time’s up!")

def reset_countdown():
    countdown_label.config(text="")
    entry.delete(0, tk.END)

alarm_triggered = False
def update_clock():
    current_time = strftime('%H:%M:%S')
    clock_label.config(text=strftime('%H:%M:%S %p\n%d-%m-%Y'))

    if alarm and alarm["time"] == current_time:
        alarm_label.config(text=f"⏰ {alarm['label']} is ringing!")
        threading.Thread(target=play_alarm, args=("alarm.wav",), daemon=True).start()
        
    clock_label.after(1000, update_clock)


def clear_alarm():
    global alarm
    alarm = None
    update_alarm_display()

stopwatch_running = False
stopwatch_seconds = 0

def update_stopwatch():
    global stopwatch_seconds
    while stopwatch_running:
        mins, secs = divmod(stopwatch_seconds, 60)
        hrs, mins = divmod(mins, 60)
        stopwatch_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
        time.sleep(1)
        stopwatch_seconds += 1

def start_stopwatch():
    global stopwatch_running
    if not stopwatch_running:
        stopwatch_running = True
        threading.Thread(target=update_stopwatch, daemon=True).start()

def stop_stopwatch():
    global stopwatch_running
    stopwatch_running = False
    stopwatch_label.config(text="⏹️ Stopwatch stopped")

def reset_stopwatch():
    global stopwatch_seconds
    stopwatch_seconds = 0
    stopwatch_label.config(text="00:00:00")

def set_alarm():
    global alarm
    time_str = alarm_time_entry.get().strip()
    label_str = alarm_label_entry.get().strip()
    print("Time entered:", time_str)
    print("Label entered:", label_str)
    if time_str and label_str:
        alarm = {"time": time_str, "label": label_str}
        print("Alarm set:", alarm)
        alarm_label.config(text=f"Alarm set for {time_str} → {label_str}")
        update_alarm_display()
    else:
        print("Missing time or label")


# GUI setup
root = tk.Tk()
root.title("Digital Clock")
window_width = 360
window_height = 640
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="white")
root.resizable(False, False)

# Scrollable canvas
canvas = tk.Canvas(root, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def add_separator():
    tk.Frame(scrollable_frame, height=2, bd=0, relief='ridge', bg='gray').pack(fill='x', padx=20, pady=12)

# 🕒 Clock Section
tk.Label(scrollable_frame, text="🕒 Digital Clock", font=('calibri', 20, 'bold'), bg='white', fg='black').pack(pady=(8, 0))
clock_label = tk.Label(scrollable_frame, font=('calibri', 32, 'bold'), background='black', foreground='red')
clock_label.pack(pady=20)
add_separator()

# ⏳ Countdown Section
tk.Label(scrollable_frame, text="⏳ Countdown Timer", font=('calibri', 20, 'bold'), bg='white', fg='black').pack()
entry = tk.Entry(scrollable_frame, font=('calibri', 16), justify='center')
entry.pack(pady=8)
tk.Button(scrollable_frame, text="Start Countdown", font=('calibri', 12), command=start_countdown).pack(pady=4)
tk.Button(scrollable_frame, text="Reset Countdown", font=('calibri', 12), command=reset_countdown).pack(pady=4)
countdown_label = tk.Label(scrollable_frame, font=('calibri', 24, 'bold'), fg='blue', bg='white')
countdown_label.pack(pady=8)
add_separator()

# ⏱️ Stopwatch Section
tk.Label(scrollable_frame, text="⏱️ Stopwatch", font=('calibri', 20, 'bold'), bg='white', fg='black').pack()
stopwatch_label = tk.Label(scrollable_frame, text="00:00:00", font=('calibri', 24, 'bold'), fg='green', bg='white')
stopwatch_label.pack(pady=12)
tk.Button(scrollable_frame, text="Start Stopwatch", font=('calibri', 12), command=start_stopwatch).pack(pady=4)
tk.Button(scrollable_frame, text="Stop Stopwatch", font=('calibri', 12), command=stop_stopwatch).pack(pady=4)
tk.Button(scrollable_frame, text="Reset Stopwatch", font=('calibri', 12), command=reset_stopwatch).pack(pady=4)
add_separator()

# 🔔 Alarm Section
tk.Label(scrollable_frame, text="🔔 Alarm", font=('calibri', 20, 'bold'), bg='white', fg='black').pack()
tk.Label(scrollable_frame, text="Alarm Time (HH:MM:SS)", font=('calibri', 12), bg='white').pack()
alarm_time_entry = tk.Entry(scrollable_frame, font=('calibri', 16), justify='center')
alarm_time_entry.pack(pady=4)

tk.Label(scrollable_frame, text="Alarm Label (Purpose)", font=('calibri', 12), bg='white').pack()
alarm_label_entry = tk.Entry(scrollable_frame, font=('calibri', 16), justify='center')
alarm_label_entry.pack(pady=4)

tk.Button(scrollable_frame, text="Set Alarm", font=('calibri', 12), command=set_alarm).pack(pady=4)
alarm_label = tk.Label(scrollable_frame, font=('calibri', 16), fg='purple', bg='white')
alarm_label.pack(pady=4)
alarm_list_label = tk.Label(scrollable_frame, font=('calibri', 12), fg='black', bg='white', justify='left')
alarm_list_label.pack(pady=4)

# 🔁 Alarm Actions (grouped)
action_frame = tk.Frame(scrollable_frame, bg='white')
action_frame.pack(pady=8)
tk.Button(action_frame, text="Snooze 5 min", font=('calibri', 12), command=snooze_alarm).pack(side='left', padx=4)
repeat_btn = tk.Button(action_frame, text="Repeat: OFF", font=('calibri', 12), command=toggle_repeat)
repeat_btn.pack(side='left', padx=4)
tk.Button(action_frame, text="Stop Alarm", font=('calibri', 12), command=stop_repeat).pack(side='left', padx=4)

# 🔊 Sound Settings
add_separator()
tk.Label(scrollable_frame, text="🔊 Sound Settings", font=('calibri', 20, 'bold'), bg='white', fg='black').pack()
sound_btn = tk.Button(scrollable_frame, text="🔊 Sound: ON",font=('calibri', 12), command=toggle_sound)

sound_btn.pack(pady=8)

# Enable mouse wheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Start clock updates and launch app
update_clock()
root.mainloop()