import tkinter as tk
import configparser


class HelpWindow(tk.Frame):
    """
    A class to customize the behaviour of the program through a
    user inferface
    """

    def __init__(self, master: tk.Frame) -> None:
        """
        Create the menu
        :param master: The main window of which the help window is a child
        :type master: tk.Frame
        """
        self.top = tk.Toplevel(master)
        self.top.wm_title('Help')
        self.top.columnconfigure(1, weight=3)
        self.top.geometry('400x250')

        # The help items and descriptions are in a file, the lists are
        # converted to a dictionary to make the selection changed matching
        # easier.
        config = configparser.ConfigParser()
        config.read('help.ini')
        self.help_items = {}
        for items in config.options('Items'):
            self.help_items[items.capitalize()] = config.get('Items', items)

        self.items_list = tk.Listbox(self.top)
        self.textfield = tk.Label(self.top, anchor=tk.N + tk.W,
                                  justify=tk.LEFT, wraplength=260)
        self.create_ui_elements()

    def create_ui_elements(self) -> None:
        """Create all visible elements"""
        for item in self.help_items:
            self.items_list.insert(tk.END, item)
        self.items_list.bind_all('<<ListboxSelect>>', self.selection_changed)
        self.items_list.grid(row=0, column=0, sticky=tk.N)
        self.textfield.grid(row=0, column=1, sticky=tk.N)

    def selection_changed(self, event: tk.Event) -> None:
        """
        Change the text when a different keyword is selected
        :param event: The event which is triggered
        :type event: tk.Event
        """
        selection = self.items_list.selection_get()
        self.textfield.config(text=self.help_items.get(selection))
