from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename


class ApplicationMainWindow:
    def __init__(self):
        self.root = Tk()
        self.all_widgets = []
        self.ftypes = [('Txt файлы', '*.txt'), ('Docx файлы', '*.docx'), ('Doc файлы', '*.doc')]
        self.filepath_to_encoding = ""

    def run(self):
        self.set_window()
        self.set_widgets()
        while True:
            self.root.mainloop()

    def set_window(self):
        self.root.title('Дешифратор')
        self.root.geometry('600x300')
        self.root.minsize(600, 300)
        self.root.maxsize(600, 300)

    def set_widgets(self):
        choose_label = Label(text="Выберете файл, чтобы зашифровать его")
        choose_label.grid(column=0, row=1, padx=10, pady=10)

        choose_button = Button(text="Выбрать файл", command=self.open_file)
        choose_button.grid(column=0, row=2, padx=10)

        download_label = Label(text="Сохранить выбранный файл")
        download_label.grid(column=0, row=3, padx=10, pady=20)

        download_button = Button(text="Сохранить файл", command=self.save_file)
        download_button.grid(column=0, row=4, padx=10)

        empty_label = Label()
        empty_label.grid(column=0, row=5, pady=20)

        choose_label = Label(text="Выберете файл, чтобы расшифровать его")
        choose_label.grid(column=2, row=6, padx=10, pady=10)

        choose_button = Button(text="Выбрать файл", command=self.decoding_file)
        choose_button.grid(column=2, row=7, padx=10)

    def open_file(self):
        self.filepath_to_encoding = filedialog.askopenfilename(filetypes=self.ftypes)
        lbl_filename = Label(text="Вы выбрали файл: " + self.filepath_to_encoding)
        lbl_filename.grid(column=1, row=2, padx=10)

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=self.ftypes,
        )
        if not filepath:
            return
        # вызвать encoding
        lbl_filename = Label(text="Вы сохранили зашифрованный файл: " + filepath)
        lbl_filename.grid(column=1, row=4, sticky=NSEW, padx=10)

    def decoding_file(self):
        filepath_to_decoding = filedialog.askopenfilename(filetypes=self.ftypes)
        window_with_decoding_file = Tk()
        window_with_decoding_file.title('Дешифратор')
        window_with_decoding_file.geometry('600x300')
        window_with_decoding_file.minsize(600, 300)
        txt_edit = Text(window_with_decoding_file)
        txt_edit.insert(END, "text from decoding method")
        txt_edit.grid(column=0, row=0)