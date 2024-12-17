import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from views.txt_view import TxtView
from views.img_view import ImgView

import crypter.crypter as crypter


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hippocampus")
        self.iconbitmap("media/icon.ico")
        self.geometry("600x300")
        self._init_main_interface()

    def _init_main_interface(self) -> None:
        cur_mode = ttk.Label(text="Текущий режим:")
        cur_mode.grid(row=0, column=0, sticky="nw")

        opts = {
            "Шифрование файла": "enc",
            "Дешифрование текста": "txt",
            "Дешифрование изображения": "img",
            "Дешифрование в файл": "file",
        }
        self.cur_opt = tk.StringVar(value="enc")

        opt_btns = 0
        for opt in opts:
            opt_btn = ttk.Radiobutton(text=opt, value=opts[opt], variable=self.cur_opt)
            opt_btn.grid(row=1 + opt_btns, column=0, sticky="nw")
            opt_btns += 1
        
        sep = ttk.Separator(orient="horizontal")
        sep.grid(row=5, column=0, columnspan=2, sticky="we", pady=5)

        input_file = ttk.Label(text="Выберете исходный файл:")
        input_file.grid(row=6, column=0, sticky="nw")
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(width=40, textvariable=self.input_path)
        input_entry.grid(row=6, column=1, columnspan=2, sticky="nw")

        in_btn = ttk.Button(text="Обзор", command=self.get_input)
        in_btn.grid(row=6, column=3, sticky="w")
        
        output_file = ttk.Label(text="Выберете файл для сохранения:")
        output_file.grid(row=7, column=0, sticky="nw")
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(width=40, textvariable=self.output_path)
        output_entry.grid(row=7, column=1, columnspan=2, sticky="nw")

        out_btn = ttk.Button(text="Обзор", command=self.get_output)
        out_btn.grid(row=7, column=3, sticky="w")
        
        key_lbl = ttk.Label(text="Введите ключ (де)шифрования:")
        key_lbl.grid(row=8, column=0, sticky="nw")
        self.key = tk.StringVar()
        key_entry = ttk.Entry(width=40, textvariable=self.key)
        key_entry.grid(row=8, column=1, columnspan=2, sticky="nw")

        sep = ttk.Separator(orient="horizontal")
        sep.grid(row=9, column=0, columnspan=2, sticky="we", pady=5)

        run_btn = ttk.Button(text="ПУСК", command=self.run)
        run_btn.grid(row=10, column=1)
    
    def get_input(self):
        selected = fd.askopenfilename(title="Исходный файл:")
        if crypter.path.isfile(selected):
            self.input_path.set(selected)
    
    def get_output(self):
        selected = fd.askopenfilename(title="Файл для сохранения:")
        if crypter.path.isfile(selected):
            self.output_path.set(selected)

    def run(self):
        opt = self.cur_opt.get()
        in_path = self.input_path.get()
        key = self.key.get()
        out_path = self.output_path.get()
        if opt == "enc":
            crypter.encode_file(in_path, key, out_path)
        elif opt == "file":
            crypter.decode_to_file(in_path, key, out_path)
        elif opt == "txt":
            text = crypter.decode_txt(in_path, key)
            TxtView(crypter.path.basename(in_path), text)
        elif opt == "img":
            img = crypter.decode_image(in_path, key)
            ImgView(crypter.path.basename(in_path), img)
