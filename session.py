import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, Listbox, Text, Radiobutton, StringVar
import json
import os
from datetime import datetime

# Importy dla nowej funkcji wykresu
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Globalne zmienne do zarządzania stanem sesji
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
    if timer_running:
        messagebox.showwarning("MateOasis", "Sesja jest już w toku!")
        return
    label.config(text="Sesja w toku...")
    session_seconds = 25 * 60  # 25 minut
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
    elif timer_running:
        label.config(text="Sesja zakończona.")
        timer_label.config(text="00:00")
        session_data["end_time"] = datetime.now().isoformat()
        session_data["session_completed"] = True
        timer_running = False
        messagebox.showinfo("MateOasis – Przerwa", "Czas na przerwę!\nWstań, oddychaj, rozluźnij się.")
        show_mindfulness_window(root)

def end_session(label, timer_label):
    global timer_running
    if not timer_running:
        messagebox.showinfo("MateOasis", "Żadna sesja nie jest aktualnie uruchomiona.")
        return
    timer_running = False
    label.config(text="Sesja zakończona przed czasem.")
    timer_label.config(text="--:--")
    session_data["end_time"] = datetime.now().isoformat()
    session_data["session_completed"] = False
    log_session(**session_data)
    messagebox.showinfo("MateOasis", "Sesja została zakończona.")

def show_mindfulness_window(root):
    mindfulness = Toplevel(root)
    mindfulness.title("Ćwiczenie oddechowe")
    mindfulness.geometry("300x220")

    instruction = Label(mindfulness, text="Oddychaj głęboko przez 1 minutę", font=("Arial", 12), wraplength=250)
    instruction.pack(pady=10)

    timer_display = Label(mindfulness, text="01:00", font=("Arial", 24))
    timer_display.pack(pady=10)

    mindfulness_seconds = 60
    mindfulness_timer_running = False

    def countdown_mindfulness():
        nonlocal mindfulness_seconds, mindfulness_timer_running
        if not mindfulness_timer_running:
            return

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
            mindfulness_timer_running = False

    def start_mindfulness_timer():
        nonlocal mindfulness_timer_running
        if not mindfulness_timer_running:
            mindfulness_timer_running = True
            countdown_mindfulness()
            
    btn_start = Button(mindfulness, text="Start ćwiczenia", command=start_mindfulness_timer)
    btn_start.pack(pady=5)

    def close_mindfulness():
        nonlocal mindfulness_timer_running
        mindfulness_timer_running = False
        session_data["mindfulness_completed"] = False
        if session_data["session_completed"]:
             log_session(**session_data)
        mindfulness.destroy()

    btn_close = Button(mindfulness, text="Zakończ", command=close_mindfulness)
    btn_close.pack(pady=5)
    mindfulness.protocol("WM_DELETE_WINDOW", close_mindfulness)


def log_session(start_time, end_time, session_completed, mindfulness_completed):
    log_entry = {
        "start_time": start_time,
        "end_time": end_time,
        "session_completed": session_completed,
        "mindfulness_completed": mindfulness_completed
    }

    os.makedirs("data", exist_ok=True)
    log_path = os.path.join("data", "session_log.json")

    data = []
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []

    data.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def show_history_window(root):
    history_window = Toplevel(root)
    history_window.title("Historia sesji")
    history_window.geometry("500x300")

    title = Label(history_window, text="Historia sesji", font=("Arial", 14, "bold"))
    title.pack(pady=10)

    listbox = Listbox(history_window, width=70)
    listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    log_path = os.path.join("data", "session_log.json")

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for entry in reversed(data): # Wyświetlanie od najnowszych
                    start = entry.get("start_time", "brak")[:16].replace("T", " ")
                    session_ok = "✅" if entry.get("session_completed") else "❌"
                    breath_ok = "✅" if entry.get("mindfulness_completed") else "❌"
                    item = f"📅 {start} — Sesja: {session_ok}, Ćwiczenie: {breath_ok}"
                    listbox.insert(tk.END, item)
            except (json.JSONDecodeError, AttributeError):
                listbox.insert(tk.END, "Błąd odczytu pliku z historią.")
    else:
        listbox.insert(tk.END, "Brak danych do wyświetlenia.")

