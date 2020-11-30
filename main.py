# Main Imports
from tkinter import *

# Other Imports
from tkinter import filedialog
from os import getcwd, chdir, listdir
import csv

# Common functions
# Destroy all widgets of the given window_variable
def clear_window(window_variable):
    for widget in window_variable.winfo_children():
        widget.destroy()

# sets up a window with a given height and width in the center of the user's screen
def setup_window(window_variable, w, h, *, name = '', bg_color = None, offset = (0, 0)):
    window_variable.title(name)
    ws = window_variable.winfo_screenwidth()
    hs = window_variable.winfo_screenheight()
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))
    window_variable.geometry(f'{w}x{h}+{x + offset[0]}+{y + offset[1]}')

    if bg_color is not None:
        window_variable.config(background = bg_color)

# Opens a file explorer window with an intialdir of the current directory and sets 'self.file_dir' equal the
# to the directory of the file given
def create_file_explorer(window_variable):
    file_dir = filedialog.askopenfilename (
        initialdir = '%userprofile%/documents', # Sets initial dir to the user's documents folder
        title = 'Select a File',
        # filetypes sets what file types are accepted
        filetypes = (
            ('Comma Seperated Value', '*.csv*'),
            #('Excel Spreadsheet', '*.xlsx*'),
            #('All files', '*.*') # Makes the explorer accept all file types
        )
    )

    # The user either hit the close window button or 'Cancel'
    #if file_dir == '':
        #Label(window_variable, text = 'Make sure to select a .csv file!').grid()
        #return

    return file_dir

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.BASE_DIR = getcwd()
        self.main_menu()

    # Main menu of the program, features file explorer and exit button
    def main_menu(self):
        wait_var = StringVar()

        Label(self, text = 'Current Version: BETA 0.0.10', fg = 'white', bg = 'deep sky blue', justify = 'left', width = 71).grid(sticky = W)
        Label(self, text = 'Welcome to the J & L Data Analyzer', fg = 'white', bg = 'deep sky blue', width = 50, height = 2, font = ('Calibri', 15)).grid(sticky = W)

        open_file_window = Button(self, text = 'Open File Explorer', width = 30, bg = 'lime', command = lambda: wait_var.set('load_data'))
        open_file_window.grid()

        #test_button = Button(self, text = 'Placeholder text', width = 30, bg = 'sky blue', command = lambda: wait_var.set('placeholder'))
        #test_button.grid()

        Button(self, text = 'Exit Program', width = 30, bg = 'red', command = main_window.destroy).grid()

        # probably could use something else here but this is just to wait for the 'wait_var' variable
        # to change its value
        open_file_window.wait_variable(wait_var)

        if wait_var.get() == 'placeholder':
            clear_window(self)

        elif wait_var.get() == 'load_data':
            file_dir = create_file_explorer(main_window)

            Label(self, text = f'Opened file at: \n{file_dir}', fg = 'green', wraplength = 500, justify = 'left').grid(sticky = W)

            # self.file_dir contains the actual file name, which is not desired as a directory change is needed
            # seperate the file name from the rest of the directory
            if file_dir is None or file_dir == '':
                Label(self, text = 'Make sure to select a .csv file! (The program will need to be restarted)').grid()

            else:
                file_dir = file_dir.split('/') # seperate file dir by forward slashes
                file_name = file_dir[-1] # self.file_dir[-1] is the name of the file
                del file_dir[-1] # remove file name from directory
                file_dir = '/'.join(file_dir) # convert back to string

                self.load_data(file_dir, file_name)

    # Sets the yview of all listboxes to the same value
    def OnVsb(self, *args):
        self.product_title_list.yview(*args)
        self.product_vtitle_list.yview(*args)
        self.product_sold_list.yview(*args)

    def OnMouseWheel(self, event):
        self.product_title_list.yview('scroll', -(event.delta), 'units')
        self.product_vtitle_list.yview('scroll', -(event.delta), 'units')
        self.product_sold_list.yview('scroll', -(event.delta), 'units')
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return 'break'

    # Takes the file_dir and file_name, opens the file and loads its data
    def load_data(self, file_dir, file_name):
        self.data_window = Toplevel(main_window)
        setup_window(self.data_window, 800, 540, name = f'Viewing Data of {file_name}')

        Label(self.data_window, text = 'Use the scrollbar to scroll down the list').grid(row = 0,  sticky = W)

        self.sales = []

        chdir(file_dir)
        with open(file_name, 'r', encoding = 'utf-8') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[2] != '0': # remove any items that were not sold
                    self.sales.append(line)
        chdir(self.BASE_DIR)

        del self.sales[0] # Delete the line that contains information of each column


        self.salesScrollbar = Scrollbar(self.data_window, command = self.OnVsb)

        self.product_title_list = Listbox(self.data_window, yscrollcommand = self.salesScrollbar.set, font = ('TkFixedFont', 10), width = 40, height = 29)
        self.product_vtitle_list = Listbox(self.data_window, yscrollcommand = self.salesScrollbar.set, font = ('TkFixedFont', 10), width = 50, height = 29)
        self.product_sold_list = Listbox(self.data_window, yscrollcommand = self.salesScrollbar.set, font = ('TkFixedFont', 10), width = 20, height = 29)

        Label(self.data_window, text = 'Product Title').grid(row = 1, column = 0, sticky = W)
        Label(self.data_window, text = 'Product Variant Title').grid(row = 1, column = 1, sticky = W)
        Label(self.data_window, text = '# of Product Sold').grid(row = 1, column = 2, sticky = W)

        counter = 0
        totalSold = 0
        for sale in self.sales:
            counter += 1
            self.product_title_list.insert(END, f'{counter}: {sale[0]}')
            self.product_vtitle_list.insert(END, sale[1])
            self.product_sold_list.insert(END, sale[2])
            totalSold += int(sale[2])

        self.product_title_list.insert(END, '')
        self.product_vtitle_list.insert(END, '')
        self.product_sold_list.insert(END, f'Total Bows Sold: {totalSold}')

        self.product_title_list.grid(row = 2, column = 0, sticky = W)
        self.product_vtitle_list.grid(row = 2, column = 1, sticky = W)
        self.product_sold_list.grid(row = 2, column = 2, sticky = W)

        self.product_title_list.bind('<MouseWheel>', self.OnMouseWheel)
        self.product_vtitle_list.bind('<MouseWheel>', self.OnMouseWheel)
        self.product_sold_list.bind('<MouseWheel>', self.OnMouseWheel)

        self.salesScrollbar.config(command = self.OnVsb)
        self.salesScrollbar.grid(row = 2, column = 4, sticky = 'ns')

# Create Tkinter window and start the application
main_window = Tk()
setup_window(main_window, 500, 300, name = 'J & L Data Analyzer')
app = Application(main_window)
main_window.mainloop()
