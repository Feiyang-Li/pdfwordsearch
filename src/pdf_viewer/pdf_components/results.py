from tkinter import Scrollbar
from tkinter.constants import TOP, NW, X, VERTICAL, NE, BOTH, TRUE
from typing import List, Tuple, Callable, Optional

from pymupdf import Document
from ttkbootstrap import Label, Canvas

from ttkbootstrap import Frame

from pdf_viewer.pdf_components.result import Result
from pdf_viewer.pdf_components.vertical_scrollable_frame import VerticalScrollableFrame
from pdf_viewer.utilities.summary import summary

MAX_SUMMARY_LENGTH = 5


class Results(Frame):
    def __init__(self, parent, display_page_function: Callable[[int], None]):
        Frame.__init__(self, parent)
        self.scrollable_frame = VerticalScrollableFrame(self)

        self.display_page_function = display_page_function
        self.pdf: Optional[Document] = None

    def update_file(self, pdf: Document):
        self.pdf = pdf

    def update_results(self, results: List[Tuple[int, float]]) -> None:
        for w in self.scrollable_frame.interior.pack_slaves():
            w.destroy()

        if len(results) == 0:
            self.scrollable_frame.pack_forget()
            label = Label(self.scrollable_frame.interior, text="No Results Found")
            label.pack(side=TOP)
            return

        if self.pdf is None:
            raise Exception("pdf is None")

        for index, result in enumerate(results):
            r = (Result(
                self.scrollable_frame.interior,
                result[0],
                summary(self.pdf, result[0]),
                self.display_page_function,
            )
                 .pack(side=TOP, anchor=NW, padx=5, pady=5, fill=X))

        self.scrollable_frame.pack(expand=TRUE, fill=BOTH, side=TOP, anchor=NE)
        print("Showing results")
