import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb


class Window(tk.Toplevel):
    filetypes = (
        ("Текстовый файл", "*.txt"),
        ("Изображение", "*.jpg *.jpeg *.gif *.png *.bmp *.svg *.eps *.tif")
    )

    def __init__(self, parent: tk.Tk):
        self.parent = parent
        super().__init__()
        self._init_main_interface()
        self.geometry(parent.geometry())
        self.iconbitmap("media/icon.ico")
        self.title(parent.title())
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit())

    def __del__(self):
        self.parent.destroy()

    def _init_main_interface(self) -> None:
        self.frame = tk.Frame(
            self,
            padx=16,
            pady=16
        )
        self.frame.pack(expand=True)
        btn = tk.Button(
            self.frame,
            text="Назад",
            command=self.close
        )
        btn.pack()

    def choose_file(self) -> str:
        return fd.askopenfilename(
            title="Открыть файл",
            initialdir="/",
            filetypes=self.filetypes
        )

    def check_format(self, filename: str) -> str:
        if ".txt" in filename:
            return "TEXT"
        else:
            return "IMAGE"

    def show_error(self, msg: str) -> None:
        mb.showerror("Ошибка", msg)

    def close(self) -> None:
        self.destroy()
        self.parent.show()
