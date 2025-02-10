import tkinter as tk
from gui.MainWindow import MainWindow

def main():
    root = tk.Tk()
    root.title("Pokémon Game")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 