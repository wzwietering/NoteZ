import tkinter as tk

import analytics
import menu_events
from ui import settings

""""This file contains the window"""


class MainWindow(tk.Frame):
    received_data = ''
    search_with_regex = False
    ignore_case = False

    def __init__(self, master: tk.Tk) -> None:
        """
        Initialize the window
        :param master: The master window
        :type master: tk.Tk
        """
        tk.Frame.__init__(self, master)
        self.master = master
        self.make_window(root)
        self.menu_event = menu_events.MenuEvents()
        self.set_settings()

    def make_window(self, root: tk.Tk) -> None:
        """
        Makes the window
        :param root: The main window
        :type root: tk.Tk
        """
        width, height = 400, 400
        root.geometry(f'{width}x{height}')
        toplevel = root.winfo_toplevel()
        toplevel.wm_state('zoomed')
        root.wm_title('NoteZ')
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.iconbitmap('res/noteZLogo.ico')

        # Text field
        self.text = text = tk.Text(root, undo=True)
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(fill=tk.BOTH, expand=1)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        text.bind_all('<Key>',
                      lambda event: self.menu_event.set_not_saved(text))
        text.tag_config('search', background='#79c5f2')

        # Menu setup
        menu = tk.Menu(root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label='New',
                              command=lambda: self.menu_event.new(
                                  text, text.get("1.0", tk.END)),
                              accelerator="Ctrl+N")
        file_menu.add_command(label='Open',
                              command=lambda: self.menu_event.load(text),
                              accelerator="Ctrl+O")
        file_menu.add_command(label='Save',
                              command=lambda: self.menu_event.save(
                                  text.get("1.0", tk.END)),
                              accelerator="Ctrl+S")
        file_menu.add_command(label='Save as',
                              command=lambda: self.menu_event.save_as(
                                  text.get("1.0", tk.END)),
                              accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label='Exit',
                              command=lambda: self.close())
        menu.add_cascade(label='File', menu=file_menu)

        edit_menu = tk.Menu(menu, tearoff=0)
        edit_menu.add_command(label='Undo', command=text.edit_undo,
                              accelerator="Ctrl+Z")
        edit_menu.add_command(label='Redo', command=text.edit_redo,
                              accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label='Copy',
                              command=lambda: root.event_generate(
                                  '<Control-c>'), accelerator="Ctrl+C")
        edit_menu.add_command(label='Cut', command=lambda: root.event_generate(
            '<Control-x>'), accelerator="Ctrl+X")
        edit_menu.add_command(label='Paste',
                              command=lambda: root.event_generate(
                                  '<Control-v>'), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label='Find',
                              command=lambda: self.menu_event.search(text,
                                                                     'search',
                                                                     self),
                              accelerator="Ctrl+F")
        menu.add_cascade(label='Edit', menu=edit_menu)

        analyzer = analytics.Analyzer()
        advanced_menu = tk.Menu(menu, tearoff=0)
        advanced_menu.add_command(label='Statistics',
                                  command=lambda: analyzer.statistics(
                                      text.get("1.0", tk.END)))
        advanced_menu.add_command(label='Character plot',
                                  command=lambda: analyzer.plot_characters(
                                      text.get("1.0", tk.END)))
        advanced_menu.add_command(label='Word plot',
                                  command=lambda: analyzer.plot_words(
                                      text.get("1.0", tk.END)))
        advanced_menu.add_command(label='Dispersion plot',
                                  command=lambda: analyzer.plot_dispersion(
                                      text.get("1.0", tk.END)))
        menu.add_cascade(label='Advanced', menu=advanced_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label='Help',
                              command=lambda: self.menu_event.help(self))
        help_menu.add_command(label='Settings',
                              command=lambda: self.menu_event.settings(self))
        menu.add_cascade(label='Help', menu=help_menu)

        # Create shortcuts
        self.bind_all("<Control-n>", lambda event: self.menu_event.new(
            text, text.get("1.0", tk.END)))
        self.bind_all("<Control-o>", lambda event: self.menu_event.load(text))
        self.bind_all("<Control-s>",
                      lambda event: self.menu_event.save(
                          text.get("1.0", tk.END)))
        self.bind_all("<Control-S>", lambda event: menu_events.save_as(
            text.get("1.0", tk.END)))
        self.bind_all("<Control-f>",
                      lambda event: self.menu_event.search(text, 'search',
                                                           self))

        root.config(menu=menu)

        self.pack()

    def set_settings(self) -> None:
        """Initialize the settings"""
        settings.stop_checked = tk.IntVar()
        settings.lemmatize_checked = tk.IntVar()
        settings.ask_save = tk.IntVar()
        settings.ask_save.set(1)

    def close(self) -> None:
        """Check for save, close the window"""
        self.menu_event.check_save(self.text.get("1.0", tk.END))
        root.destroy()
        root.quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
