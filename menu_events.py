import tkinter as tk
from tkinter import filedialog, messagebox

from ui import search_dialog, settings, help

file_extensions = (("Text File", "*.txt"), ("All Files", "*.*"))
saved = True
save_file = None


class MenuEvents:
    """A class to handle events in the menu"""

    def new(self, text: tk.Text, data: str) -> None:
        """
        Create a new document after saving
        :param text: The text ui element
        :param data: Text inside the ui
        :type text: tk.Text
        :type data: str
        """
        self.check_save(data)
        text.delete('1.0', tk.END)

    def save(self, data: str) -> None:
        """
        Saves a piece of data
        :param data: The text to save
        :type data: str
        """
        global saved, save_file
        if save_file is None:
            self.save_as(data)
            saved = True
        else:
            with open(save_file, 'w') as file:
                file.write(data)

    def save_as(self, data: str) -> None:
        """
        Save with a certain file name
        :param data: The text to save
        :type data: str
        """
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt",
                                     filetypes=file_extensions)
        if f is None:
            return
        f.write(data)
        f.close()

        global save_file, saved
        save_file = f.name
        saved = True

    def load(self, text: tk.Text) -> None:
        """
        Load a file
        :param text: The text object to load the data to
        :type text: tk.Text
        """
        f = filedialog.askopenfilename(filetypes=file_extensions)
        if f is None:
            return
        text.delete('1.0', tk.END)
        with open(f, 'r', encoding="utf8") as file:
            text.insert('1.0', file.read())
        global saved
        saved = True

    def set_not_saved(self, text: tk.Text) -> None:
        """
        When you edit the file, this method registers that you have
        unsaved changes.
        :param text: The text object to edit
        :type text: tk.Text
        """
        text.tag_remove('search', '1.0', tk.END)
        global saved
        saved = False

    def search(self, text: tk.Text, tag: str, master: tk.Frame) -> None:
        """
        Search the document for a certain string and mark it
        :param text: The text field to search
        :param tag: The tag to highlight the text with
        :param master: The main window
        :type text: tk.Text
        :type tag: str
        :type master: tk.Frame
        """
        dialog = search_dialog.SearchDialog(master)
        master.wait_window(dialog.top)
        keyword = master.received_data
        pos = '1.0'
        while True:
            countVar = tk.StringVar()
            idx = text.search(keyword, pos, tk.END,
                              regexp=master.search_with_regex, count=countVar,
                              nocase=master.ignore_case)
            if not idx:
                break
            pos = f'{idx}+{countVar.get()}c'
            text.tag_add(tag, idx, pos)

    def settings(self, master: tk.Frame) -> None:
        """
        Show the settings menu
        :param master: The main window of which the settings window is a child
        :type master: tk.Frame
        """
        window = settings.SettingsMenu(master)
        master.wait_window(window.top)

    def help(self, master: tk.Frame) -> None:
        """
        Show the help menu
        :param master: The main window of which the help window is a child
        :type master: tk.Frame
        """
        window = help.HelpWindow(master)
        master.wait_window(window.top)

    def check_save(self, data: str) -> None:
        """
        Ask the user if he wants to save when the document is unsaved
        :param data: The text to save
        :type data: str
        """
        if not saved and settings.ask_save.get() == 1:
            if messagebox.askyesno("Save", "Do you want to save?"):
                self.save(data)
