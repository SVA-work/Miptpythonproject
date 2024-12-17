import views.view as view

class TxtView(view.View):
    def show(self, data):
        text = view.ttk.Label(self, text=data, anchor="nw")
        text.pack()