import tkinter as tk
from typing import Callable, Optional
from ttkbootstrap import Entry, Button, Frame

from pdfViewer.pdf_components.results import Results
from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList


MAX_RESULTS_DISPLAY = 5

class Sidebar(Frame):
    def __init__(self, master, display_page_function: Callable[[int], None]):
        Frame.__init__(self, master)

        self.pl: Optional[AbstractPostingsList] = None
        self.display_page_function = display_page_function

        # Create an entry widget for user input
        self.entry = Entry(master)
        self.entry.pack(side=tk.LEFT, fill=tk.X, anchor=tk.NW)

        # Create a search button
        self.search_button = Button(master, text="Search")
        self.search_button.pack(side=tk.LEFT, anchor=tk.NW)

        self.results = Results(master)
        self.results.pack(side=tk.LEFT, anchor=tk.SW)


    def load_pdf_file(self):
        self.pl = CompressedPostingsList()

    def perform_search(self):
        results = self.pl.execute_query(self.entry.get())

        i = 0
        for result in results:
            i += 1
            if i > MAX_RESULTS_DISPLAY:
                break

if __name__ == '__main__':
    root = tk.Tk()
    sidebar = Sidebar(root, lambda _: None)
    root.mainloop()