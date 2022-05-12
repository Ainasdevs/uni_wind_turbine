import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class TurbineInfo(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.ui = {}
        self.windmill_base_file = Image.open("assets/windmill_base.png")
        self.windmill_rotating_file = Image.open("assets/windmill_rotating.png")
        self.windmill_base_tk = ImageTk.PhotoImage(self.windmill_base_file)
        self.windmill_rotating_tk = ImageTk.PhotoImage(self.windmill_rotating_file)
        self.power_max = 74
        self.rpm = 50
        self.voltage = 20
        self.current = 3
        self._setup()
        self._create_view()
        self.pack()

    def _setup(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=10)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def _create_view(self):
        ttk.Label(self, text="TURBINE MONITOR UTILITY [Group 9 Team 1]").grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        self.ui["power_max_label"] = ttk.Label(self, text="0W")
        self.ui["power_max_label"].grid(row=1, column=1)
        self.ui["power_bar"] = ttk.Progressbar(self, orient="vertical", mode="determinate", length=74)
        self.ui["power_bar"].grid(row=2, column=1, rowspan=3)
        self.ui["power_label"] = ttk.Label(self, text="0W")
        self.ui["power_label"].grid(row=5, column=1)

        self.ui["rpm_label"] = ttk.Label(self, text="RPM: 0")
        self.ui["rpm_label"].grid(row=1, column=2, sticky=tk.W)
        self.ui["vol_label"] = ttk.Label(self, text="Voltage: 0.00V")
        self.ui["vol_label"].grid(row=2, column=2, sticky=tk.W)
        self.ui["cur_label"] = ttk.Label(self, text="Current: 0.00A")
        self.ui["cur_label"].grid(row=3, column=2, sticky=tk.W)
        self.ui["overspeed_label"] = ttk.Label(self, text="OVERSPEED!", foreground="red")
        self.ui["overspeed_label"].grid(row=4, column=2, rowspan=2)

        self.ui["canvas"] = tk.Canvas(self, width=94, height=123)
        self.ui["canvas"].grid(row=1, column=0, rowspan=5, sticky=tk.E)

        self.ui["canvas"].create_image(29, 57, image=self.windmill_base_tk, anchor=tk.NW)
        self.process_next_frame = self._draw_windmill().__next__
        self.after(1, self.process_next_frame)

    def _draw_windmill(self):
        seconds = time.perf_counter()
        angle = 0
        while True:
            self.windmill_rotating_tk = ImageTk.PhotoImage(self.windmill_rotating_file.rotate(angle))
            canvas_obj = self.ui["canvas"].create_image(0, 0, image=self.windmill_rotating_tk, anchor=tk.NW)
            self.master.after_idle(self.process_next_frame)
            yield
            self.ui["canvas"].delete(canvas_obj)
            seconds_now = time.perf_counter()
            delta_t = seconds_now - seconds
            seconds = seconds_now
            angle -= (self.rpm * 360 * delta_t)/60
            angle %= 360
            self._ui_update()

    def _ui_update(self):
        self.ui["power_max_label"]["text"] = "{:.0f}W".format(self.power_max)
        self.ui["rpm_label"]["text"] = "RPM: {:.0f}".format(self.rpm)
        self.ui["vol_label"]["text"] = "Voltage: {:.2f}V".format(self.voltage)
        self.ui["cur_label"]["text"] = "Current: {:.2f}A".format(self.current)
        power = abs(self.voltage * self.current)
        self.ui["power_label"]["text"] = "{:.0f}W".format(power)
        self.ui["power_bar"]["value"] = 100 * power / self.power_max
        if power > self.power_max:
            self.ui["overspeed_label"]["text"] = "OVERSPEED!"
            self.ui["overspeed_label"]["foreground"] = "red"
            self.ui["overspeed_label"].grid(row=4, column=2, rowspan=2)
        elif power > self.power_max * 0.8:
            self.ui["overspeed_label"]["text"] = "SPEED WARN"
            self.ui["overspeed_label"]["foreground"] = "orange"
            self.ui["overspeed_label"].grid(row=4, column=2, rowspan=2)
        else:
            self.ui["overspeed_label"].grid_forget()