def show_stats_window(root):
    stats_win = Toplevel(root)
    stats_win.title("Statystyki")
    stats_win.geometry("400x250")

    title = Label(stats_win, text="Twoje statystyki", font=("Arial", 14, "bold"))
    title.pack(pady=10)

    log_path = os.path.join("data", "session_log.json")
    total = completed = mindful = 0

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    for entry in data:
                        total += 1
                        if entry.get("session_completed"):
                            completed += 1
                        if entry.get("mindfulness_completed"):
                            mindful += 1
            except json.JSONDecodeError:
                data = []

    Label(stats_win, text=f"Całkowita liczba sesji: {total}").pack(pady=5)
    Label(stats_win, text=f"Ukończone sesje: {completed}").pack(pady=5)
    Label(stats_win, text=f"Wykonane ćwiczenia: {mindful}").pack(pady=5)
    if total > 0:
        percent = (completed / total) * 100
        Label(stats_win, text=f"Skuteczność sesji: {percent:.1f}%").pack(pady=5)
    else:
        Label(stats_win, text="Skuteczność sesji: 0.0%").pack(pady=5)

def clear_session_log():
    log_path = os.path.join("data", "session_log.json")
    if os.path.exists(log_path):
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić całą historię sesji?"):
            os.remove(log_path)
            messagebox.showinfo("MateOasis", "Historia została wyczyszczona.")
    else:
        messagebox.showinfo("MateOasis", "Brak historii do usunięcia.")

def ask_daily_mood(root):
    log_path = os.path.join("data", "mood_log.json")
    today = datetime.now().date().isoformat()
    data = []

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if any(entry["date"] == today for entry in data):
                    return
            except (json.JSONDecodeError, AttributeError):
                data = []

    mood_win = Toplevel(root)
    mood_win.title("Jak się dzisiaj czujesz?")
    mood_win.geometry("400x300")
    mood_win.transient(root) # Okno modalne
    mood_win.grab_set()

    Label(mood_win, text="Jak się dzisiaj czujesz?", font=("Arial", 14)).pack(pady=10)
    
    moods_map = {"dobrze": "😊 Dobrze", "normalnie": "😐 Normalnie", "zle": "😞 Źle"}
    mood_var = StringVar(value="normalnie")

    for value, text in moods_map.items():
        Radiobutton(mood_win, text=text, variable=mood_var, value=value).pack(anchor="w", padx=20)

    Label(mood_win, text="Dlaczego? (opcjonalne):").pack(pady=10)
    reason_entry = Text(mood_win, height=5, width=40)
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

    Button(mood_win, text="Zapisz", command=save_mood).pack(pady=10)
    root.wait_window(mood_win)

def show_mood_stats_window(root):
    log_path = os.path.join("data", "mood_log.json")
    mood_win = Toplevel(root)
    mood_win.title("Nastrój – Statystyki")
    mood_win.geometry("400x300")

    Label(mood_win, text="Twoje nastroje", font=("Arial", 14, "bold")).pack(pady=10)
    
    mood_counts = {'dobrze': 0, 'normalnie': 0, 'zle': 0}

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    for entry in data:
                        mood = entry.get("mood")
                        if mood in mood_counts:
                            mood_counts[mood] += 1
            except json.JSONDecodeError:
                pass

    Label(mood_win, text=f"😊 Dobrze: {mood_counts['dobrze']} dni").pack(pady=3)
    Label(mood_win, text=f"😐 Normalnie: {mood_counts['normalnie']} dni").pack(pady=3)
    Label(mood_win, text=f"😞 Źle: {mood_counts['zle']} dni").pack(pady=3)

# NOWA FUNKCJA DO WYKRESU
def show_mood_chart_window(root):
    log_path = os.path.join("data", "mood_log.json")
    chart_win = Toplevel(root)
    chart_win.title("Wykres Nastrojów")
    chart_win.geometry("500x500")

    Label(chart_win, text="Wykres Twoich nastrojów", font=("Arial", 14, "bold")).pack(pady=10)

    mood_counts = {'Dobrze': 0, 'Normalnie': 0, 'Źle': 0}
    mood_map = {'dobrze': 'Dobrze', 'normalnie': 'Normalnie', 'zle': 'Źle'}
    
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for entry in data:
                    mood_key = entry.get("mood")
                    if mood_key in mood_map:
                        mood_counts[mood_map[mood_key]] += 1
            except json.JSONDecodeError:
                data = []
    
    labels = []
    sizes = []
    # Dodajemy tylko te etykiety, które mają wartość > 0
    for label, size in mood_counts.items():
        if size > 0:
            labels.append(label)
            sizes.append(size)

    if not sizes:
        Label(chart_win, text="Brak danych do stworzenia wykresu.").pack()
        return

    # Stworzenie figury i osi dla wykresu
    fig = Figure(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#90EE90', '#FFD700', '#FF6347'])
    ax.axis('equal')  # Zapewnia, że wykres jest kołem.

    # Osadzenie wykresu w oknie Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_win)
    canvas.draw()
    canvas.get_tk_widget().pack()