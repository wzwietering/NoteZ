import tkinter as tk


class SearchDialog(object):
    def __init__(self, master: tk.Frame) -> None:
        """
        Creates the settings window
        :param master: The main window of which this window is a child
        :type master: tk.Frame
        """
        self.top = tk.Toplevel(master)
        self.master = master
        self.master.search_with_regex = False
        self.master.ignore_case = False
        self.top.wm_title('Search')
        self.top.protocol('WM_DELETE_WINDOW', self.close_window)
        self.top.columnconfigure(0, weight=2)

        self.label = tk.Label(self.top, text="Search for:")
        self.label.grid(row=0, column=0)
        self.entry = tk.Entry(self.top)
        self.entry.grid(row=1, column=0)
        self.button = tk.Button(self.top, text='Search', command=self.close_window)
        self.button.grid(row=2, column=0)

        self.regex_checked = tk.IntVar()
        self.check_regex = tk.Checkbutton(self.top, text="Regex", variable=self.regex_checked)
        self.check_regex.grid(row=0, column=1, sticky=tk.W)
        self.case_checked = tk.IntVar()
        self.check_case = tk.Checkbutton(self.top, text="Ignore case", variable=self.case_checked)
        self.check_case.grid(row=1, column=1, sticky=tk.W)

    def close_window(self) -> None:
        """Save the variables, close the window"""
        self.master.received_data = self.entry.get()
        if self.regex_checked.get() == 1:
            self.master.search_with_regex = True
        if self.case_checked.get() == 1:
            self.master.ignore_case = True
        self.top.destroy()
