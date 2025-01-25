from tkinter import Tk
from gui.translator import Translator

def main():
    window = Tk()
    app = Translator(window)
    window.mainloop()

if __name__ == "__main__":
    main()