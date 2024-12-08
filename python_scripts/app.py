import re
import tkinter as tk
from os import path
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from crypter import CrypterException, encode_file, decode_txt, decode_image


class Window(tk.Toplevel):
    filetypes = (
        ("Текстовый файл", "*.txt"),
        ("Изображение", "*.jpg *.jpeg *.gif *.png *.bmp *.svg *.eps *.tif")
    )

    def __init__(self, parent: tk.Tk):
        self.parent = parent
        super().__init__()
        self.init_main_interface()
        self.geometry(parent.geometry())
        self.title(parent.title())

    def __del__(self):
        self.parent.destroy()
        self.destroy()
        super().__del__()

    def init_main_interface(self) -> None:
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


class EncryptWindow(Window):
    def init_main_interface(self) -> None:
        super().init_main_interface()

        lbl = tk.Label(self.frame, text="Выберите файл для шифрования")
        lbl.pack()
        self.read_entry = tk.Entry(self.frame)
        self.read_entry.pack()
        btn = tk.Button(self.frame, text="Выбрать", command=self.choose_file_to_read)
        btn.pack()

        lbl = tk.Label(self.frame, text="Выберите файл куда сохранить зашифрованное")
        lbl.pack()
        self.write_entry = tk.Entry(self.frame)
        self.write_entry.pack()
        btn = tk.Button(self.frame, text="Выбрать", command=self.choose_file_to_write)
        btn.pack()

        lbl = tk.Label(self.frame, text="Введите ключ шифрования")
        lbl.pack()
        self.key_entry = tk.Entry(self.frame)
        self.key_entry.pack()

        btn = tk.Button(self.frame, text="Зашифровать", command=self.encrypt)
        btn.pack()

    def encrypt(self) -> None:
        if not self.key_entry.get():
            self.show_error("Ключ не указан, пожалуйста, введите значение")
            return
        elif not path.isfile(self.read_entry.get()):
            self.show_error("Файл, который вы хотите зашифровать, не существует")
            return

        input = self.read_entry.get()
        out = self.write_entry.get()
        key = self.key_entry.get()
        kwargs = {"allow_rewrite": True}

        try:
            encode_file(input, key, out, **kwargs)
        except CrypterException as ex:
            print(ex)
            self.show_error(str(ex))
        except Exception as ex:
            print(ex)
            self.show_error(str(ex))

    def choose_file_to_write(self) -> None:
        self.write_entry.delete(0, tk.END)
        self.write_entry.insert(0, self.choose_file())

    def choose_file_to_read(self) -> None:
        self.read_entry.delete(0, tk.END)
        self.read_entry.insert(0, self.choose_file())


class DencryptWindow(Window):
    def init_main_interface(self) -> None:
        super().init_main_interface()

        lbl = tk.Label(self.frame, text="Выберите файл для дешифрования")
        lbl.pack()
        self.read_entry = tk.Entry(self.frame)
        self.read_entry.pack()
        btn = tk.Button(self.frame, text="Выбрать", command=self.choose_file_to_read)
        btn.pack()

        lbl = tk.Label(self.frame, text="Введите ключ")
        lbl.pack()
        self.key_entry = tk.Entry(self.frame)
        self.key_entry.pack()

        btn = tk.Button(self.frame, text="Расшифровать", command=self.decrypt)
        btn.pack()

    def decrypt(self) -> None:
        if not self.key_entry.get():
            self.show_error("Ключ не указан, пожалуйста, введите значение")
            return
        elif not path.isfile(self.read_entry.get()):
            self.show_error("Файл, который вы хотите расшифровать, не существует")
            return

        input = self.read_entry.get()
        key = self.key_entry.get()
        filetype = self.check_format(input)
        if filetype == "TEXT":
            try:
                result = decode_txt(input, key)
                lbl = tk.Label(self.frame, text=result)
                lbl.pack()
            except Exception as ex:
                self.show_error(str(ex))
        elif filetype == "IMAGE":
            try:
                result = decode_txt(input, key)
                lbl = tk.Label(self.frame, image=result)
                lbl.pack()
            except Exception as ex:
                self.show_error(str(ex))

    def choose_file_to_read(self) -> None:
        self.read_entry.delete(0, tk.END)
        self.read_entry.insert(0, self.choose_file())


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("SVA-work")
        self.geometry("500x400")
        self.minsize(300, 200)
        self.init_main_interface()

    def init_main_interface(self) -> None:
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
            command=lambda: self.open_window(EncryptWindow)
        )
        btn.pack()
        btn = tk.Button(
            self.frame,
            text="Дешифровать файл",
            command=lambda: self.open_window(DencryptWindow)
        )
        btn.pack()

    def open_window(self, window) -> Window:
        self.withdraw()
        return window(self)

    def show(self) -> None:
        self.update()
        self.deiconify()
