import tkinter as tk
from ui.TurbineControl import TurbineControl


class TurbineGui(tk.Tk):
    frame = None

    def __init__(self, width: int, height: int):
        super().__init__()
        self._setup(width, height)
        self._create_view()

    def _setup(self, width: int, height: int):
        self.title("Wind turbine")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.geometry(f"+{center_x}+{center_y}")
        self.resizable(False, False)

    def _create_view(self):
        self.frame = TurbineControl(master=self)
