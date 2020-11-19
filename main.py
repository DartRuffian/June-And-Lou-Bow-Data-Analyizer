# Main Imports
from tkinter import *

# Other Imports
from tkinter import filedialog
from os import getcwd, chdir, listdir

# Common functions
# Destroy all widgets of the given window_variable
def clear_window(window_variable):
    for widget in window_variable.winfo_children():
        widget.destroy()

# sets up a window with a given height and width in the center of the user's screen
def setup_window(window_variable, w, h, *, name = None, bg_color = None):
    window_variable.title(name)
    ws = window_variable.winfo_screenwidth()
    hs = window_variable.winfo_screenheight()
    x = int((ws/2) - (w/2))
    y = int((hs/2) - (h/2))
    window_variable.geometry(f"{w}x{h}+{x}+{y}")

    if bg_color is not None:
        window_variable.config(background = bg_color)

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.BASE_DIR = getcwd()
        self.file_dir = getcwd() # this is later changed but a default value is needed
        self.main_menu()

    # Opens a file explorer window with an intialdir of the current directory and sets "self.file_dir" equal the
    # to the directory of the file given
    def create_file_explorer(self):
        self.file_dir = filedialog.askopenfilename (
            initialdir = getcwd(), # Sets initial dir to current directory
            title = "Select a File",
            # filetypes sets what file types are accepted
            filetypes = (
                ("Comma Seperated Value", "*.csv*"),
                #("Excel Spreadsheet", "*.xlsx*"),
                #("All files", "*.*") # Makes the explorer accept all file types
            )
        )

        # The user either hit the close window button or "Cancel"
        if self.file_dir == "":
            Label(self, text = "Make sure to select either an excel spreadsheet or a .csv file!").grid()
            return

        Label(self, text = f"Opened file at: {self.file_dir}", fg = "green", wraplength = 500, justify = "left").grid()

    def main_menu(self):
        Label(self, text = "Welcome to the J & L Data Analyzer", fg = "white", bg = "deep sky blue", width = 50, height = 2, font = ("Calibri", 15)).grid()
        Button(self, text = "Open File Explorer", width = 30, bg = "lime", command = self.create_file_explorer).grid()
        Button(self, text = "Exit Program", width = 30, bg = "red", command = main_window.destroy).grid()

main_window = Tk()
setup_window(main_window, 500, 500, name = "J & L Data Analyzer")
app = Application(main_window)
main_window.mainloop()
