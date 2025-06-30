from tkinter import Tk
from typing import Callable

from ttkbootstrap import Button, Frame, LabelFrame, Label


class Result(Frame):
    def __init__(
        self,
        parent,
        page_number: int,
        summary: str,
        display_page_function: Callable[[int], None] = lambda _: None,
    ):
        Frame.__init__(self, parent)
        self.label_frame = LabelFrame(self, text=f"Page {page_number}")
        self.label_frame.pack(fill="x")

        self.summary = Label(self.label_frame, text=summary)
        self.summary.pack(fill="x")

        self.go_to_button = Button(
            self.label_frame,
            text="Go to page",
            command=lambda: display_page_function(page_number),
        )
        self.go_to_button.pack(side="left")


if __name__ == "__main__":
    root = Tk()
    root.geometry("300x300")
    for i in range(3):
        r = Result(root, i, "Summary")
        r.pack()
    root.mainloop()
