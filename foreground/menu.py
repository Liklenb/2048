import tkinter
from widgets import button as button


class Menu(tkinter.Frame):
    canvas: tkinter.Canvas

    def __init__(self, frames_controller):
        super().__init__()
        self.controller = frames_controller
        self.grid(row=0, column=0)
        self.button_size = 50
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tkinter.Canvas(self, width=self.controller.root.winfo_width(),
                                     height=self.controller.root.winfo_height())
        self.canvas.pack()
        self.canvas.create_text(self.controller.root.winfo_width() / 2, 100, text="Menu", anchor="n")
        button.Button(self.canvas, self.controller.root.winfo_width() / 2, self.controller.root.winfo_height() / 2,
                      text="Aller à l'exemple", command=lambda: self.controller.example.tkraise(), anchor="center",
                      padding=(self.button_size, self.button_size))

        super_button = button.Button(self.canvas, 200, 200, text="Modifie moi !",
                                     command=lambda: self.modify_super_button(super_button))

    def modify_super_button(self, super_button):
        super_button.config_button(color=(255, 0, 0), text="Je suis modifié !", command=lambda:
                                   self.second_modify_button(super_button))
        super_button.move(100, 100)

    def second_modify_button(self, super_button):
        self.button_size += 10
        super_button.config_button(padding=(self.button_size, self.button_size))
