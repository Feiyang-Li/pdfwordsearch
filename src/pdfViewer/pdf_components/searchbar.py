import tkinter as tk
from pathlib import Path
from threading import Thread
from typing import Callable, Optional
from ttkbootstrap import Entry, Button, Frame, LabelFrame

from pdfViewer.pdf_components.results import Results
from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.compressed_postings_list import (
    CompressedPostingsList,
)
from pdfwordsearch.scan.pdf_scan import pdf_info_get


class SearchBar(LabelFrame):
    def __init__(self, master, display_page_function: Callable[[int], None]):
        super().__init__(master, text="Searchbar")
        self.pl: Optional[AbstractPostingsList] = None
        self.display_page_function = display_page_function

        self.search_widget = Frame(self)
        # Create an entry widget for user input
        self.entry = Entry(self.search_widget)
        self.entry.pack(side=tk.LEFT, fill=tk.X, anchor=tk.NW, expand=True)

        # Create a search button
        self.search_button = Button(
            self.search_widget, text="Search", command=self._perform_search
        )
        self.search_button.pack(side=tk.LEFT, anchor=tk.NW, expand=False)
        self.search_widget.pack(side=tk.TOP, anchor=tk.NW, expand=True, padx=5, pady=5, fill=tk.X)

        self.results = Results(self, self.display_page_function)
        self.results.pack(side=tk.TOP, anchor=tk.SW)

        master.bind("<Return>", lambda _ : self._perform_search())

    def load_pdf_file(
        self, file_path: Optional[str] = None, file: Optional[bytes] = None
    ):
        """

        Parameters
        ----------
        file_path : path to the pdf
        file : file as bytes

        Returns
        -------

        """
        if file_path is None and file is None:
            raise ValueError("Either file_path or file must be provided")

        if file_path is not None:
            info = pdf_info_get(file_path)
        else:
            info = pdf_info_get(file, is_binary=True)

        self.pl = CompressedPostingsList(info)
        self.results.update_file(info)

    def _perform_search(self):
        """
        Executes the query provided in the entry. If no pdf file is loaded, the method will do nothing.
        Returns
        -------

        """
        if self.pl is None:
            return
        results = self.pl.execute_query(self.entry.get())
        self.results.update_results(results)


if __name__ == "__main__":
    root = tk.Tk()
    current_dir = Path(__file__).parent
    sidebar = SearchBar(root, lambda a: print(f"Go to page {a}"))
    sidebar.pack(side=tk.LEFT, expand=True, fill=tk.Y, anchor=tk.NW, padx=5, pady=5)

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
