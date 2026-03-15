# main.py
# Main entry point for the Ave Mujica Logic Grimoire application

import tkinter as tk
from gui_components import AveMujicaLogicGrimoire

def main():
    root = tk.Tk()
    app = AveMujicaLogicGrimoire(root)
    root.mainloop()

if __name__ == "__main__":
    main()