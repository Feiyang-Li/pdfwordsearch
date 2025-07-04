from tkinter import Frame, ttk, VERTICAL, FALSE, RIGHT, Y, Canvas, LEFT, BOTH, TRUE, NW, Tk, NE


class VerticalScrollableFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE, anchor=NE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                                width=200, height=300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)
        self.canvas.bind('<Configure>', self._configure_canvas)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


class Window:
    def __init__(self, master, *args, **kwargs):
        self.frame = VerticalScrollableFrame(master)
        self.frame.pack(expand=True, fill=BOTH)
        self.label = ttk.Label(master, text="Shrink the window to activate the scrollbar.")
        self.label.pack()

        for i in range(10):
            ttk.Button(self.frame.interior, text=f"Button {i}").pack(padx=10, pady=5)

if __name__ == "__main__":
    root = Tk()
    window = Window(root)
    root.mainloop()