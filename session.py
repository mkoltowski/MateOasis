import tkinter as tk

session_seconds = 0
timer_running = False

def start_session(label, timer_label, root):
    global session_seconds, timer_running
    label.config(text="Sesja w toku...")
    session_seconds = 1 * 2
    timer_running = True
    countdown(label, timer_label, root)

def countdown(label, timer_label, root):
    global session_seconds, timer_running
    if session_seconds > 0 and timer_running:
        minutes = session_seconds // 60
        seconds = session_seconds % 60
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        session_seconds -= 1
        root.after(1000, lambda: countdown(label, timer_label, root))
    else:
        if timer_running:
            label.config(text="Sesja zakończona.")
            timer_label.config(text="00:00")
            timer_running = False

def end_session(label, timer_label):
    global timer_running
    timer_running = False
    label.config(text="Sesja zakończona.")
    timer_label.config(text="--:--")
