import globals
import tkinter as tk
from tkinter import ttk


class TurbineControl(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.labels = []
        self._setup()
        self._create_view()
        self.pack()

    def _setup(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)

    def _create_view(self):
        ttk.Label(self, text="BLE TEST UTILITY [Group 9 Team 1]").grid(row=0, column=0, columnspan=3, pady=10)
        ttk.Label(self, text="30.00V").grid(row=1, column=0, padx=20)
        ttk.Label(self, text="10.00A").grid(row=1, column=1, padx=20)
        ttk.Label(self, text="100RPM").grid(row=1, column=2, padx=20)
        ttk.Scale(self, from_=30, to=0, orient="vertical", command=lambda value: self._update(0, value)).grid(row=2, column=0, padx=20, sticky=tk.NS)
        ttk.Scale(self, from_=10, to=-10, orient="vertical", command=lambda value: self._update(1, value)).grid(row=2, column=1, padx=20, sticky=tk.NS)
        ttk.Scale(self, from_=100, to=0, orient="vertical", command=lambda value: self._update(2, value)).grid(row=2, column=2, padx=20, sticky=tk.NS)
        self.labels.append(ttk.Label(self, text="0.00"))
        self.labels.append(ttk.Label(self, text="0.00"))
        self.labels.append(ttk.Label(self, text="0.00"))
        self.labels[0].grid(row=3, column=0, padx=20)
        self.labels[1].grid(row=3, column=1, padx=20)
        self.labels[2].grid(row=3, column=2, padx=20)

    def _update(self, index, value):
        self.labels[index].configure(text='{:.2f}'.format(float(value)))
        globals.server.set_characteristic(globals.gatt[index], float(value))
