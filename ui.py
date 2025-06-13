import tkinter as tk
import session

def create_main_window(root):
    root.title("MateOasis")
    root.geometry("320x500")

    label = tk.Label(root, text="Witaj w MateOasis!", font=("Arial", 14))
    label.pack(pady=20)

    timer_label = tk.Label(root, text="", font=("Arial", 24))
    timer_label.pack(pady=10)

    btn_start = tk.Button(root, text="Start sesji", command=lambda: session.start_session(label, timer_label, root))
    btn_start.pack(pady=5)

    btn_end = tk.Button(root, text="Zakończ sesję", command=lambda: session.end_session(label, timer_label))
    btn_end.pack(pady=5)

    btn_history = tk.Button(root, text="Historia", command=lambda: session.show_history_window(root))
    btn_history.pack(pady=5)

    btn_stats = tk.Button(root, text="Statystyki", command=lambda: session.show_stats_window(root))
    btn_stats.pack(pady=5)

    btn_clear = tk.Button(root, text="Wyczyść historię", command=session.clear_session_log)
    btn_clear.pack(pady=5)

    btn_mood_stats = tk.Button(root, text="Statystyki nastroju", command=lambda: session.show_mood_stats_window(root))
    btn_mood_stats.pack(pady=5)
