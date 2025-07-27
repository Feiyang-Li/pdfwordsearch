from src.pdf_viewer.main import *
from resource.nltk_data.corpora.importWordnet import *


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()