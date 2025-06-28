from tkinter import Listbox, Variable
from tkinter.constants import BOTTOM
from typing import List, Tuple

from ttkbootstrap import Entry, Button, Frame


class Results(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.list_items = Variable(value=["Start by entering a query"])
        self.listbox = Listbox(self, listvariable=self.list_items)
        self.listbox.pack(side=BOTTOM)

    def show_results(self, results: List[Tuple[int, float]]) -> None:
        pass