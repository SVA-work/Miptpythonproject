import tkinter as tk
from os import path

from python_scripts.crypter.crypter import CrypterException, encode_file
from python_scripts.window import Window


class EncryptWindow(Window):
    def __init__(self, parent: tk.Tk):
        self.__key_entry = None
        self.__write_entry = None
        self.__read_entry = None
        super().__init__(parent)

    def _init_main_interface(self) -> None:
        super()._init_main_interface()

        lbl = tk.Label(self.frame, text="Выберите файл для шифрования")
        lbl.pack()
        self.__read_entry = tk.Entry(self.frame)
        self.__read_entry.pack()
        btn = tk.Button(self.frame, text="Выбрать", command=self._choose_file_to_read)
        btn.pack()

        lbl = tk.Label(self.frame, text="Выберите файл куда сохранить зашифрованное")
        lbl.pack()
        self.__write_entry = tk.Entry(self.frame)
        self.__write_entry.pack()
        btn = tk.Button(self.frame, text="Выбрать", command=self._choose_file_to_write)
        btn.pack()

        lbl = tk.Label(self.frame, text="Введите ключ шифрования")
        lbl.pack()
        self.__key_entry = tk.Entry(self.frame)
        self.__key_entry.pack()

        btn = tk.Button(self.frame, text="Зашифровать", command=self.encrypt)
        btn.pack()

    def encrypt(self) -> None:
        if not self.__key_entry.get():
            self.show_error("Ключ не указан, пожалуйста, введите значение")
            return
        elif not path.isfile(self.__read_entry.get()):
            self.show_error("Файл, который вы хотите зашифровать, не существует")
            return

        input_file = self.__read_entry.get()
        out = self.__write_entry.get()
        key = self.__key_entry.get()
        kwargs = {"allow_rewrite": True}

        try:
            encode_file(input_file, key, out, **kwargs)
        except CrypterException as ex:
            self.show_error(str(ex))
        except Exception as ex:
            self.show_error(str(ex))

    def _choose_file_to_write(self) -> None:
        self.__write_entry.delete(0, tk.END)
        self.__write_entry.insert(0, self.choose_file())

    def _choose_file_to_read(self) -> None:
        self.__read_entry.delete(0, tk.END)
        self.__read_entry.insert(0, self.choose_file())
