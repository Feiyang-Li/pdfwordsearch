import tkinter as tk
from pathlib import Path
from threading import Thread
from typing import Callable, Optional

import pymupdf
from pymupdf import Document
from ttkbootstrap import Entry, Button, Frame, LabelFrame

from pdf_viewer.pdf_components.results import Results
from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.compressed_postings_list import (
    CompressedPostingsList,
)
from pdfwordsearch.scan.pdf_scan import pdf_info_get


class SearchBar(LabelFrame):
    def __init__(self, master, display_page_function: Callable[[int], None]):
        super().__init__(master, text="Searchbar")
        self.file: Optional[Document] = None
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
        self.search_widget.pack(side=tk.TOP, anchor=tk.NW, expand=False, padx=5, pady=5, fill=tk.X)

        self.results = Results(self, self.display_page_function)
        self.results.pack(side=tk.TOP, anchor=tk.NW, expand=True)

        master.bind("<Return>", lambda _ : self._perform_search())

    def load_pdf_file(
        self, file: Document
    ):
        """

        Parameters
        ----------
        file : file opened in pymupdf

        Returns
        -------

        """
        # info = pdf_info_get(file=file)

        self.file = file

        # self.pl = CompressedPostingsList(info)
        self.pl = CompressedPostingsList.pdf_convert_to_abl(file_position=file)




        self.results.update_file(file)

    def _perform_search(self):
        """
        Executes the query provided in the entry. If no pdf file is loaded, the method will do nothing.
        Returns
        -------

        """
        if self.pl is None:
            return
        results = self.pl.execute_query(self.entry.get())
        # ## Test
        # with open("tuples.txt", "w", encoding="utf-8") as f:
        #     for item in results:
        #         f.write(f"{item}\n")

        # ##
        self.results.update_results(results)


if __name__ == "__main__":
    root = tk.Tk()
    current_dir = Path(__file__).parent
    sidebar = SearchBar(root, lambda a: print(f"Go to page {a}"))
    sidebar.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor=tk.NW, padx=5)


    doc = pymupdf.open(current_dir.joinpath(
                    "../../../tests/resources/hello world.pdf"
                ))
    sidebar.load_pdf_file(doc)


    root.mainloop()
