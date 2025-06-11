import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

session_seconds = 0
timer_running = False

session_data = {
    "start_time": None,
    "end_time": None,
    "session_completed": False,
    "mindfulness_completed": False
}

def start_session(label, timer_label, root):
    global session_seconds, timer_running
    label.config(text="Sesja w toku...")
    session_seconds = 25 * 60  # 25 minut
    timer_running = True
    countdown(label, timer_label, root)
    session_data["start_time"] = datetime.now().isoformat()


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
            messagebox.showinfo("MateOasis – Przerwa", "Czas na przerwę!\nWstań, oddychaj, rozluźnij się.")
            show_mindfulness_window(root)
            timer_running = False
            session_data["end_time"] = datetime.now().isoformat()
            session_data["session_completed"] = True

def end_session(label, timer_label):
    global timer_running
    timer_running = False
    label.config(text="Sesja zakończona.")
    timer_label.config(text="--:--")
    session_data["end_time"] = datetime.now().isoformat()
    session_data["session_completed"] = False
    show_mindfulness_window(timer_label.master)


def show_mindfulness_window(root):
    mindfulness = tk.Toplevel(root)
    mindfulness.title("Ćwiczenie oddechowe")
    mindfulness.geometry("300x220")

    instruction = tk.Label(mindfulness, text="Oddychaj głęboko przez 1 minutę", font=("Arial", 12), wraplength=250)
    instruction.pack(pady=10)

    timer_display = tk.Label(mindfulness, text="01:00", font=("Arial", 24))
    timer_display.pack(pady=10)

    mindfulness_seconds = 60  # lokalna zmienna

    def countdown_mindfulness():
        nonlocal mindfulness_seconds
        if mindfulness_seconds > 0:
            minutes = mindfulness_seconds // 60
            seconds = mindfulness_seconds % 60
            timer_display.config(text=f"{minutes:02d}:{seconds:02d}")
            mindfulness_seconds -= 1
            mindfulness.after(1000, countdown_mindfulness)
        else:
            instruction.config(text="Brawo! Ćwiczenie zakończone.")
            timer_display.config(text="00:00")
            session_data["mindfulness_completed"] = True
            log_session(
                session_data["start_time"],
                session_data["end_time"],
                session_data["session_completed"],
                session_data["mindfulness_completed"]
            )

    btn_start = tk.Button(mindfulness, text="Start ćwiczenia", command=countdown_mindfulness)
    btn_start.pack(pady=5)

    btn_close = tk.Button(mindfulness, text="Zakończ ćwiczenie", command=lambda: (
        log_session(
            session_data["start_time"],
            session_data["end_time"],
            session_data["session_completed"],
            False
        ),
        mindfulness.destroy()
    ))
    btn_close.pack(pady=5)

def log_session(start_time, end_time, session_completed, mindfulness_completed):
    log_entry = {
        "start_time": start_time,
        "end_time": end_time,
        "session_completed": session_completed,
        "mindfulness_completed": mindfulness_completed
    }

    os.makedirs("data", exist_ok=True)
    log_path = os.path.join("data", "session_log.json")

    # Jeśli plik istnieje, odczytaj i dopisz
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def show_history_window(root):
    history_window = tk.Toplevel(root)
    history_window.title("Historia sesji")
    history_window.geometry("500x300")

    # Tytuł
    title = tk.Label(history_window, text="Historia sesji", font=("Arial", 14, "bold"))
    title.pack(pady=10)

    # Lista
    listbox = tk.Listbox(history_window, width=70)
    listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    log_path = os.path.join("data", "session_log.json")

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        for entry in data:
            start = entry.get("start_time", "brak")[:16].replace("T", " ")
            session_ok = "✅" if entry.get("session_completed") else "❌"
            breath_ok = "✅" if entry.get("mindfulness_completed") else "❌"

            item = f"📅 {start} — Sesja: {session_ok}, Ćwiczenie: {breath_ok}"
            listbox.insert(tk.END, item)
    else:
        listbox.insert(tk.END, "Brak danych do wyświetlenia.")