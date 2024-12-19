import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import re


class Window(tk.Toplevel):
    """
    Класс Window представляет дочернее окно графического интерфейса приложения Tkinter.

    Атрибуты:
    ----------
    filetypes : tuple
        Кортеж с описанием поддерживаемых типов файлов для диалогового окна выбора файла.
    """

    filetypes = (
        ("Текстовый файл", "*.txt"),
        ("Изображение", "*.jpg *.jpeg *.gif *.png *.bmp *.svg *.eps *.tif *.webp"),
        ("Все файлы", "*")
    )

    def __init__(self, parent: tk.Tk):
        """
        Инициализирует дочернее окно, связывая его с родительским окном.

        Параметры:
        ----------
        parent : tk.Tk
            Родительское окно, к которому привязывается дочернее.
        """

        self.parent = parent
        super().__init__()
        self._init_main_interface()
        self.geometry(parent.geometry())
        self.iconbitmap("media/icon.ico")
        self.title(parent.title())
        self.protocol('WM_DELETE_WINDOW', lambda: self.quit())

    def __del__(self):
        """
        Уничтожает родительское окно при удалении дочернего.
        """

        self.parent.destroy()

    def _init_main_interface(self) -> None:
        """
        Инициализирует основной интерфейс окна.

        Создаёт фрейм с отступами и добавляет кнопку "Назад",
        которая закрывает окно.
        """

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
        """
        Открывает диалоговое окно для выбора файла.

        Возвращает:
        ----------
        str
           Путь к выбранному файлу.
        """

        return fd.askopenfilename(
            title="Открыть файл",
            filetypes=self.filetypes
        )

    def check_format(self, filename: str) -> str:
        """
        Проверяет формат выбранного файла.

        Параметры:
        ----------
        filename : str
            Путь к файлу для проверки.

        Возвращает:
        ----------
        str
            Формат файла:
            - "TEXT", если файл является текстовым.
            - "IMAGE", если файл является изображением.
            - "UNDEFINED", если формат не распознан.
        """

        if ".txt" in filename:
            return "TEXT"
        elif any([re.compile(
                pattern.replace('*', '.*')
                ).match(filename) for pattern in self.filetypes[1][1].split()]):
            return "IMAGE"
        else:
            return "UNDEFINED"

    @staticmethod
    def show_error(msg: str) -> None:
        """
        Показывает окно с сообщением об ошибке.

        Параметры:
        ----------
        msg : str
            Сообщение, отображаемое в окне ошибки.
        """

        mb.showerror("Ошибка", msg)

    @staticmethod
    def show_info(msg: str) -> None:
        """
        Показывает окно с информационным сообщением.

        Параметры:
        ----------
        msg : str
            Сообщение, отображаемое в информационном окне.
        """

        mb.showinfo("Успешная операция", msg)

    def close(self) -> None:
        """
        Закрывает текущее окно и возвращает управление родительскому окну.
        """

        self.destroy()
        self.parent.show()
