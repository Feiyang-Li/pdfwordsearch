import tkinter as tk
from typing import Callable, Optional

from src.pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from src.pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList

MAX_RESULTS_DISPLAY = 5

class SideSearch(tk.Frame):
    def __init__(self, master, display_page_function: Callable[[int], int]):
        tk.Frame.__init__(self, master)

        self.pl : Optional[AbstractPostingsList] = None
        self.display_page_function = display_page_function

        # Create a label
        self.label = tk.Label(self, text="Search:")
        self.label.grid(column=0, row=0)

        # Create an entry widget for user input
        self.entry = tk.Entry(self)
        self.entry.grid(column=1, row=0)

        # Create a search button
        self.search_button = tk.Button(self, text="Search", command=self.perform_search)
        self.search_button.grid(column=2, row=0)

        self.results = tk.Listbox(self)
        self.results.grid(column=0, row=2)

    def load_pdf_file(self):
        self.pl = CompressedPostingsList()

    def perform_search(self):
        results = self.pl.execute_query(self.entry.get())



        i = 0
        for result in results:
            i += 1
            if i > MAX_RESULTS_DISPLAY:
                break



