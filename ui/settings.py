import configparser
import tkinter as tk

stop_checked = tk.IntVar
lemmatize_checked = tk.IntVar
ask_save = tk.IntVar


class SettingsMenu(tk.Frame):
    """
    A class to customize the behaviour of the program through a
    user inferface
    """

    def __init__(self, master) -> None:
        """
        Create the menu
        :param master: The master window
        :type master: MainWindow
        """
        self.top = tk.Toplevel(master)
        self.top.wm_title('Settings')
        self.top.columnconfigure(0, weight=2)
        self.top.geometry('300x200')
        self.top.protocol('WM_DELETE_WINDOW', self.close)

        global stop_checked, lemmatize_checked, ask_save

        self.check_stop = tk.Checkbutton(self.top, text="Include stop words",
                                         variable=stop_checked)
        self.check_lemmatize = tk.Checkbutton(self.top,
                                              text="Do not lemmatize words",
                                              variable=lemmatize_checked)
        self.check_save = tk.Checkbutton(self.top, text="Ask for save",
                                         variable=ask_save)

        # Load configuration
        config = configparser.ConfigParser()
        config.read('settings.ini')
        stop_checked.set(int(config['Checkbuttons']['stop_checked']))
        lemmatize_checked.set(int(config['Checkbuttons']['lemmatize_checked']))
        ask_save.set(int(config['Checkbuttons']['ask_save']))

        self.create_ui_elements()

    def create_ui_elements(self) -> None:
        """Create all visible elements"""
        self.check_stop.grid(row=0, column=0, sticky=tk.W)
        self.check_lemmatize.grid(row=1, column=0, sticky=tk.W)
        self.check_save.grid(row=2, column=0, sticky=tk.W)

    def close(self) -> None:
        """Destroy the menu. Saves the settings before the close."""
        global stop_checked, lemmatize_checked, ask_save
        config = configparser.ConfigParser()
        config['Checkbuttons'] = {'stop_checked': stop_checked.get(),
                                  'lemmatize_checked': lemmatize_checked.get(),
                                  'ask_save': ask_save.get()}
        with open('settings.ini', 'w') as file:
            config.write(file)
        self.top.destroy()
