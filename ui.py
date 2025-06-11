import tkinter as tk
import session

def create_main_window(root):
    root.title("MateOasis")
    root.geometry("300x400")

    label = tk.Label(root, text="Jak się dziś czujesz?", font=("Arial", 15))
    label.pack(pady=20)

    timer_label = tk.Label(root, text="", font=("Arial", 15))
    timer_label.pack(pady=10)

    btn_start = tk.Button(root, text="Start sesji", command=lambda: session.start_session(label, timer_label, root))
    btn_start.pack(pady=10)

    btn_end = tk.Button(root, text="Zakończ sesję", command=lambda: session.end_session(label, timer_label))
    btn_end.pack(pady=10)