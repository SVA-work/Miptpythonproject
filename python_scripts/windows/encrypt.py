import tkinter as tk
from os import path

from python_scripts.crypter.crypter import CrypterException, encode_file
from python_scripts.window import Window


class EncryptWindow(Window):
    """
    Класс EncryptWindow для шифрования файлов.

    Этот класс наследует `Window` и предоставляет графический интерфейс для выбора файла,
    куда будет сохранен зашифрованный файл, а также для ввода ключа шифрования.

    Attributes:
        __key_entry (tk.Entry): Поле ввода для ключа шифрования.
        __write_entry (tk.Entry): Поле ввода пути сохранения зашифрованного файла.
        __read_entry (tk.Entry): Поле ввода пути исходного файла для шифрования.

    Methods:
        encrypt(): Выполняет шифрование файла на основе указанных параметров.
        _choose_file_to_write(): Вызывает диалог выбора файла для сохранения зашифрованного файла.
        _choose_file_to_read(): Вызывает диалог выбора исходного файла для шифрования.
    """

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
        """
        Выполняет шифрование файла.

        Проверяет наличие ключа шифрования и исходного файла.
        Вызывает метод `encode_file` для шифрования. Результат сохраняется в указанный путь.

        Exceptions:
            CrypterException: Исключение, связанное с ошибками шифрования.
            Exception: Прочие исключения.
        """

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
            self.show_info("Файл успешно зашифрован")
        except CrypterException as ex:
            self.show_error(str(ex))
        except Exception as ex:
            self.show_error(str(ex))

    def _choose_file_to_write(self) -> None:
        """
        Открывает диалог выбора файла для указания пути сохранения зашифрованного файла.
        """

        self.__write_entry.delete(0, tk.END)
        self.__write_entry.insert(0, self.choose_file())

    def _choose_file_to_read(self) -> None:
        """
        Открывает диалог выбора исходного файла для шифрования.
        """

        self.__read_entry.delete(0, tk.END)
        self.__read_entry.insert(0, self.choose_file())
