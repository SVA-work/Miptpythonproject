import tkinter as tk
from PIL import ImageTk

from python_scripts.windows.encrypt import EncryptWindow
from python_scripts.windows.decrypt import DecryptWindow


class Application(tk.Tk):
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

    def __init__(self, *args, **kwargs):
        """
        Конструктор класса Application. Создает главное окно приложения, устанавливает заголовок,
        инициализирует интерфейс.

        Args:
            *args: Дополнительные аргументы для конструктора родителя.
            **kwargs: Ключевые аргументы для конструктора родителя.
        """

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
        """
        Закрывает главное окно и открывает указанное окно (EncryptWindow или DecryptWindow).

        Args:
            window (Window): Класс окна, которое нужно открыть.
        """

        self.withdraw()
        window(self)

    def show(self) -> None:
        """
        Показывает главное окно приложения, если оно было свернуто.
        """

        self.update()
        self.deiconify()
