import tkinter as tk
from os import path

from python_scripts.crypter.crypter import CrypterException, decode_image, decode_txt
from python_scripts.window import Window


class DecryptWindow(Window):
    def __init__(self, parent: tk.Tk):
        self.__key_entry = None
        self.__read_entry = None
        super().__init__(parent)

    def _init_main_interface(self) -> None:
        super()._init_main_interface()

        lbl = tk.Label(self.frame, text="Выберите файл для дешифрования")
        lbl.pack()
        self.__read_entry = tk.Entry(self.frame)
        self.__read_entry.pack()
        btn = tk.Button(self.frame, text="Выбрать", command=self.choose_file_to_read)
        btn.pack()

        lbl = tk.Label(self.frame, text="Введите ключ")
        lbl.pack()
        self.__key_entry = tk.Entry(self.frame)
        self.__key_entry.pack()

        btn = tk.Button(self.frame, text="Расшифровать", command=self.decrypt)
        btn.pack()

    def decrypt(self) -> None:
        if not self.__key_entry.get():
            self.show_error("Ключ не указан, пожалуйста, введите значение")
            return
        elif not path.isfile(self.__read_entry.get()):
            self.show_error("Файл, который вы хотите расшифровать, не существует")
            return

        input_file = self.__read_entry.get()
        key = self.__key_entry.get()
        filetype = self.check_format(input_file)
        if filetype == "TEXT":
            try:
                result = decode_txt(input_file, key)
                new_root = tk.Toplevel(self)
                lbl = tk.Label(new_root, text=result)
                lbl.pack()
            except Exception as ex:
                self.show_error(str(ex))
        elif filetype == "IMAGE":
            try:
                result = decode_image(input_file, key)
                tk_image = ImageTk.PhotoImage(result)
                new_root = tk.Toplevel(self)
                lbl = tk.Label(new_root, image=tk_image)
                lbl.image = tk_image
                lbl.pack()
            except Exception as ex:
                print(ex)
                self.show_error(str(ex))

    def choose_file_to_read(self) -> None:
        self.__read_entry.delete(0, tk.END)
        self.__read_entry.insert(0, self.choose_file())
