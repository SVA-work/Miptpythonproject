import tkinter as tk
from os import path
from PIL import ImageTk, UnidentifiedImageError

from python_scripts.crypter.crypter import CrypterException, decode_image, decode_txt, decode_file
from python_scripts.window import Window


class DecryptWindow(Window):
    """
    Класс DecryptWindow для дешифрования файлов.

    Этот класс наследует `Window` и предоставляет графический интерфейс для выбора файла,
    ввода ключа дешифрования и отображения результата дешифрования.

    Attributes:
        __key_entry (tk.Entry): Поле ввода для ключа дешифрования.
        __read_entry (tk.Entry): Поле ввода пути исходного файла для дешифрования.

    Methods:
        decrypt(): Выполняет дешифрование файла и отображает результат (текст или изображение).
        choose_file_to_read(): Вызывает диалог выбора файла для дешифрования.
    """

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
        """
        Выполняет дешифрование файла.

        Проверяет наличие ключа дешифрования и файла для обработки.
        В зависимости от типа файла (текст, изображение или другой формат) вызывает
        соответствующий метод (`decode_txt`, `decode_image`, `decode_file`).

        Exceptions:
            UnidentifiedImageError: Ошибка дешифрования изображения.
            Exception: Прочие исключения.
        """

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
            except UnidentifiedImageError:
                self.show_error("Неверный ключ дешифрования или данный файл не был зашифрован")
            except Exception as ex:
                self.show_error(str(ex))
        else:  # UNDEFINED
            try:
                result = decode_file(input_file, key)
                new_root = tk.Toplevel(self)
                lbl = tk.Label(new_root, text=result)
                lbl.pack()
            except Exception as ex:
                self.show_error(str(ex))

    def choose_file_to_read(self) -> None:
        """
        Открывает диалог выбора файла для дешифрования и обновляет путь в текстовом поле.
        """

        self.__read_entry.delete(0, tk.END)
        self.__read_entry.insert(0, self.choose_file())
