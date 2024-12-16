import tkinter as tk
from PIL import ImageTk

from python_scripts.windows.encrypt import EncryptWindow
from python_scripts.windows.decrypt import DecryptWindow


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Управление шифрованием файлов")
        self.iconbitmap("media/icon.ico")
        self.geometry("500x400")
        self.minsize(300, 200)
        self.__init_main_interface()

    def __init_main_interface(self) -> None:
        self.frame = tk.Frame(
            self,
            padx=16,
            pady=16
        )
        self.frame.pack(expand=True)
        label = tk.Label(
            self.frame,
            text="Выберите действие"
        )
        label.pack()
        btn = tk.Button(
            self.frame,
            text="Зашифровать файл",
            command=lambda: self._open_window(EncryptWindow)
        )
        btn.pack()
        btn = tk.Button(
            self.frame,
            text="Дешифровать файл",
            command=lambda: self._open_window(DecryptWindow)
        )
        btn.pack()

    def _open_window(self, window) -> None:
        self.withdraw()
        window(self)

    def show(self) -> None:
        self.update()
        self.deiconify()
