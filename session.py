import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

session_data = {
    "start_time": None,
    "end_time": None,
    "session_completed": False,
    "mindfulness_completed": False
}

session_seconds = 0
timer_running = False

def start_session(label, timer_label, root):
    global session_seconds, timer_running
    label.config(text="Sesja w toku...")
    session_seconds = 25 * 60
    session_data["start_time"] = datetime.now().isoformat()
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
            messagebox.showinfo("MateOasis – Przerwa", "Czas na przerwę!\nWstań, oddychaj, rozluźnij się.")
            session_data["end_time"] = datetime.now().isoformat()
            session_data["session_completed"] = True
            show_mindfulness_window(root)
            timer_running = False

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

    mindfulness_seconds = 60

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
            log_session(**session_data)

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

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
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

    title = tk.Label(history_window, text="Historia sesji", font=("Arial", 14, "bold"))
    title.pack(pady=10)

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

def show_stats_window(root):
    stats_win = tk.Toplevel(root)
    stats_win.title("Statystyki")
    stats_win.geometry("400x250")

    title = tk.Label(stats_win, text="Twoje statystyki", font=("Arial", 14, "bold"))
    title.pack(pady=10)

    log_path = os.path.join("data", "session_log.json")
    total = completed = mindful = 0

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        for entry in data:
            total += 1
            if entry.get("session_completed"):
                completed += 1
            if entry.get("mindfulness_completed"):
                mindful += 1

    tk.Label(stats_win, text=f"Całkowita liczba sesji: {total}").pack(pady=5)
    tk.Label(stats_win, text=f"Ukończone sesje: {completed}").pack(pady=5)
    tk.Label(stats_win, text=f"Wykonane ćwiczenia: {mindful}").pack(pady=5)
    if total > 0:
        percent = (completed / total) * 100
        tk.Label(stats_win, text=f"Skuteczność sesji: {percent:.1f}%").pack(pady=5)

def clear_session_log():
    log_path = os.path.join("data", "session_log.json")
    if os.path.exists(log_path):
        os.remove(log_path)
        messagebox.showinfo("MateOasis", "Historia została wyczyszczona.")
    else:
        messagebox.showinfo("MateOasis", "Brak pliku do usunięcia.")

def ask_daily_mood(root):
    log_path = os.path.join("data", "mood_log.json")
    today = datetime.now().date().isoformat()

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if any(entry["date"] == today for entry in data):
                    return
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    mood_win = tk.Toplevel(root)
    mood_win.title("Jak się dzisiaj czujesz?")
    mood_win.geometry("400x300")

    tk.Label(mood_win, text="Jak się dzisiaj czujesz?", font=("Arial", 14)).pack(pady=10)

    mood_var = tk.StringVar()

    moods = [("😊 Dobrze", "dobrze"), ("😐 Normalnie", "normalnie"), ("😞 Źle", "zle")]
    for text, value in moods:
        tk.Radiobutton(mood_win, text=text, variable=mood_var, value=value).pack(anchor="w", padx=20)

    tk.Label(mood_win, text="Dlaczego? (opcjonalne):").pack(pady=10)
    reason_entry = tk.Text(mood_win, height=5, width=40)
    reason_entry.pack()

    def save_mood():
        entry = {
            "date": today,
            "mood": mood_var.get(),
            "reason": reason_entry.get("1.0", "end").strip()
        }
        data.append(entry)
        os.makedirs("data", exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        mood_win.destroy()

    tk.Button(mood_win, text="Zapisz", command=save_mood).pack(pady=10)

def show_mood_stats_window(root):
    log_path = os.path.join("data", "mood_log.json")
    mood_win = tk.Toplevel(root)
    mood_win.title("Nastrój – Statystyki")
    mood_win.geometry("400x300")

    tk.Label(mood_win, text="Twoje nastroje", font=("Arial", 14, "bold")).pack(pady=10)

    good = normal = bad = 0
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        for entry in data:
            mood = entry.get("mood")
            if mood == "dobrze":
                good += 1
            elif mood == "normalnie":
                normal += 1
            elif mood == "zle":
                bad += 1

    tk.Label(mood_win, text=f"😊 Dobrze: {good} dni").pack(pady=3)
    tk.Label(mood_win, text=f"😐 Normalnie: {normal} dni").pack(pady=3)
    tk.Label(mood_win, text=f"😞 Źle: {bad} dni").pack(pady=3)
