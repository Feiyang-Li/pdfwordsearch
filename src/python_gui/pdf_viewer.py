# importing everything from tkinter
from tkinter import *
# importing ttk for styling widgets from tkinter
from tkinter import ttk
# importing filedialog from tkinter
from tkinter import filedialog as fd
# importing os module
import os
# importing the PDFMiner class from the miner file
from miner import PDFMiner
from src.python_gui.side_pdf_smart_search import SideSearch


# creating a class called PDFViewer
class PDFViewer:
    # initializing the __init__ / special method
    def __init__(self, master):
        self.path = None
        self.file_is_open = None
        self.author = None
        self.name = None
        self.current_page = 0
        self.num_pages = None

        self.master = master
        self.master.title('PDF Viewer')
        # Window Size
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=0, height=0)
        # loads the icon and adds it to the main window
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')
        # creating the menu
        self.menu = Menu(self.master)
        # adding it to the main window
        self.master.config(menu=self.menu)
        # creating a sub menu
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)


        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        # placing the frame using inside main window using grid()

        # the frame will not propagate
        self.top_frame.grid_propagate(False)
        # creating the bottom frame
        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        # placing the frame using inside main window using grid()

        # the frame will not propagate
        self.bottom_frame.grid_propagate(False)
        # creating a vertical scrollbar
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        # adding the scrollbar
        self.scrolly.grid(row=0, column=1, sticky=(N, S))
        # creating a horizontal scrollbar
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        # adding the scrollbar
        self.scrollx.grid(row=1, column=1, sticky=(W, E))
        # creating the canvas for display the PDF pages
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        # inserting both vertical and horizontal scrollbars to the canvas
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        # adding the canvas

        # configuring the horizontal scrollbar to the canvas
        self.scrolly.configure(command=self.output.yview)
        # configuring the vertical scrollbar to the canvas
        self.scrollx.configure(command=self.output.xview)
        # loading the button icons
        self.uparrow_icon = PhotoImage(file='uparrow.png')
        self.downarrow_icon = PhotoImage(file='downarrow.png')
        # resizing the icons to fit on buttons
        self.uparrow = self.uparrow_icon.subsample(3, 3)
        self.downarrow = self.downarrow_icon.subsample(3, 3)
        # creating an up button with an icon
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        # adding the button

        # creating a down button with an icon
        self.down_button = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        # adding the button

        # label for displaying page numbers
        self.page_label = ttk.Label(self.bottom_frame, text='page')
        # adding the label


        self.searcher = SideSearch(self.master)


        # Set locations
        self.top_frame.pack(side=TOP, fill=X)
        self.output.pack(side=TOP, fill=X)

        self.searcher.pack(side=LEFT, fill=X)

        self.down_button.pack(side=LEFT, fill=X)
        self.upbutton.pack(side=RIGHT, fill=X)
        self.page_label.pack(side=RIGHT, fill=X)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

    # function for opening pdf files
    def open_file(self):
        # open the file dialog
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        # checking if the file exists
        if filepath:
            # declaring the path
            self.path = filepath
            # extracting the pdf file from the path
            filename = os.path.basename(self.path)
            # passing the path to PDFMiner
            self.miner = PDFMiner(self.path)
            # getting data and numPages
            data, numPages = self.miner.get_metadata()
            # setting the current page to 0
            self.current_page = 0
            # checking if numPages exists
            if numPages:
                # getting the title
                self.name = data.get('title', filename[:-4])
                # getting the author
                self.author = data.get('author', None)
                self.num_pages = numPages
                # setting fileopen to True
                self.file_is_open = True
                # calling the display_page() function
                self.display_page()
                # replacing the window title with the PDF document name
                self.master.title(self.name)

    # the function to display the page
    def display_page(self):
        # checking if numPages is less than current_page and if current_page is less than
        # or equal to 0
        if 0 <= self.current_page < self.num_pages:
            # getting the page using get_page() function from miner
            self.img_file = self.miner.get_page(self.current_page)
            # inserting the page image inside the Canvas
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            # the variable to be stringified
            self.stringified_current_page = self.current_page + 1
            # updating the page label with number of pages
            self.page_label['text'] = str(self.stringified_current_page) + ' of ' + str(self.num_pages)
            # creating a region for inserting the page inside the Canvas
            region = self.output.bbox(ALL)
            # making the region to be scrollable
            self.output.configure(scrollregion=region)

            # function for displaying next page

    def next_page(self):
        # checking if file is open
        if self.file_is_open:
            # checking if current_page is less than or equal to numPages-1
            if self.current_page <= self.num_pages - 1:
                # updating the page with value 1
                self.current_page += 1
                # displaying the new page
                self.display_page()

    # function for displaying the previous page
    def previous_page(self):
        # checking if fileisopen
        if self.file_is_open:
            # checking if current_page is greater than 0
            if self.current_page > 0:
                # decrementing the current_page by 1
                self.current_page -= 1
                # displaying the previous page
                self.display_page()

    def set_page(self, page_number: int):
        if not self.file_is_open:
            return

        if not (0 <= page_number < self.num_pages):
            return

        self.current_page = page_number
        self.display_page()


# creating the root winding using Tk() class
root = Tk()
# instantiating/creating object app for class PDFViewer
app = PDFViewer(root)
# calling the mainloop to run the app infinitely until user closes it
root.mainloop()