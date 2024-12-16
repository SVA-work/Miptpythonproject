import tkinter as tk
from os import path

from python_scripts.crypter.crypter import CrypterException, encode_file
from python_scripts.window import Window


class EncryptWindow(Window):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.key_entry = None
        self.write_entry = None
        self.read_entry = None

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
            self.show_error(str(ex))
        except Exception as ex:
            self.show_error(str(ex))

    def choose_file_to_write(self) -> None:
        self.write_entry.delete(0, tk.END)
        self.write_entry.insert(0, self.choose_file())

    def choose_file_to_read(self) -> None:
        self.read_entry.delete(0, tk.END)
        self.read_entry.insert(0, self.choose_file())
