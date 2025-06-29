import tkinter as tk
import session

def create_main_window(root):
    root.title("MateOasis")
    root.geometry("320x500")
    root.resizable(False, False) # Zapobiega zmianie rozmiaru okna

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Etykieta powitalna i statusowa
    label = tk.Label(main_frame, text="Witaj w MateOasis!", font=("Arial", 16, "bold"))
    label.pack(pady=(0, 20))

    # Etykieta timera
    timer_label = tk.Label(main_frame, text="--:--", font=("Courier", 48, "bold"))
    timer_label.pack(pady=10)

    # Ramka na przyciski start/stop
    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=10)

    btn_start = tk.Button(control_frame, text="Start sesji", command=lambda: session.start_session(label, timer_label, root), width=15)
    btn_start.pack(side="left", padx=5)

    btn_end = tk.Button(control_frame, text="Zakończ sesję", command=lambda: session.end_session(label, timer_label), width=15)
    btn_end.pack(side="left", padx=5)

    # Ramka na przyciski statystyk
    stats_frame = tk.Frame(main_frame)
    stats_frame.pack(pady=20)
    
    tk.Label(stats_frame, text="--- Analiza ---").pack()

    btn_history = tk.Button(stats_frame, text="Historia Sesji", command=lambda: session.show_history_window(root), width=20)
    btn_history.pack(pady=5)

    btn_stats = tk.Button(stats_frame, text="Statystyki Sesji", command=lambda: session.show_stats_window(root), width=20)
    btn_stats.pack(pady=5)
    
    btn_mood_stats = tk.Button(stats_frame, text="Statystyki Nastroju", command=lambda: session.show_mood_stats_window(root), width=20)
    btn_mood_stats.pack(pady=5)

    # NOWY PRZYCISK DO WYKRESU
    btn_mood_chart = tk.Button(stats_frame, text="Wykres Nastroju", command=lambda: session.show_mood_chart_window(root), width=20)
    btn_mood_chart.pack(pady=5)
    
    # Przycisk do czyszczenia danych
    btn_clear = tk.Button(main_frame, text="Wyczyść historię sesji", command=session.clear_session_log)
    btn_clear.pack(pady=(10, 0))