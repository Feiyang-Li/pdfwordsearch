import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pymupdf

from pdfViewer.pdf_components.searchbar import SearchBar
from pdfwordsearch.scan.pdf_scan import pdf_info_get


class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer with Search")

        self.search_bar = SearchBar(root, self.display_page)
        self.search_bar.pack(side=tk.LEFT, fill=tk.Y, anchor=tk.NW, padx=5, pady=5)

        # UI Elements
        self.canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight() - 300)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Open PDF", command=self.open_pdf).pack(side=tk.LEFT)
        tk.Label(control_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(control_frame)
        self.search_entry.pack(side=tk.LEFT)
        tk.Button(control_frame, text="Go", command=self.search_text).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Prev", command=self.prev_page).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Next", command=self.next_page).pack(side=tk.LEFT)

        self.doc = None
        self.page_number = 0
        self.total_pages = 0
        self.images = []



    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        self.doc = pymupdf.open(file_path)
        self.search_bar.load_pdf_file(file_path)
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
        if not 0 < page_number < self.total_pages:
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

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()
