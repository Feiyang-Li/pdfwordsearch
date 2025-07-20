import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pymupdf
import os
import sys

from src.pdf_viewer.pdf_components.searchbar import SearchBar

def resource_path(relative_path):
    """Get absolute path to resource (works for dev and PyInstaller)"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")  # Dev mode

    return os.path.join(base_path, relative_path)

# root
# ├── main_frame (fill=BOTH)
# │   ├── left_frame (side=LEFT, fill=Y)
# │   │   └── search_bar (fill=BOTH, expand=True)
# │   └── canvas_frame (fill=BOTH, expand=True)
# └── control_frame (side=BOTTOM, fill=X)

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer with Search")

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # sidebar left:
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.search_bar = SearchBar(left_frame, self.display_page)
        self.search_bar.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # UI 
        ## mainly width and height of here affect the total size
        # Frame for canvas and scrollbars
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas with scroll support
        self.canvas = tk.Canvas(canvas_frame, 
                                width=500, 
                                height=600,
                                yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll.config(command=self.canvas.yview)
        h_scroll.config(command=self.canvas.xview)
        ##

        # mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)      # Windows & Mac
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)        # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)        # Linux scroll down

        #
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)
        # center
        button_container = tk.Frame(control_frame)
        button_container.pack(side=tk.TOP, anchor=tk.CENTER)

        tk.Button(button_container, text="Open PDF", command=self.open_pdf).pack(side=tk.LEFT)
        tk.Label(button_container, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(button_container)
        self.search_entry.pack(side=tk.LEFT)
        tk.Button(button_container, text="Go", command=self.search_text).pack(side=tk.LEFT)
        tk.Button(button_container, text="Prev", command=self.prev_page).pack(side=tk.LEFT)
        tk.Button(button_container, text="Next", command=self.next_page).pack(side=tk.LEFT)

        self.doc = None
        self.page_number = 0
        self.total_pages = 0
        self.images = []
        icon_path = resource_path("assets/searching.png")
        icon = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(True, icon)


    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        self.doc = pymupdf.open(file_path)
        self.search_bar.load_pdf_file(self.doc)
        self.total_pages = len(self.doc)
        self.page_number = 0
        self.show_page()

    def show_page(self):
        if self.doc is None:
            return

        page = self.doc.load_page(self.page_number)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))  # High-res render
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

        # Update scroll region to fit image
        self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))

        self.root.title(f"PDF Viewer - Page {self.page_number+1}/{self.total_pages}")


    def next_page(self):
        if self.doc and self.page_number < self.total_pages - 1:
            self.page_number += 1
            self.show_page()

    def prev_page(self):
        if self.doc and self.page_number > 0:
            self.page_number -= 1
            self.show_page()

    def display_page(self, page_number):
        if self.doc is None:
            return
        if not 0 <= page_number < self.total_pages:
            raise ValueError("Page number out of range")

        self.page_number = page_number
        self.show_page()

    def search_text(self):
        if self.doc is None:
            return

        query = self.search_entry.get()
        if not query:
            return

        for i in range(self.page_number, self.total_pages):
            page = self.doc.load_page(i)
            text_instances = page.search_for(query)
            if text_instances:
                self.page_number = i
                self.highlight_text(page, text_instances)
                return

        messagebox.showinfo("Search", f"'{query}' not found in remaining pages.")

    def highlight_text(self, page, rects):
        # Draw highlights and render page
        for rect in rects:
            page.draw_rect(rect, color=(1, 1, 0), fill=(1, 1, 0), overlay=True)

        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def _on_mousewheel(self, event):
        if event.state & 0x1:  # Shift key is held down
            # Horizontal scroll (Shift + wheel)
            if event.num == 4 or event.delta > 0:
                self.canvas.xview_scroll(-1, "units")  # Scroll left
            elif event.num == 5 or event.delta < 0:
                self.canvas.xview_scroll(1, "units")   # Scroll right
        else:
            # Vertical scroll (normal wheel)
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")  # Scroll up
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")   # Scroll down

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()
