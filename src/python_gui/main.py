from tkinter import Tk

from src.python_gui.pdf_viewer import PdfViewer

if __name__ == "__main__":
    root = Tk()
    app = PdfViewer(root)
    root.mainloop()