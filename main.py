from tkinter import Tk
from ui import create_main_window
import session

root = Tk()
session.ask_daily_mood(root)
create_main_window(root)
root.mainloop()
