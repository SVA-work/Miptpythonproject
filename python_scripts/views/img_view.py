import views.view as view
from PIL import ImageTk

class ImgView(view.View):
    def show(self, data):
        img = ImageTk.PhotoImage(data, master=self)
        label = view.ttk.Label(self, image=img)
        label.image = img
        label.pack(expand=1, fill='both')
