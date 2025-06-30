import tkinter as tk
from pathlib import Path
from threading import Thread
from typing import Callable, Optional
from ttkbootstrap import Entry, Button, Frame

from pdfViewer.pdf_components.results import Results
from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.compressed_postings_list import (
    CompressedPostingsList,
)
from pdfwordsearch.scan.pdf_scan import pdf_info_get


class Sidebar(Frame):
    def __init__(self, master, display_page_function: Callable[[int], None]):
        Frame.__init__(self, master)

        self.pl: Optional[AbstractPostingsList] = None
        self.display_page_function = display_page_function

        self.search_widget = Frame(self)
        # Create an entry widget for user input
        self.entry = Entry(self.search_widget)
        self.entry.pack(side=tk.LEFT, fill=tk.X, anchor=tk.NW)

        # Create a search button
        self.search_button = Button(
            self.search_widget, text="Search", command=self._perform_search
        )
        self.search_button.pack(side=tk.LEFT, anchor=tk.NW)
        self.search_widget.pack(side=tk.TOP, anchor=tk.NW)

        self.results = Results(self, self.display_page_function)
        self.results.pack(side=tk.TOP, anchor=tk.SW)

        self.pdf_info = None

    def load_pdf_file(
        self, file_path: Optional[str] = None, file: Optional[bytes] = None
    ):
        if file_path is None and file is None:
            raise ValueError("Either file_path or file must be provided")

        if file_path is not None:
            info = pdf_info_get(file_path)
        else:
            info = pdf_info_get(file, is_binary=True)

        self.pdf_info = info
        self.pl = CompressedPostingsList(info)
        self.results.update_file(info)

    def _perform_search(self):
        results = self.pl.execute_query(self.entry.get())
        self.results.update_results(results)


if __name__ == "__main__":
    root = tk.Tk()
    current_dir = Path(__file__).parent
    sidebar = Sidebar(root, lambda a: print(f"Go to page {a}"))
    sidebar.pack(side=tk.LEFT)

    t1 = Thread(
        target=sidebar.load_pdf_file(
            str(
                current_dir.joinpath(
                    "../../../tests/resources/List_of_chiropterans.pdf"
                )
            )
        )
    )
    t1.start()
    root.mainloop()
