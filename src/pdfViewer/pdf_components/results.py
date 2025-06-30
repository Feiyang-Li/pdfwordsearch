from tkinter.constants import TOP, NW
from typing import List, Tuple, Callable, Optional
from ttkbootstrap import Label

from ttkbootstrap import Frame

from pdfViewer.pdf_components.result import Result

MAX_SUMMARY_LENGTH = 5


class Results(Frame):
    def __init__(self, parent, display_page_function: Callable[[int], None]):
        Frame.__init__(self, parent)
        self.display_page_function = display_page_function
        self.pdf_info: Optional[dict] = None

    def update_file(self, pdf_info: dict):
        self.pdf_info = pdf_info

    def update_results(self, results: List[Tuple[int, float]]) -> None:
        for w in self.pack_slaves():
            w.destroy()
        if len(results) == 0:
            print("No Results Found")
            label = Label(self, text="No Results Found")
            label.pack(side=TOP)
            return

        for index, result in enumerate(results):
            r = Result(
                self,
                result[0],
                f"{self.pdf_info[index][:MAX_SUMMARY_LENGTH]}...",
                self.display_page_function,
            )
            r.pack(side=TOP, anchor=NW, padx=5, pady=5)
        print("Showing results")
