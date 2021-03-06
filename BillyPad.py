"""
main file
"""
# imports
from tkinter.filedialog import *
from tkinter.messagebox import *


def show_about() -> None:
    """
    show the about popup
    :return:
    """
    showinfo("About BillyPad", "A sophisticated text editor.")


def show_command() -> None:
    """
    show the documentation popup
    :return:
    """
    # spacing is difficult
    showinfo("Documentation",
             "File\n"
             "-----\n"
             "New        - Creates a new file.\n"
             "Open      - Opens an existing file.\n"
             "Save        - Saves the current file.\n"
             "Save As   - Saves file as a new file.\n"
             "Exit          - Quit the application\n"
             "-----------------------------------\n"
             "Edit\n"
             "-----\n"
             "Copy       - Copy selected text.\n"
             "Cut          - Cut selected text.\n"
             "Paste       - Paste text from clipboard.")


class BillyPad:
    """
    main class
    """

    _root: Tk = Tk()

    _Width: int = 500

    _Height: int = 700

    _TextArea: Text = Text(_root)

    _MenuBar: Menu = Menu(_root)

    _FileMenu: Menu = Menu(_MenuBar, tearoff=0)

    _EditMenu: Menu = Menu(_MenuBar, tearoff=0)

    _HelpMenu: Menu = Menu(_MenuBar, tearoff=0)

    _CommandMenu: Menu = Menu(_MenuBar, tearoff=0)

    _ScrollBar: Scrollbar = Scrollbar(_TextArea)

    _file = None

    def __init__(self, **kwargs):
        """
        initialize
        :param kwargs:
        """

        # icon
        try:
            self._root.wm_iconbitmap("./res/BillyPad.ico")
        except FileNotFoundError:
            # icon file not found.
            print("icon file not found,"
                  " maybe deleted or moved")
            pass

        # window size
        try:
            self._Width = kwargs['width']
            self._Height = kwargs['height']
        except KeyError:
            # gave invalid inputs
            print("gave invalid window size values")
            pass

        # window title
        self._root.title("Untitled-BillyPad")

        # Center the window
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()

        # align left
        left = (screen_width / 2) - (self._Width / 2)

        # align right
        top = (screen_height / 2) - (self._Height / 2)

        # top and bottom
        self._root.geometry('%dx%d+%d+%d' % (self._Width, self._Height, left, top))

        # auto resizable text area.
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self._TextArea.grid(sticky=N + E + S + W)

        # File Menu

        # open new file
        self._FileMenu.add_command(label="New", command=self.new_file)
        # open a already existing file
        self._FileMenu.add_command(label="Open", command=self.open_file)
        # save file
        self._FileMenu.add_command(label="Save", command=self.save_file)
        # save file
        self._FileMenu.add_command(label="Save As...", command=self.save_file_as)
        # separator
        self._FileMenu.add_separator()
        # quit the application
        self._FileMenu.add_command(label="Exit", command=self.quit_application)
        # add menu
        self._MenuBar.add_cascade(label="File", menu=self._FileMenu)

        # Edit Menu

        # cut selected
        self._EditMenu.add_command(label="Cut", command=self.cut)
        # copy selected
        self._EditMenu.add_command(label="Copy", command=self.copy)
        # paste from clipboard
        self._EditMenu.add_command(label="Paste", command=self.paste)
        # add menu
        self._MenuBar.add_cascade(label="Edit", menu=self._EditMenu)

        # Help Menu

        # Documentation
        self._HelpMenu.add_command(label="Documentation", command=show_command)
        # separator
        self._HelpMenu.add_separator()
        # about
        self._HelpMenu.add_command(label="About", command=show_about)
        # add menu
        self._MenuBar.add_cascade(label="Help", menu=self._HelpMenu)

        # add menubar
        self._root.config(menu=self._MenuBar)
        self._ScrollBar.pack(side=RIGHT, fill=Y)

        # adjust scrollbar according to the content
        self._ScrollBar.config(command=self._TextArea.yview)
        self._TextArea.config(yscrollcommand=self._ScrollBar.set)

    def quit_application(self) -> None:
        """
        exits the application.
        :return:
        """
        self._root.destroy()
        # exit()

    def open_file(self) -> None:
        """
        opens an existing file.
        :return:
        """
        self._file = askopenfilename(defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self._file == "":
            # no file to open
            self._file = None
        else:
            # Try to open the file
            # set the window title
            self._root.title(os.path.basename(self._file) + " - BillyPad")
            self._TextArea.delete(1.0, END)
            file = open(self._file, "r")
            self._TextArea.insert(1.0, file.read())
            file.close()

    def new_file(self) -> None:
        """
        Creates a new file.
        :return:
        """
        self._root.title("Untitled BillyPad")
        self._file = None
        self._TextArea.delete(1.0, END)

    def save_file(self) -> None:
        """
        saves current file.
        :return:
        """
        # save as new file
        if self._file is None:
            # Save as new file
            self._file = asksaveasfilename(initialfile='Untitled.txt',
                                           defaultextension=".txt",
                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if self._file == "":
                self._file = None
            else:
                # Try to save the file
                file = open(self._file, "w")
                file.write(self._TextArea.get(1.0, END))
                file.close()
                # Change the window title
                self._root.title(os.path.basename(self._file) + " - BillyPad")
        # overwrite existing
        else:
            file = open(self._file, "w")
            file.write(self._TextArea.get(1.0, END))
            file.close()

    def save_file_as(self) -> None:
        """
        saves file with given name
        :return:
        """
        file = asksaveasfilename(initialfile="Untitled.txt",
                                 defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"), ("Text Documents", "^.txt")])
        if file != "":
            _file = open(file, "w")
            _file.write(self._TextArea.get(1.0, END))
            _file.close()
            self._file = file
            # Change the window title
            self._root.title(os.path.basename(self._file) + " - BillyPad")

    def cut(self) -> None:
        """
        cut the selected text
        :return:
        """
        self._TextArea.event_generate("<<Cut>>")

    def copy(self) -> None:
        """
        copy the selected text
        :return:
        """
        self._TextArea.event_generate("<<Copy>>")

    def paste(self) -> None:
        """
        paste text from clipboard
        :return:
        """
        self._TextArea.event_generate("<<Paste>>")

    def run(self) -> None:
        """
        run the application loop
        :return:
        """
        # Run main application
        self._root.mainloop()


# creating an instance
billy_pad = BillyPad(width=600, height=400)
# calling run function
billy_pad.run()
