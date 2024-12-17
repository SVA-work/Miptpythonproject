import tkinter as tk
from tkinter import ttk

class View(tk.Toplevel):
    def __init__(self, name, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(name)
        self.iconbitmap("media/icon.ico")
        self.show(data)
    
    def show(self, data):
        pass
