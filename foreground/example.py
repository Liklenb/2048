import tkinter.font
import widgets.button as button


class Example(tkinter.Frame):
    canvas: tkinter.Canvas

    def __init__(self, frames_controller):
        super().__init__()
        # set the controller
        self.controller = frames_controller
        # grid on the first row and first column to stack the frames
        self.grid(row=0, column=0)
        # add widgets in the frame
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tkinter.Canvas(self, width=self.controller.root.winfo_width(),
                                     height=self.controller.root.winfo_height())
        self.canvas.pack()
        self.canvas.create_text(self.controller.root.winfo_width()/2, 100, text="Exemple", anchor="n",
                                font=("Arial", 100))
        button.Button(self.canvas, self.controller.root.winfo_width()/2, self.controller.root.winfo_height()/2,
                      text="Aller au menu", command=lambda: self.controller.menu.tkraise(),
                      padding=(100, 100), font=tkinter.font.Font(size=50, family="impact"), color=(255, 0, 255),
                      hover_color=(0, 255, 0),
                      hover_text_color=(255, 0, 0), text_color=(255, 255, 255), anchor="w")
